import enum
import pygame

import random

last_color_index = -1

class Color(enum.Enum):
    BLACK = pygame.Color(23, 29, 28)
    # WHITE = pygame.Color('white')
    GREY = pygame.Color(222, 222, 224)  # Custom color
    RED = pygame.Color('red')
    BLUE = pygame.Color('blue')
    GREEN = pygame.Color('green')

    MAIN_BACKGROUND_COLOR = pygame.Color(246, 239, 238)
    HOVER_CELL_COLOR = pygame.Color(192, 192, 192)  #
    CORRECT_WORD_COLOR = pygame.Color(0, 78, 152)  # 

def generate_colors_for_words(words: list) -> dict:
    colors = {}
    for word in words:
        colors[word] = generate_pastel_color()
    return colors

def generate_pastel_color(alpha=128):
    global last_color_index
    
    # Define base colors emphasizing red, green, and blue
    base_colors = [
        (200, random.randint(100, 150), random.randint(100, 150)),  # Red emphasis
        (random.randint(100, 150), 200, random.randint(100, 150)),  # Green emphasis
        (random.randint(100, 150), random.randint(100, 150), 200)   # Blue emphasis
    ]
    
    # Cycle through the base colors to ensure variation
    last_color_index = (last_color_index + 1) % len(base_colors)
    r, g, b = base_colors[last_color_index]
    
    # Lighten the chosen base color
    r = min(r + random.randint(30, 55), 255)
    g = min(g + random.randint(30, 55), 255)
    b = min(b + random.randint(30, 55), 255)
    
    # Return the pastel color with alpha transparency
    return pygame.Color(r, g, b, alpha)

# if __name__ == "__main__":
#     print(generate_pastel_color())


