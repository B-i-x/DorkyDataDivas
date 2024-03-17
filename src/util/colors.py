import enum
import pygame

class Color(enum.Enum):
    BLACK = pygame.Color(23, 29, 28)
    WHITE = pygame.Color('white')
    GREY = pygame.Color(222, 222, 224)  # Custom color
    RED = pygame.Color('red')
    BLUE = pygame.Color('blue')
    GREEN = pygame.Color('green')

    MAIN_BACKGROUND_COLOR = pygame.Color(235, 235, 235)
    HOVER_CELL_COLOR = pygame.Color(192, 192, 192)  #
    CORRECT_WORD_COLOR = pygame.Color(0, 78, 152)  # 
