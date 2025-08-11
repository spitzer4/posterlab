import os
import requests
from pathlib import Path
from PIL import ImageFont, ImageDraw
import random
import textwrap
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env into environment

API_KEY = os.getenv("GOOGLE_FONTS_API_KEY")

if not API_KEY:
    raise ValueError("Google Fonts API key not found. Please set GOOGLE_FONTS_API_KEY in .env")

FONT_FAMILY = "Roboto"
FONT_VARIANT = "regular"
FONT_DIR = Path("data/fonts")
FONT_PATH = FONT_DIR / f"{FONT_FAMILY}-{FONT_VARIANT}.ttf"

def get_font_url(api_key, family, variant):
    url = f"https://www.googleapis.com/webfonts/v1/webfonts?key={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    fonts = response.json().get("items", [])

    for font in fonts:
        if font["family"].lower() == family.lower():
            files = font.get("files", {})
            if variant in files:
                return files[variant]
    raise ValueError(f"Font '{family}' with variant '{variant}' not found")

def download_font():
    if not FONT_DIR.exists():
        FONT_DIR.mkdir(parents=True)
    if not FONT_PATH.is_file():
        print(f"Downloading font '{FONT_FAMILY} {FONT_VARIANT}' from Google Fonts API...")
        font_url = get_font_url(API_KEY, FONT_FAMILY, FONT_VARIANT)
        r = requests.get(font_url)
        r.raise_for_status()
        with open(FONT_PATH, "wb") as f:
            f.write(r.content)
        print("Font downloaded successfully.")
    else:
        print("Font already downloaded.")

def get_contrast_color(bg_color):
    r, g, b = bg_color
    luminance = (0.299*r + 0.587*g + 0.114*b)/255
    return (0, 0, 0) if luminance > 0.5 else (255, 255, 255)

def draw_wrapped_text(draw, text, palette, width, height, font_size=None, max_width_ratio=0.8, line_spacing=10):
    """
    Draw wrapped multiline text inside width*max_width_ratio area with good contrast
    """
    download_font()

    if font_size is None:
        font_size = random.randint(80, 200)

    font = ImageFont.truetype(str(FONT_PATH), font_size)
    max_text_width = width * max_width_ratio
    text_color = get_contrast_color(palette[0])  # Choose text color contrasting first palette color

    # Wrap text: estimate max chars per line by average char width
    avg_char_width = font.getlength("a")  # Pillow >=8.0, else approximate
    max_chars_per_line = max(10, int(max_text_width / avg_char_width))

    lines = textwrap.wrap(text, width=max_chars_per_line)
    # Calculate total height for all lines
    line_heights = [font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines]
    total_text_height = sum(line_heights) + line_spacing * (len(lines) -1)

    # Start vertically centered
    y = (height - total_text_height) // 2

    for line, line_height in zip(lines, line_heights):
        bbox = draw.textbbox((0,0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2  # center horizontally
        draw.text((x, y), line, font=font, fill=text_color)
        y += line_height + line_spacing
