"""Create consistent 9:16 YouTube Shorts thumbnails from videos.json."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "thumbnails"
FONT_REGULAR = Path("C:/Windows/Fonts/NotoSansTC-VF.ttf")
FONT_BOLD = Path("C:/Windows/Fonts/msjhbd.ttc")
SIZE = (1080, 1920)
INK = "#161722"
BLUE = "#2925D9"
MUTED = "#646579"
PAPER = "#F7F6E8"


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    if not path.is_file():
        raise FileNotFoundError(f"找不到字型：{path}")
    return ImageFont.truetype(str(path), size)


def wrap_text(draw: ImageDraw.ImageDraw, value: str, text_font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for character in value:
        candidate = current + character
        if current and draw.textlength(candidate, font=text_font) > max_width:
            lines.append(current)
            current = character
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def render(item: dict, destination: Path) -> None:
    day = int(item["day"])
    hook = item["title"].split("｜", 1)[0].strip()
    topic = item["topic"].strip()
    if not hook or not topic:
        raise ValueError(f"Day{day:02d} 缺少標題或主題")

    canvas = Image.new("RGB", SIZE, PAPER)
    draw = ImageDraw.Draw(canvas)
    regular = font(FONT_REGULAR, 46)
    small = font(FONT_REGULAR, 40)
    bold = font(FONT_BOLD, 102)
    number = font(FONT_BOLD, 246)

    draw.rounded_rectangle((70, 70, 1010, 1850), radius=42, outline="#DAD8EA", width=3)
    draw.text((115, 130), "徵授信新手", font=regular, fill=BLUE)
    draw.text((705, 137), "30 DAYS", font=small, fill=MUTED)
    draw.line((115, 225, 965, 225), fill="#CAC9DF", width=3)

    draw.rounded_rectangle((115, 300, 385, 385), radius=42, fill=BLUE)
    draw.text((151, 310), f"DAY {day:02d}", font=font(FONT_BOLD, 48), fill="white")
    draw.text((112, 400), f"{day:02d}", font=number, fill=BLUE, stroke_width=0)
    draw.rectangle((116, 666, 360, 680), fill=BLUE)

    heading_size = 102
    while True:
        heading_font = font(FONT_BOLD, heading_size)
        lines = wrap_text(draw, hook, heading_font, 850)
        if len(lines) <= 4 or heading_size <= 72:
            break
        heading_size -= 6
    line_height = heading_size + 48
    heading_y = 790 + max(0, (4 - len(lines)) * 34)
    for index, line in enumerate(lines):
        draw.text((115, heading_y + index * line_height), line, font=heading_font, fill=INK)

    draw.line((115, 1450, 965, 1450), fill="#CAC9DF", width=3)
    draw.text((115, 1495), "本集重點", font=small, fill=MUTED)
    topic_font = font(FONT_BOLD, 61)
    topic_lines = wrap_text(draw, topic, topic_font, 850)
    for index, line in enumerate(topic_lines[:2]):
        draw.text((115, 1575 + index * 82), line, font=topic_font, fill=BLUE)
    draw.rounded_rectangle((115, 1757, 965, 1766), radius=4, fill=BLUE)
    draw.text((115, 1790), "先查證，再判斷", font=small, fill=MUTED)

    destination.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(destination, format="JPEG", quality=91, optimize=True, subsampling=0)


def main() -> None:
    items = json.loads((ROOT / "videos.json").read_text(encoding="utf-8"))
    if len(items) != 30 or {int(item["day"]) for item in items} != set(range(1, 31)):
        raise ValueError("videos.json 必須包含 Day01–Day30 各一筆")
    for item in items:
        render(item, OUTPUT / f"day{int(item['day']):02d}.jpg")
    print(f"已產生 {len(items)} 張縮圖：{OUTPUT}")


if __name__ == "__main__":
    main()
