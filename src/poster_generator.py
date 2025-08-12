from PIL import Image, ImageDraw
import random
from typography import draw_text_line, get_accessible_text_color, FONT_DIR
from shapes import draw_shape_by_name, draw_random_shape
from event_extractor import extract_event_info

WIDTH, HEIGHT = 1080, 1350

WARM_PALETTE = [(239, 71, 111), (255, 209, 102), (255, 255, 255)]
COOL_PALETTE = [(20, 33, 61), (0, 48, 73), (200, 200, 200)]
NEUTRAL_PALETTE = [(200, 200, 200), (100, 100, 100), (150, 150, 150)]

LOCATION_SHAPES = {
    "park": "leaf",
    "beach": "circle",
    "hall": "rectangle",
    "stadium": "circle",
}

def design_params_from_event(text):
    info = extract_event_info(text)

    palette = WARM_PALETTE if info["date"] else NEUTRAL_PALETTE

    name_len = len(info["event_name"])
    if name_len < 10:
        font_size_range = (150, 200)
    elif name_len < 30:
        font_size_range = (80, 140)
    else:
        font_size_range = (40, 80)

    shape = None
    if info["location"]:
        loc = info["location"].lower()
        for key in LOCATION_SHAPES:
            if key in loc:
                shape = LOCATION_SHAPES[key]
                break

    return {
        "palette": palette,
        "font_size_range": font_size_range,
        "shape": shape,
        "event_name": info["event_name"],
        "date": info["date"],
        "location": info["location"],
    }

def generate_poster(text, output_path, details=None):
    params = design_params_from_event(text)
    palette = params["palette"]

    bg_color = random.choice(palette)
    img = Image.new("RGB", (WIDTH, HEIGHT), color=bg_color)
    draw = ImageDraw.Draw(img)
    
	# Text colors for accessibility
    text_color = get_accessible_text_color(bg_color)

    # Font paths for weights - adjust if you have multiple font files downloaded
    font_paths = {
        "bold": FONT_DIR / "Roboto-Bold.ttf",
        "medium": FONT_DIR / "Roboto-Medium.ttf",
        "regular": FONT_DIR / "Roboto-Regular.ttf",
        "light": FONT_DIR / "Roboto-Light.ttf",
    }

    # Positions
    EVENT_Y = int(HEIGHT * 0.2)
    DATE_Y = EVENT_Y + 110
    LOCATION_Y = int(HEIGHT * 0.8)
    DETAILS_Y = HEIGHT - 60
    CENTER_X = WIDTH // 2
    LEFT_MARGIN = 60

    # Draw Event Name (largest)
    event_name = params["event_name"] or ""
    event_font_size = 70
    draw_text_line(draw, event_name, (CENTER_X, EVENT_Y), font_paths["bold"], event_font_size, text_color, anchor="mm")

    # Draw Date/Time (medium)
    date = params["date"] or ""
    date_font_size = 32
    draw_text_line(draw, date, (CENTER_X, DATE_Y), font_paths["medium"], date_font_size, text_color, anchor="mm")

    # Draw Location (smaller)
    location = params["location"] or ""
    location_font_size = 24
    draw_text_line(draw, location, (CENTER_X, LOCATION_Y), font_paths["regular"], location_font_size, text_color, anchor="mm")

    # Draw Additional Details (smallest, if any)
    if details:
        details_font_size = 14
        draw_text_line(draw, details, (LEFT_MARGIN, DETAILS_Y), font_paths["light"], details_font_size, text_color, anchor="lm")

    img.save(output_path)
