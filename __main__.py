import pygame
import sys
from word_search_generator import WordSearch
# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Word Search Game")

# Word search setup
words = "python, pygame, puzzle, game, word"
ws = WordSearch(words)

print(ws.json)
# Font for rendering text
font = pygame.font.Font(None, 36)

def draw_grid(words, grid):
    block_size = 40 # Size of grid block
    for y, row in enumerate(grid):
        for x, letter in enumerate(row):
            rect = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
            pygame.draw.rect(screen, white, rect, 1)
            text = font.render(letter.upper(), True, white)
            screen.blit(text, rect.topleft + pygame.Vector2(10, 5))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)

    # Draw the word search grid
    draw_grid(words, ws.grid)

    pygame.display.flip()

pygame.quit()
