import requests
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from datetime import datetime, timezone

CLUB_SLUG = "and-chess-for-all-1"
OUTPUT_FILE = "acfa-welcome-board.png"
DEFAULT_AVATAR = "https://www.chess.com/bundles/web/images/user-image.007dad08.svg"

WIDTH = 900
HEIGHT = 520

def get_font(size, bold=False):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in font_paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def time_ago(unix_time):
    seconds = int(datetime.now(timezone.utc).timestamp() - unix_time)
    if seconds < 60:
        return "just now"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}m ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours}h ago"
    days = hours // 24
    if days < 30:
        return f"{days}d ago"
    months = days // 30
    if months < 12:
        return f"{months}mo ago"
    years = months // 12
    return f"{years}y ago"

def fetch_new_members():
    headers = {"User-Agent": "ACFA-Welcome-Board-Image/1.0"}
    url = f"https://api.chess.com/pub/club/{CLUB_SLUG}/members"
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    data = r.json()

    members = []
    for section in ["weekly", "monthly", "all_time"]:
        members.extend(data.get(section, []))

    seen = set()
    unique = []
    for m in members:
        username = m.get("username")
        joined = m.get("joined")
        if username and joined and username not in seen:
            seen.add(username)
            unique.append(m)

    unique.sort(key=lambda x: x.get("joined", 0), reverse=True)
    return unique[:5]

def draw_rounded_rectangle(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def generate_board():
    members = fetch_new_members()

    img = Image.new("RGB", (WIDTH, HEIGHT), (5, 5, 5))
    draw = ImageDraw.Draw(img)

    gold = (255, 215, 0)
    dark_gold = (184, 134, 11)
    text_light = (245, 230, 168)
    muted = (190, 170, 100)

    # Background glow
    for i in range(220, 0, -4):
        alpha_color = (
            min(30 + i // 10, 80),
            min(25 + i // 14, 60),
            8
        )
        draw.ellipse(
            (WIDTH//2 - i*2, -i, WIDTH//2 + i*2, i*2),
            fill=alpha_color
        )

    # Outer border
    draw_rounded_rectangle(draw, (18, 18, WIDTH - 18, HEIGHT - 18), 24, (8, 8, 8), gold, 4)
    draw_rounded_rectangle(draw, (30, 30, WIDTH - 30, HEIGHT - 30), 18, (12, 12, 12), dark_gold, 1)

    title_font = get_font(48, True)
    subtitle_font = get_font(24, False)
    name_font = get_font(30, True)
    small_font = get_font(20, False)
    rank_font = get_font(24, True)

    # Header
    title = "ACFA NEW MEMBERS"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((WIDTH - (bbox[2]-bbox[0])) // 2, 48), title, font=title_font, fill=gold)

    subtitle = "Every Player Belongs • Every Move Matters"
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    draw.text(((WIDTH - (bbox[2]-bbox[0])) // 2, 105), subtitle, font=subtitle_font, fill=text_light)

    draw.line((80, 145, WIDTH - 80, 145), fill=gold, width=2)

    if not members:
        msg = "No recent members found"
        bbox = draw.textbbox((0, 0), msg, font=name_font)
        draw.text(((WIDTH - (bbox[2]-bbox[0])) // 2, 250), msg, font=name_font, fill=gold)
    else:
        y = 172
        for idx, member in enumerate(members, start=1):
            username = member["username"]
            joined = member["joined"]

            # Member card
            draw_rounded_rectangle(draw, (80, y, WIDTH - 80, y + 55), 12, (18, 18, 18), dark_gold, 2)

            # Rank badge
            draw_rounded_rectangle(draw, (100, y + 11, 140, y + 45), 8, (40, 32, 8), gold, 1)
            rank_text = str(idx)
            bbox = draw.textbbox((0, 0), rank_text, font=rank_font)
            draw.text((120 - (bbox[2]-bbox[0])//2, y + 13), rank_text, font=rank_font, fill=gold)

            # Name
            draw.text((160, y + 9), f"@{username}", font=name_font, fill=text_light)

            # Time
            joined_text = time_ago(joined)
            bbox = draw.textbbox((0, 0), joined_text, font=small_font)
            draw.text((WIDTH - 105 - (bbox[2]-bbox[0]), y + 18), joined_text, font=small_font, fill=muted)

            y += 62

    # Footer
    updated = datetime.now(timezone.utc).strftime("Updated %b %d, %Y • %H:%M UTC")
    bbox = draw.textbbox((0, 0), updated, font=small_font)
    draw.text(((WIDTH - (bbox[2]-bbox[0])) // 2, HEIGHT - 58), updated, font=small_font, fill=muted)

    img.save(OUTPUT_FILE, quality=95)

if __name__ == "__main__":
    generate_board()
