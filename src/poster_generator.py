from PIL import Image, ImageDraw, ImageFont
import random
import math
from typing import List, Tuple, Optional
from event_extractor import extract_event_info

WIDTH, HEIGHT = 1080, 1350

def get_text_dimensions(text: str, font: ImageFont.FreeTypeFont) -> Tuple[int, int]:
    """Get accurate text dimensions using textbbox."""
    # Create temporary image to measure text
    temp_img = Image.new('RGB', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # Get bounding box - this gives us the actual text dimensions
    bbox = temp_draw.textbbox((0, 0), text.upper(), font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    
    return width, height

def get_rotated_bbox(width: int, height: int, rotation: float) -> Tuple[int, int]:
    """Calculate bounding box dimensions after rotation."""
    if rotation == 0:
        return width, height
    
    # Convert to radians
    angle = math.radians(abs(rotation))
    
    # Calculate rotated dimensions using rotation matrix
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    
    new_width = int(abs(width * cos_a) + abs(height * sin_a))
    new_height = int(abs(width * sin_a) + abs(height * cos_a))
    
    return new_width, new_height

def find_non_overlapping_position(
    text_width: int, 
    text_height: int, 
    preferred_x: int, 
    preferred_y: int,
    occupied_areas: List[Tuple[int, int, int, int]],
    canvas_width: int = WIDTH,
    canvas_height: int = HEIGHT,
    margin: int = 20
) -> Tuple[int, int]:
    """Find a position that doesn't overlap with existing text."""
    
    def rect_overlaps(x1: int, y1: int, w1: int, h1: int, 
                     x2: int, y2: int, x2_end: int, y2_end: int) -> bool:
        """Check if two rectangles overlap with margin."""
        return not (x1 + w1 + margin <= x2 or 
                   x1 >= x2_end + margin or 
                   y1 + h1 + margin <= y2 or 
                   y1 >= y2_end + margin)
    
    def position_is_valid(x: int, y: int) -> bool:
        """Check if position is valid (in bounds and no overlaps)."""
        # Check canvas boundaries
        if (x < margin or y < margin or 
            x + text_width > canvas_width - margin or 
            y + text_height > canvas_height - margin):
            return False
        
        # Check overlaps with existing text
        for occupied in occupied_areas:
            if rect_overlaps(x, y, text_width, text_height, *occupied):
                return False
        
        return True
    
    # Try preferred position first
    if position_is_valid(preferred_x, preferred_y):
        return preferred_x, preferred_y
    
    # Spiral search around preferred position
    max_radius = min(canvas_width, canvas_height) // 2
    
    for radius in range(50, max_radius, 30):
        # Try positions in a circle around preferred position
        for angle_deg in range(0, 360, 15):
            angle_rad = math.radians(angle_deg)
            x = int(preferred_x + radius * math.cos(angle_rad))
            y = int(preferred_y + radius * math.sin(angle_rad))
            
            if position_is_valid(x, y):
                return x, y
    
    # Fallback: try grid positions
    grid_size = 100
    for y in range(margin, canvas_height - text_height - margin, grid_size):
        for x in range(margin, canvas_width - text_width - margin, grid_size):
            if position_is_valid(x, y):
                return x, y
    
    # Last resort: clamp to bounds and hope for the best
    x = max(margin, min(preferred_x, canvas_width - text_width - margin))
    y = max(margin, min(preferred_y, canvas_height - text_height - margin))
    return x, y

# def draw_event_text(
#     base_img: Image.Image,
#     text: str,
#     preferred_position: Tuple[int, int],
#     font_path,
#     size: int,
#     color: Tuple[int, int, int],
#     stretch_factor: float = 1.0,
#     rotation: float = 0,
#     occupied_areas: Optional[List] = None
# ) -> Optional[Tuple[int, int, int, int]]:
#     """Draw text with improved positioning and overlap prevention."""
    
#     if occupied_areas is None:
#         occupied_areas = []
    
#     try:
#         # Create font with stretch factor
#         font = ImageFont.truetype(str(font_path), int(size * stretch_factor))
        
#         # Get text dimensions
#         text_width, text_height = get_text_dimensions(text, font)
        
#         # Adjust dimensions for rotation
#         if rotation != 0:
#             text_width, text_height = get_rotated_bbox(text_width, text_height, rotation)
        
#         # Find non-overlapping position
#         final_x, final_y = find_non_overlapping_position(
#             text_width, text_height, 
#             preferred_position[0], preferred_position[1],
#             occupied_areas
#         )
        
#         # Draw the text
#         if rotation == 0:
#             # Simple case - no rotation
#             draw = ImageDraw.Draw(base_img)
#             draw.text((final_x, final_y), text.upper(), font=font, fill=color)
#         else:
#             # Create temporary image for rotation
#             temp_img = Image.new("RGBA", (text_width + 100, text_height + 100), (0, 0, 0, 0))
#             temp_draw = ImageDraw.Draw(temp_img)
            
#             # Draw text in center of temp image
#             temp_x = (temp_img.width - text_width) // 2
#             temp_y = (temp_img.height - text_height) // 2
#             temp_draw.text((temp_x, temp_y), text.upper(), font=font, fill=color)
            
#             # Rotate and paste
#             rotated = temp_img.rotate(rotation, expand=True)
            
#             # Calculate paste position (center the rotated text on final position)
#             paste_x = final_x - (rotated.width - text_width) // 2
#             paste_y = final_y - (rotated.height - text_height) // 2
            
#             # Paste with alpha channel for proper blending
#             if rotated.mode == 'RGBA':
#                 base_img.paste(rotated, (paste_x, paste_y), rotated)
#             else:
#                 base_img.paste(rotated, (paste_x, paste_y))
        
#         # Return bounding box for tracking
#         return (final_x, final_y, final_x + text_width, final_y + text_height)
        
#     except Exception as e:
#         print(f"Error drawing text '{text}': {e}")
#         return None

def draw_event_text(
    base_img: Image.Image,
    text: str,
    preferred_position: Tuple[int, int],
    font_path,
    size: int,
    color: Tuple[int, int, int],
    stretch_factor: float = 1.0,
    rotation: float = 0,
    occupied_areas: Optional[List] = None,
    min_size: int = 20
) -> Optional[Tuple[int, int, int, int]]:
    """Draw text with dynamic resizing to avoid overflow and overlaps."""

    if occupied_areas is None:
        occupied_areas = []

    current_size = size

    while current_size >= min_size:
        try:
            font = ImageFont.truetype(str(font_path), int(current_size * stretch_factor))

            text_width, text_height = get_text_dimensions(text, font)
            if rotation != 0:
                text_width, text_height = get_rotated_bbox(text_width, text_height, rotation)

            # Check if text fits inside canvas bounds
            if (preferred_position[0] + text_width > base_img.width or
                preferred_position[1] + text_height > base_img.height):
                current_size -= 5
                continue

            # Check overlap with existing areas
            overlaps = False
            for (ox1, oy1, ox2, oy2) in occupied_areas:
                if not (preferred_position[0] + text_width < ox1 or
                        preferred_position[0] > ox2 or
                        preferred_position[1] + text_height < oy1 or
                        preferred_position[1] > oy2):
                    overlaps = True
                    break
            if overlaps:
                current_size -= 5
                continue

            # Passed checks, draw the text (you can reuse your existing drawing logic here)
            draw = ImageDraw.Draw(base_img)
            if rotation == 0:
                draw.text(preferred_position, text.upper(), font=font, fill=color)
            else:
                # Same temp_img + rotate + paste logic as before
                temp_img = Image.new("RGBA", (text_width + 100, text_height + 100), (0, 0, 0, 0))
                temp_draw = ImageDraw.Draw(temp_img)
                temp_x = (temp_img.width - text_width) // 2
                temp_y = (temp_img.height - text_height) // 2
                temp_draw.text((temp_x, temp_y), text.upper(), font=font, fill=color)
                rotated = temp_img.rotate(rotation, expand=True)
                paste_x = preferred_position[0] - (rotated.width - text_width) // 2
                paste_y = preferred_position[1] - (rotated.height - text_height) // 2
                base_img.paste(rotated, (paste_x, paste_y), rotated)

            return (preferred_position[0], preferred_position[1],
                    preferred_position[0] + text_width, preferred_position[1] + text_height)

        except Exception as e:
            print(f"Error drawing text '{text}' at size {current_size}: {e}")
            current_size -= 5

    print(f"Could not fit text '{text}' even at minimum size {min_size}")
    return None

def apply_layout(base_img, event_name, date, location, font_path, colors):
    """Apply layout with improved text placement."""
    bg_color, text_color, accent_color = colors
    occupied = []

    # Event name - largest, most prominent
    bbox = draw_event_text(
        base_img, event_name,
        preferred_position=(random.randint(50, 400), random.randint(50, 400)),
        font_path=font_path, 
        size=min(220, max(120, 2000 // len(event_name))),  # Adaptive sizing
        color=text_color,
        stretch_factor=random.uniform(0.8, 1.6),
        rotation=random.choice([0, 0, 0, 15, -15, 90, -90]),  # Favor horizontal
        occupied_areas=occupied
    )
    if bbox:
        occupied.append(bbox)

    # Date - secondary importance
    bbox = draw_event_text(
        base_img, date,
        preferred_position=(random.randint(50, 600), random.randint(600, 900)),
        font_path=font_path, 
        size=min(100, max(60, 800 // len(date))),
        color=accent_color,
        rotation=random.choice([0, 0, 90, -90]),
        occupied_areas=occupied
    )
    if bbox:
        occupied.append(bbox)

    # Location - supporting text
    bbox = draw_event_text(
        base_img, location,
        preferred_position=(random.randint(50, 500), random.randint(1000, 1200)),
        font_path=font_path, 
        size=min(120, max(40, 1000 // len(location))),
        color=text_color,
        stretch_factor=random.uniform(0.9, 1.3),
        rotation=random.choice([0, 0, 0, 180]),  # Favor readable orientations
        occupied_areas=occupied
    )
    if bbox:
        occupied.append(bbox)

# Updated generate_poster function
def generate_poster(text, output_path, font_path="data/fonts/Roboto-Regular.ttf"):
    """Generate poster with improved text placement."""
    event_info = extract_event_info(text)
    event_name = event_info.get("event_name", "Event Name")
    date = event_info.get("date", "Date")
    location = event_info.get("location", "Location")

    # Create base image with background
    palette = [(255, 100, 100), (50, 50, 50), (255, 255, 100)]  # Sample palette
    bg_color = palette[0]
    text_color = (255, 255, 255)  # White for contrast
    accent_color = palette[2]

    img = Image.new("RGB", (WIDTH, HEIGHT), color=bg_color)
    apply_layout(img, event_name, date, location, font_path, (bg_color, text_color, accent_color))

    img.save(output_path)
