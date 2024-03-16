import enum
import pygame

class Color(enum.Enum):
    BLACK = pygame.Color('black')
    WHITE = pygame.Color('white')
    GREY = pygame.Color(128, 128, 128)  # Custom color
    RED = pygame.Color('red')
    BLUE = pygame.Color('blue')