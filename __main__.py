import pygame
import sys
import json
from word_search_generator import WordSearch

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1200
screen_height = 800

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Word Search Game")

# Puzzle data (Assuming this is the JSON you've provided)
puzzle_data = WordSearch("test, asdasd, pip").json
puzzle_data = json.loads(puzzle_data)
# print(type(puzzle_data))

# Extract puzzle grid and words
grid = puzzle_data['puzzle']
words = puzzle_data['words']

# Font for rendering text
font = pygame.font.Font(None, 36)

def draw_grid(grid):
    block_size = 40 # Size of grid block
    for y, row in enumerate(grid):
        for x, letter in enumerate(row):
            rect = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
            pygame.draw.rect(screen, white, rect, 1)
            text = font.render(letter.upper(), True, white)
            screen.blit(text, rect.topleft + pygame.Vector2(10, 5))

def draw_words(words):
    start_x = 600 # Starting X position for the words list
    start_y = 100 # Starting Y position for the words list
    for word in words:
        text = font.render(word, True, red)
        screen.blit(text, (start_x, start_y))
        start_y += 40 # Move down for the next word

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)

    # Draw the word search grid
    draw_grid(grid)
    # Draw the words list
    draw_words(words)

    pygame.display.flip()

pygame.quit()