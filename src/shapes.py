import random

def draw_random_shape(draw, palette, width, height):
    shape_type = random.choice(["circle", "rectangle", "line"])
    color = random.choice(palette)
    
    if shape_type == "circle":
        r = random.randint(50, 300)
        x, y = random.randint(0, width), random.randint(0, height)
        draw.ellipse((x-r, y-r, x+r, y+r), fill=color)
    
    elif shape_type == "rectangle":
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(x1, width), random.randint(y1, height)
        draw.rectangle((x1, y1, x2, y2), fill=color)
    
    elif shape_type == "line":
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=color, width=random.randint(5, 20))
        
		
def draw_shape_by_name(draw, shape_name, palette, width, height):
    color = random.choice(palette)
    if shape_name == "heart":
        # Simplified heart shape using polygons or bezier curves (can be refined)
        # For now, draw a red circle as a placeholder:
        cx, cy = width // 2, height // 2
        r = 150
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color)
    elif shape_name == "leaf":
        # Draw a green ellipse or polygon representing a leaf
        cx, cy = width // 2, height // 2
        draw.ellipse((cx - 120, cy - 60, cx + 120, cy + 60), fill=color)
    elif shape_name == "circle":
        cx, cy = width // 2, height // 2
        r = 200
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color)
    else:
        # fallback random shape
        from shapes import draw_random_shape
        draw_random_shape(draw, palette, width, height)

