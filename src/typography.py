import os
import requests
from pathlib import Path
from PIL import ImageFont
import random

# Config
API_KEY = "AIzaSyBRQy681PpRQihZbZFOLdhFEaxJwH5qpMM"
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

def draw_text(draw, text, palette, width, height, font_size=None):
    download_font()

    if font_size is None:
        font_size = random.randint(80, 200)

    font = ImageFont.truetype(str(FONT_PATH), font_size)

    # Get bounding box of the text
    bbox = draw.textbbox((0, 0), text, font=font)  # returns (x0, y0, x1, y1)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = random.randint(0, max(0, width - text_width))
    y = random.randint(0, max(0, height - text_height))

    text_color = random.choice(palette)
    draw.text((x, y), text, font=font, fill=text_color)
