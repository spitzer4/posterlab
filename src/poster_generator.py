from PIL import Image, ImageDraw
import random
from typography import draw_text
from shapes import draw_shape_by_name, draw_random_shape
from textblob import TextBlob

WIDTH, HEIGHT = 1080, 1350  # Portrait poster size

# Define palettes for different sentiments
WARM_PALETTE = [(239, 71, 111), (255, 209, 102), (255, 255, 255)]
COOL_PALETTE = [(20, 33, 61), (0, 48, 73), (200, 200, 200)]
NEUTRAL_PALETTE = [(200, 200, 200), (100, 100, 100), (150, 150, 150)]

KEYWORD_SHAPES = {
    "love": "heart",
    "nature": "leaf",
    "storm": "circle",
    # Add more keyword-to-shape mappings as you like
}

def analyze_text(text):
    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity  # Range from -1 to 1
    length = len(text)
    words = text.lower().split()

    shape = None
    for word in words:
        if word in KEYWORD_SHAPES:
            shape = KEYWORD_SHAPES[word]
            break

    return {
        "sentiment": sentiment,
        "length": length,
        "shape": shape,
    }

def design_params_from_text(text):
    analysis = analyze_text(text)

    # Select palette based on sentiment
    if analysis["sentiment"] > 0.1:
        palette = WARM_PALETTE
    elif analysis["sentiment"] < -0.1:
        palette = COOL_PALETTE
    else:
        palette = NEUTRAL_PALETTE

    # Determine font size range based on text length
    if analysis["length"] < 10:
        font_size_range = (150, 200)
    elif analysis["length"] < 30:
        font_size_range = (80, 140)
    else:
        font_size_range = (40, 80)

    return {
        "palette": palette,
        "font_size_range": font_size_range,
        "shape": analysis["shape"],
    }

def generate_poster(text, output_path):
    params = design_params_from_text(text)
    palette = params["palette"]
    font_min, font_max = params["font_size_range"]

    # Create canvas with a random background color from the palette
    bg_color = random.choice(palette)
    img = Image.new('RGB', (WIDTH, HEIGHT), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Draw shape based on detected keyword or random if none found
    if params["shape"]:
        draw_shape_by_name(draw, params["shape"], palette, WIDTH, HEIGHT)
    else:
        draw_random_shape(draw, palette, WIDTH, HEIGHT)

    # Draw the text using dynamic font size
    font_size = random.randint(font_min, font_max)
    draw_text(draw, text, palette, WIDTH, HEIGHT, font_size=font_size)

    # Save the poster
    img.save(output_path)
