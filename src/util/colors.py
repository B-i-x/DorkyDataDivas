import enum
import pygame

import random

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
    # Generate even lighter pastel colors by narrowing the range closer to 255
    r = random.randint(150, 220)
    g = random.randint(150, 255)
    b = random.randint(150, 255)
    # Add opacity (alpha) to the color
    return pygame.Color(r, g, b, alpha)


# if __name__ == "__main__":
#     print(generate_pastel_color())


