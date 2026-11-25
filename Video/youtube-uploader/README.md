# YouTube 影片上傳工具

Windows PowerShell 命令列工具，使用 `videos.json` 和 `template.json` 管理 Day 01～Day 30 影片的標題、說明、縮圖、播放清單與發布設定。

## 專案目前狀態

30 集均已上傳並設為公開，自訂縮圖與播放清單設定完成。播放清單已依 Day 01 至 Day 30 排序：

- [觀看 YouTube 播放清單](https://www.youtube.com/playlist?list=PLT1rFkuL6ecg)
- [課程首頁](https://30-days-of-sme-credit.killysss123.workers.dev/)

本次 30 集均為立即公開，沒有設定排程。操作前請先執行 `list` 確認狀態；已上傳集數會依 `upload_state.json` 跳過，重跑一般上傳不會更新已發布影片。

## 1. 開啟 PowerShell 並進入資料夾

```powershell
Set-Location 'D:\VIbeCoding\30-days-of-sme-credit\Video\youtube-uploader'
```

## 2. 安裝 Python 套件

需要 Python 3.10 或更新版本：

```powershell
python --version
python -m pip install -r requirements.txt
```

## 3. 設定 Google OAuth（首次使用）

在 Google Cloud Console 建立或選取專案，啟用 **YouTube Data API v3**，完成 OAuth 同意畫面設定，並建立類型為 **桌面應用程式** 的 OAuth 用戶端 ID。下載 JSON 憑證，放到本資料夾並命名為 `client_secret.json`。

接著執行授權：

```powershell
python youtube_uploader.py auth
```

瀏覽器開啟後，登入能使用目標 YouTube 頻道「不冒險的藝術家」的 Google 帳號，並選取該 YouTube 頻道完成授權。成功後會在本機建立 `token.json`。

如需重新選擇帳號或頻道：

```powershell
python youtube_uploader.py auth --reauthorize
```

OAuth 憑證和 token 具有帳戶存取權，請留在本機，不要貼到聊天、提交 Git 或放到公開資料夾。

## 4. 檢查上傳資料

- `videos.json`：各集影片路徑、標題、說明、縮圖、播放清單與排程時間。
- `template.json`：標題與說明共用範本。
- `thumbnails/`：Day 01～Day 30 自訂縮圖。
- `upload_state.json`：影片 ID、網址及上傳、縮圖、播放清單步驟狀態。

影片檔案路徑以本資料夾為基準，目前設定指向上一層的 `Day01.mp4` 至 `Day30.mp4`。目前播放清單 ID 是 `PLT1rFkuL6ecg`。

未設定 `publish_at` 時，預設立即公開。排程時間須為未來的 ISO 8601 日期時間並包含時區，例如 `2026-12-01T09:00:00+08:00`；排程影片在發布前會維持私人狀態。

檢查影片清單與上傳狀態：

```powershell
python youtube_uploader.py list
```

依目前各集標題重新產生縮圖：

```powershell
python generate_thumbnails.py
```

## 5. 預覽資料

預覽不會上傳影片。可選單集、範圍或全部：

```powershell
python youtube_uploader.py preview --day 01
python youtube_uploader.py preview --range 01-05
python youtube_uploader.py preview --all
```

## 6. 上傳影片

上傳單集、指定範圍或全部：

```powershell
python youtube_uploader.py upload --day 01
python youtube_uploader.py upload --range 02-05
python youtube_uploader.py upload --all
```

程式會先顯示上傳資料並要求確認。可加上 `--yes` 略過互動確認，適合已檢查設定的批次操作：

```powershell
python youtube_uploader.py upload --day 01 --yes
python youtube_uploader.py upload --range 02-05 --yes
python youtube_uploader.py upload --all --yes
```

`--yes` 會依照資料設定直接執行；未排程的影片會立即公開。使用前請先執行對應的 `preview` 指令。

## 7. 重試未完成的設定

若影片已上傳，但自訂縮圖或加入播放清單失敗，使用 `--retry` 補做。這會沿用紀錄中的影片 ID，不會另外建立重複影片：

```powershell
python youtube_uploader.py upload --day 01 --retry
python youtube_uploader.py upload --range 01-05 --retry
python youtube_uploader.py upload --all --retry
```

若縮圖因影片仍在處理或頻道資格而失敗，待處理完成或取得資格後，再用相同集數的 `--retry` 指令重試。

## 建議的日常流程

```powershell
Set-Location 'D:\VIbeCoding\30-days-of-sme-credit\Video\youtube-uploader'
python youtube_uploader.py list
python youtube_uploader.py preview --day 01
python youtube_uploader.py upload --day 01
python youtube_uploader.py list
```

單集流程確認正常後，再依需求預覽並上傳其他集數。全部已上傳時，不必重跑 `upload --all`；若僅需補做縮圖或播放清單步驟，使用 `--retry`。

## 常見問題

- **找不到 YouTube 頻道：** 確認授權的 Google 帳號能在 YouTube Studio 切換至目標頻道，再執行 `python youtube_uploader.py auth --reauthorize`。
- **找不到套件：** 在本資料夾執行 `python -m pip install -r requirements.txt`。
- **找不到影片或縮圖：** 確認檔案存在，且 `videos.json` 路徑是以本資料夾為基準。
- **更新已發布影片標題或說明：** 一般上傳會跳過已完成影片。請在 YouTube Studio 編輯該影片。
- **API 配額或每日上傳限制：** 依錯誤訊息稍後重試；已完成項目會保留在 `upload_state.json`。

## 本機憑證與上傳限制

`client_secret.json`、`token.json` 和 `upload_state.json` 是本機資料，已由 `.gitignore` 排除於 Git。不要分享 OAuth 憑證或 token。上傳受 YouTube Data API 配額、頻道每日上傳限制及自訂縮圖資格影響。程式執行期間會重試暫時性分段傳輸錯誤；如果程序中斷，尚未完成的影片可能需要重新上傳。
