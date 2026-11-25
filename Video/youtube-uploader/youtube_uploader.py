from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
VIDEO_DIR = BASE_DIR.parent
CONFIG_PATH = BASE_DIR / "videos.json"
TEMPLATE_PATH = BASE_DIR / "template.json"
STATE_PATH = BASE_DIR / "upload_state.json"
CLIENT_SECRET_PATH = BASE_DIR / "client_secret.json"
TOKEN_PATH = BASE_DIR / "token.json"
SCOPES = ["https://www.googleapis.com/auth/youtube"]
DAY_RE = re.compile(r"^\d{1,2}$")


class UploaderError(Exception):
    pass


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise UploaderError(f"無法讀取 {path.name}：{exc}") from exc


def write_json(path: Path, data: Any) -> None:
    temporary = path.with_name(path.name + ".tmp")
    try:
        temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def load_data() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    template = read_json(TEMPLATE_PATH)
    videos = read_json(CONFIG_PATH)
    if not isinstance(template, dict) or not isinstance(videos, list):
        raise UploaderError("template.json 或 videos.json 格式錯誤，請確認檔案內容是 JSON。")
    try:
        days = [int(item["day"]) for item in videos]
    except (TypeError, ValueError, KeyError) as exc:
        raise UploaderError("videos.json 每筆資料都必須有數字 day 欄位。") from exc
    duplicates = sorted(day for day in set(days) if days.count(day) > 1)
    invalid_days = sorted(day for day in set(days) if not 1 <= day <= 30)
    if duplicates:
        raise UploaderError("videos.json 有重複集數：" + ", ".join(f"Day{day:02d}" for day in duplicates))
    if invalid_days:
        raise UploaderError("videos.json 集數只能介於 01 至 30：" + ", ".join(str(day) for day in invalid_days))
    return template, videos


def format_video(item: dict[str, Any], template: dict[str, Any]) -> dict[str, Any]:
    defaults = template.get("defaults", {})
    values = {**defaults, **item}
    day = int(values.get("day", 0))
    topic = str(values.get("topic") or "").strip()
    replacements = {"day": f"{day:02d}", "topic": topic, "title": str(values.get("title", ""))}

    def expand(value: Any) -> str:
        if value is None:
            return ""
        try:
            return str(value).format_map(replacements)
        except (KeyError, ValueError) as exc:
            raise UploaderError(f"Day{day:02d} 的範本變數無法解析：{exc}") from exc

    values["day"] = day
    values["topic"] = topic
    values["title"] = expand(values.get("title", ""))
    replacements["title"] = values["title"]
    values["description"] = expand(values.get("description", ""))
    values["tags"] = values.get("tags", [])
    values["privacy_status"] = values.get("privacy_status") or "public"
    values["video_path"] = resolve_path(values.get("video"))
    values["thumbnail_path"] = resolve_path(values.get("thumbnail")) if values.get("thumbnail") else None
    return values


def resolve_path(value: Any) -> Path | None:
    if not value:
        return None
    path = Path(str(value))
    return (BASE_DIR / path).resolve() if not path.is_absolute() else path.resolve()


def validate_video(item: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    day = item.get("day", "?")
    if not item.get("video_path") or not item["video_path"].is_file():
        errors.append(f"Day{day:02d} 找不到影片：{item.get('video', '')}")
    if not item.get("topic", "").strip():
        errors.append(f"Day{day:02d} 尚未填寫 topic（主題）。")
    if not item.get("title", "").strip():
        errors.append(f"Day{day:02d} 標題是空的，請在 videos.json 填寫 title 或 topic。")
    if len(item.get("title", "")) > 100:
        errors.append(f"Day{day:02d} 標題超過 100 個字元。")
    if len(item.get("description", "")) > 5000:
        errors.append(f"Day{day:02d} 說明超過 5,000 個字元。")
    if item.get("privacy_status") not in {"public", "unlisted", "private"}:
        errors.append(f"Day{day:02d} privacy_status 必須是 public、unlisted 或 private。")
    if not isinstance(item.get("tags"), list) or not all(isinstance(tag, str) for tag in item["tags"]):
        errors.append(f"Day{day:02d} tags 必須是字串陣列。")
    if item.get("made_for_kids") is not None and not isinstance(item["made_for_kids"], bool):
        errors.append(f"Day{day:02d} made_for_kids 必須是 JSON 布林值 true 或 false。")
    if item.get("thumbnail_path"):
        thumbnail = item["thumbnail_path"]
        if not thumbnail.is_file():
            errors.append(f"Day{day:02d} 找不到縮圖：{item.get('thumbnail')}")
        elif thumbnail.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            errors.append(f"Day{day:02d} 縮圖格式只接受 JPG 或 PNG：{thumbnail.name}")
    publish_at = item.get("publish_at")
    if publish_at:
        try:
            scheduled = datetime.fromisoformat(str(publish_at).replace("Z", "+00:00"))
            if scheduled.tzinfo is None:
                errors.append(f"Day{day:02d} publish_at 必須含時區，例如 2026-12-01T09:00:00+08:00。")
            elif scheduled <= datetime.now(timezone.utc):
                errors.append(f"Day{day:02d} publish_at 必須是未來時間。")
        except ValueError:
            errors.append(f"Day{day:02d} publish_at 格式錯誤，請用 ISO 8601 並附時區。")
    return errors


def select_items(items: list[dict[str, Any]], day: str | None, day_range: str | None, all_items: bool) -> list[dict[str, Any]]:
    if day:
        if not DAY_RE.fullmatch(day) or not 1 <= int(day) <= 30:
            raise UploaderError("集數請輸入 01 至 30。")
        selected_days = {int(day)}
    elif day_range:
        try:
            first, last = (int(value) for value in day_range.split("-", 1))
        except (ValueError, TypeError) as exc:
            raise UploaderError("範圍格式需為 --range 01-05。") from exc
        if first > last:
            raise UploaderError("集數範圍起點不可大於終點。")
        if first < 1 or last > 30:
            raise UploaderError("集數範圍需介於 01 至 30。")
        selected_days = set(range(first, last + 1))
    elif all_items:
        selected_days = None
    else:
        raise UploaderError("請指定 --day、--range 或 --all。")
    selected = [item for item in items if selected_days is None or int(item.get("day", -1)) in selected_days]
    if selected_days is not None and {int(item.get("day", -1)) for item in selected} != selected_days:
        missing = sorted(selected_days - {int(item.get("day", -1)) for item in selected})
        raise UploaderError("上傳清單缺少集數：" + ", ".join(f"Day{number:02d}" for number in missing))
    return selected


def load_state() -> dict[str, Any]:
    state = read_json(STATE_PATH, {})
    if not isinstance(state, dict):
        raise UploaderError("upload_state.json 格式錯誤；請先備份後修復或移除該檔案。")
    return state


def get_youtube(*, interactive: bool, force_reauth: bool = False):
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError as exc:
        raise UploaderError("尚未安裝依賴套件。請先執行：python -m pip install -r requirements.txt") from exc

    if not CLIENT_SECRET_PATH.is_file():
        raise UploaderError("找不到 client_secret.json。請依 README.md 從 Google Cloud 下載 OAuth 桌面應用程式憑證並放在本資料夾。")
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES) if TOKEN_PATH.is_file() and not force_reauth else None
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    if not creds or not creds.valid:
        if not interactive:
            raise UploaderError("尚未完成 Google 授權。請先執行：python youtube_uploader.py auth")
        flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_PATH), SCOPES)
        creds = flow.run_local_server(port=0, prompt="select_account consent", access_type="offline")
        TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
    return build("youtube", "v3", credentials=creds, cache_discovery=False)


def execute_upload(youtube: Any, item: dict[str, Any], state: dict[str, Any]) -> None:
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload

    day = int(item["day"])
    key = f"{day:02d}"
    body: dict[str, Any] = {
        "snippet": {
            "title": item["title"],
            "description": item["description"],
            "tags": item["tags"],
            "categoryId": str(item.get("category_id", "27")),
            "defaultLanguage": item.get("language", "zh-TW"),
        },
        "status": {"privacyStatus": "private" if item.get("publish_at") else item["privacy_status"]},
    }
    if item.get("publish_at"):
        scheduled = datetime.fromisoformat(str(item["publish_at"]).replace("Z", "+00:00"))
        body["status"]["publishAt"] = scheduled.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    if item.get("made_for_kids") is not None:
        body["status"]["selfDeclaredMadeForKids"] = item["made_for_kids"]

    existing = state.get(key, {})
    video_id = existing.get("video_id")
    if not video_id:
        media = MediaFileUpload(str(item["video_path"]), mimetype="video/mp4", chunksize=8 * 1024 * 1024, resumable=True)
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        response = None
        while response is None:
            try:
                status, response = request.next_chunk(num_retries=5)
                if status:
                    print(f"  上傳進度：{status.progress() * 100:.0f}%", end="\r", flush=True)
            except HttpError:
                raise
            except Exception as exc:
                raise UploaderError(f"Day{day:02d} 上傳中斷，可重新執行同一命令重試：{exc}") from exc
        video_id = response["id"]
        actual_privacy = response.get("status", {}).get("privacyStatus", body["status"]["privacyStatus"])
        state[key] = {"video_id": video_id, "url": f"https://youtu.be/{video_id}", "status": "uploaded", "privacy_status": actual_privacy, "uploaded_at": datetime.now(timezone.utc).isoformat(), "thumbnail": "pending" if item.get("thumbnail_path") else "not_configured", "playlist": "pending" if item.get("playlist_id") else "not_configured"}
        write_json(STATE_PATH, state)
        print()

    result = state[key]
    if item.get("thumbnail_path") and result.get("thumbnail") != "done":
        processing = youtube.videos().list(part="processingDetails", id=video_id).execute()
        details = (processing.get("items") or [{}])[0].get("processingDetails", {})
        if details.get("processingStatus") == "succeeded":
            thumbnail = item["thumbnail_path"]
            mime_type = mimetypes.guess_type(str(thumbnail))[0] or "image/jpeg"
            youtube.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(str(thumbnail), mimetype=mime_type)).execute()
            result["thumbnail"] = "done"
            write_json(STATE_PATH, state)
            print(f"  已設定自訂縮圖：{thumbnail.name}")
        else:
            result["thumbnail"] = "pending"
            write_json(STATE_PATH, state)
            print("  影片仍在 YouTube 處理中；縮圖將在下次執行上傳命令時重試。")
    if item.get("playlist_id") and result.get("playlist") != "done":
        youtube.playlistItems().insert(part="snippet", body={"snippet": {"playlistId": item["playlist_id"], "resourceId": {"kind": "youtube#video", "videoId": video_id}}}).execute()
        result["playlist"] = "done"
        write_json(STATE_PATH, state)
        print(f"  已加入播放清單：{item['playlist_id']}")
    result["status"] = "scheduled" if item.get("publish_at") else "uploaded"
    result["publish_at"] = item.get("publish_at")
    write_json(STATE_PATH, state)
    visibility = "排程發布 " + item["publish_at"] if item.get("publish_at") else result.get("privacy_status", item["privacy_status"])
    print(f"Day{day:02d} 完成：{result['url']}（{visibility}）")


def print_preview(items: list[dict[str, Any]], state: dict[str, Any]) -> int:
    invalid = 0
    if not items:
        print("沒有符合條件的集數。")
        return 1
    for item in items:
        day = int(item["day"])
        errors = validate_video(item)
        status = state.get(f"{day:02d}", {})
        print(f"\nDay{day:02d}｜{item.get('topic') or '（待填主題）'}")
        print(f"  影片：{item['video_path']}")
        print(f"  標題：{item.get('title') or '（待填）'}")
        print(f"  可見度：{'排程 ' + item['publish_at'] if item.get('publish_at') else item.get('privacy_status', 'public')}")
        print(f"  縮圖：{item.get('thumbnail_path') or '未設定'}")
        print(f"  播放清單：{item.get('playlist_id') or '未設定'}")
        print(f"  上傳紀錄：{status.get('url', '尚未上傳')}")
        for error in errors:
            invalid += 1
            print(f"  錯誤：{error}")
    return 1 if invalid else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="上傳本機影片至 YouTube 頻道。")
    subparsers = parser.add_subparsers(dest="command", required=True)
    auth_parser = subparsers.add_parser("auth", help="開啟瀏覽器完成 Google OAuth 授權。")
    auth_parser.add_argument("--reauthorize", action="store_true", help="重新選擇 Google 帳號及 YouTube 頻道。")
    subparsers.add_parser("list", help="列出上傳清單與上傳狀態。")
    for name, help_text in (("preview", "預覽影片資料及檢查錯誤。"), ("upload", "上傳影片並套用設定。")):
        sub = subparsers.add_parser(name, help=help_text)
        selection = sub.add_mutually_exclusive_group(required=True)
        selection.add_argument("--day", help="單集，例如 01。")
        selection.add_argument("--range", dest="day_range", help="集數範圍，例如 01-05。")
        selection.add_argument("--all", action="store_true", help="選擇清單中的所有集數。")
        if name == "upload":
            sub.add_argument("--yes", action="store_true", help="略過上傳前確認。")
            sub.add_argument("--retry", action="store_true", help="重試未完成步驟；已完成影片仍會跳過。")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        template, raw_items = load_data()
        items = [format_video(item, template) for item in raw_items]
        if args.command == "auth":
            youtube = get_youtube(interactive=True, force_reauth=args.reauthorize)
            channel = youtube.channels().list(part="snippet", mine=True).execute()
            channels = channel.get("items", [])
            if not channels:
                raise UploaderError("授權帳號找不到 YouTube 頻道。請確認這個 Google 帳號能在 YouTube Studio 切換到目標頻道；若是品牌頻道，請在 YouTube 設定預設頻道，再執行 auth --reauthorize。")
            print(f"已授權頻道：{channels[0]['snippet']['title']}")
            return 0
        if args.command == "list":
            state = load_state()
            for item in items:
                day = int(item["day"])
                saved = state.get(f"{day:02d}", {})
                print(f"Day{day:02d}  {item.get('topic') or '待填主題'}  {saved.get('status', '待上傳')}  {saved.get('url', '')}")
            return 0
        selected = select_items(items, args.day, args.day_range, args.all)
        state = load_state()
        code = print_preview(selected, state)
        if args.command == "preview" or code:
            return code
        pending = [
            item for item in selected
            if not state.get(f"{int(item['day']):02d}", {}).get("video_id")
            or (item.get("thumbnail_path") and state.get(f"{int(item['day']):02d}", {}).get("thumbnail") != "done")
            or (item.get("playlist_id") and state.get(f"{int(item['day']):02d}", {}).get("playlist") != "done")
            or args.retry
        ]
        already_done = [item for item in selected if item not in pending]
        if already_done:
            print("\n以下影片已上傳，會跳過：" + ", ".join(f"Day{int(item['day']):02d}" for item in already_done))
        if not pending:
            print("沒有待上傳影片。")
            return 0
        if not args.yes:
            answer = input(f"\n即將處理 {len(pending)} 集；預設公開（排程集數會先設為私人）。繼續？[y/N] ").strip().lower()
            if answer not in {"y", "yes"}:
                print("已取消，沒有開始上傳。")
                return 0
        youtube = get_youtube(interactive=True)
        failures = 0
        for item in pending:
            try:
                execute_upload(youtube, item, state)
            except Exception as exc:
                failures += 1
                print(f"Day{int(item['day']):02d} 失敗：{exc}", file=sys.stderr)
                key = f"{int(item['day']):02d}"
                if key not in state:
                    state[key] = {"status": "failed", "error": str(exc), "failed_at": datetime.now(timezone.utc).isoformat()}
                else:
                    state[key]["error"] = str(exc)
                write_json(STATE_PATH, state)
        return 1 if failures else 0
    except UploaderError as exc:
        print(f"錯誤：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
