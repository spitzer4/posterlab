from PIL import Image, ImageDraw
import random
from typography import draw_text_line, get_accessible_text_color, FONT_DIR
from event_extractor import extract_event_info
from palettes import get_random_palette

WIDTH, HEIGHT = 1080, 1350

def draw_event_text(base_img, text, position, font_path, size, color, stretch_factor=1.0, rotation=0):
    from PIL import ImageDraw, ImageFont

    font = ImageFont.truetype(str(font_path), int(size * stretch_factor))

    # Create transparent image for rotated text
    temp_img = Image.new("RGB", base_img.size, (0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    temp_draw.text(position, text.upper(), font=font, fill=color)

    # Rotate text layer
    rotated = temp_img.rotate(rotation, expand=1)


def apply_layout(base_img, event_name, date, location, font_path, colors):
    bg_color, text_color, accent_color = colors

    # Main event name - oversized, possibly rotated
    main_rotation = random.choice([0, 0, 90, -90, 15, -15])
    main_stretch = random.uniform(0.8, 1.8)
    main_pos = (random.randint(50, 300), random.randint(50, 300))
    draw_event_text(base_img, event_name, main_pos, font_path, size=220,
                    color=text_color, stretch_factor=main_stretch, rotation=main_rotation)

    # Date - small but high contrast accent
    date_pos = (random.randint(50, 400), random.randint(600, 1000))
    draw_event_text(base_img, date, date_pos, font_path, size=100,
                    color=accent_color, stretch_factor=1.0, rotation=random.choice([0, 90, -90]))

    # Location - maybe rotated opposite to main
    loc_pos = (random.randint(50, 500), random.randint(1000, 1300))
    draw_event_text(base_img, location, loc_pos, font_path, size=120,
                    color=text_color, stretch_factor=random.uniform(0.9, 1.5), rotation=random.choice([0, 90, -90, 180]))

def generate_poster(text, output_path, font_path=FONT_DIR / "Roboto-Bold.ttf"):
    # Extract event info
    event_info = extract_event_info(text)
    event_name = event_info.get("event_name", "Untitled Event")
    date = event_info.get("date", "Date TBD")	
    location = event_info.get("location", "Location TBD")

    # Get color palette and accessible text colors
    palette = get_random_palette()
    bg_color = palette[0]  # Use first as background
    text_color = get_accessible_text_color(bg_color)
    accent_color = palette[2] if len(palette) > 2 else text_color

    # Create base image and draw object
    img = Image.new("RGB", (WIDTH, HEIGHT), color=bg_color)
    
    apply_layout(img, event_name, date, location, font_path, (bg_color, text_color, accent_color))

    # Optionally add more structured text (if you want your previous draw_text_line calls)
    # For that you need an ImageDraw object:
    draw = ImageDraw.Draw(img)

    # Positions for structured text
    CENTER_X = WIDTH // 2
    EVENT_Y = int(HEIGHT * 0.2)
    DATE_Y = EVENT_Y + 110
    LOCATION_Y = int(HEIGHT * 0.8)

    # Font sizes
    event_font_size = 70
    date_font_size = 32
    location_font_size = 24

    # Draw clean lines of text centered (optional, can comment out if you want only generative layout)
    draw_text_line(draw, event_name, (CENTER_X, EVENT_Y), font_path, event_font_size, text_color, anchor="mm")
    draw_text_line(draw, date, (CENTER_X, DATE_Y), font_path, date_font_size, text_color, anchor="mm")
    draw_text_line(draw, location, (CENTER_X, LOCATION_Y), font_path, location_font_size, text_color, anchor="mm")

    # Save final poster
    img.save(output_path)
