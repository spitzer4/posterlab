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
FONT_DIR = Path("data/fonts")

# Font paths for weights
font_paths = {
	"bold": FONT_DIR / "Roboto-Bold.ttf",
	"medium": FONT_DIR / "Roboto-Medium.ttf",
	"regular": FONT_DIR / "Roboto-Regular.ttf",
	"light": FONT_DIR / "Roboto-Light.ttf",
}

def get_font_url(api_key, family, variant):
    url = f"https://www.googleapis.com/webfonts/v1/webfonts?key={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    fonts = response.json().get("items", [])
    for font in fonts:
        if font["family"].lower() == family.lower():
            files = font.get("files", {})
            # Google Fonts uses variant keys like 'regular', 'italic', '700', etc.
            # Map variants to keys:
            variant_key_map = {
                "regular": "regular",
                "bold": "700",
                "medium": "500",
                "light": "300",
            }
            key = variant_key_map.get(variant)
            if key and key in files:
                return files[key]
    raise ValueError(f"Font '{family}' variant '{variant}' not found in Google Fonts API.")

def download_all_fonts():
    if not FONT_DIR.exists():
        FONT_DIR.mkdir(parents=True)
    for variant, path in font_paths.items():
        if not path.is_file():
            print(f"Downloading {FONT_FAMILY} {variant} font...")
            font_url = get_font_url(API_KEY, FONT_FAMILY, variant)
            r = requests.get(font_url)
            r.raise_for_status()
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"Downloaded {variant} font to {path}")
        else:
            print(f"{variant} font already downloaded.")
            
def get_font(variant="regular", size=40):
    """
    Returns a PIL ImageFont instance for given variant and size.
    Downloads fonts if missing.
    """
    if variant not in font_paths:
        variant = "regular"
    download_all_fonts()  # Ensures fonts are downloaded (idempotent)
    return ImageFont.truetype(str(font_paths[variant]), size)

def relative_luminance(rgb):
    def channel_lum(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * channel_lum(r) + 0.7152 * channel_lum(g) + 0.0722 * channel_lum(b)

def contrast_ratio(c1, c2):
    L1 = relative_luminance(c1)
    L2 = relative_luminance(c2)
    lighter = max(L1, L2)
    darker = min(L1, L2)
    return (lighter + 0.05) / (darker + 0.05)

def get_accessible_text_color(bg_color, candidates=[(0,0,0), (255,255,255)]):    
    # Try black or white text for sufficient contrast (4.5:1)
    for color in candidates:
        if contrast_ratio(bg_color, color) >= 4.5:
            return color
    # If neither passes, return color with highest contrast anyway
    return max(candidates, key=lambda c: contrast_ratio(bg_color, c))

def draw_text(draw, text, bg_color, width, height, font_size=None, max_width_ratio=0.8, line_spacing=10, variant="regular"):
    """
    Draw wrapped multiline text with accessible contrast color.
    """
    if font_size is None:
        font_size = random.randint(80, 200)

    font = get_font(variant, font_size)
    max_text_width = width * max_width_ratio

    # Estimate max chars per line by average char width
    avg_char_width = font.getlength("a")  # Pillow >=8.0
    max_chars_per_line = max(10, int(max_text_width / avg_char_width))

    lines = textwrap.wrap(text, width=max_chars_per_line)

    # Calculate total height
    line_heights = [font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines]
    total_text_height = sum(line_heights) + line_spacing * (len(lines) - 1)

    # Vertical start (centered)
    y = (height - total_text_height) // 2

    text_color = get_accessible_text_color(bg_color)

    for line, line_height in zip(lines, line_heights):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2  # center horizontally
        draw.text((x, y), line, font=font, fill=text_color)
        y += line_height + line_spacing

def draw_text_line(draw, text, position, font_path, font_size, fill, anchor="lt"):
    font = ImageFont.truetype(str(font_path), font_size)
    draw.text(position, text, font=font, fill=fill, anchor=anchor)
        