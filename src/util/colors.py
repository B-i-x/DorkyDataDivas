import enum
import pygame

class Color(enum.Enum):
    BLACK = pygame.Color('black')
    WHITE = pygame.Color('white')
    GREY = pygame.Color(222, 222, 224)  # Custom color
    RED = pygame.Color('red')
    BLUE = pygame.Color('blue')
    GREEN = pygame.Color('green')