import random

PALETTES = [
    [(255, 255, 255), (0, 0, 0), (255, 0, 255)],
	[(0, 0, 0), (255, 255, 255), (0, 255, 255)],
	[(255, 255, 255), (0, 0, 0), (255, 211, 0)]
]

def get_random_palette():
    return random.choice(PALETTES)
