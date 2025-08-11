from PIL import Image, ImageDraw
import random
from typography import draw_wrapped_text
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

def generate_poster(text, output_path):
    params = design_params_from_event(text)
    palette = params["palette"]
    font_min, font_max = params["font_size_range"]
    font_size = random.randint(font_min, font_max)

    bg_color = random.choice(palette)
    img = Image.new("RGB", (WIDTH, HEIGHT), color=bg_color)
    draw = ImageDraw.Draw(img)

    if params["shape"]:
        draw_shape_by_name(draw, params["shape"], palette, WIDTH, HEIGHT)
    else:
        draw_random_shape(draw, palette, WIDTH, HEIGHT)

    # Combine event details into multiline string
    lines = [params["event_name"]]
    if params["date"]:
        lines.append(params["date"])
    if params["location"]:
        lines.append(params["location"])

    poster_text = "\n".join([line for line in lines if line])

    draw_wrapped_text(draw, poster_text, palette, WIDTH, HEIGHT, font_size=font_size)

    img.save(output_path)
