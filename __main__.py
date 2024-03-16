import pygame
import sys
import json
from word_search_generator import WordSearch
import math
# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1200
screen_height = 800

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
grey = (128, 128, 128)
red = (255, 0, 0)
blue = (0, 0, 255)  # Color for highlighting selected cell

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Word Search Game")

# Puzzle data (Assuming this is the JSON you've provided)
words = ["python", "java", "kotlin", "swift", "javascript"]
words = ", ".join(words)# print(len(input_letters))
# print(matrix_size)
puzzle_data = WordSearch(words, size=10).json
puzzle_data = json.loads(puzzle_data)
# print(type(puzzle_data))

# Extract puzzle grid and words
grid = puzzle_data['puzzle']
words = puzzle_data['words']

# Font for rendering text
font = pygame.font.Font(None, 36)
# Variables for selected cell

# Function to draw the grid
def draw_grid(grid, hover_cell):
    block_size = 40  # Size of grid block
    for y, row in enumerate(grid):
        for x, letter in enumerate(row):
            rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
            # Highlight cell if hovered over
            if hover_cell == (y, x):
                pygame.draw.rect(screen, blue, rect)
            else:
                pygame.draw.rect(screen, grey, rect, 1)
            text = font.render(letter.lower(), True, white if hover_cell == (y, x) else black)
            screen.blit(text, rect.topleft + pygame.Vector2(10, 5))

# Function to draw the words list
def draw_words(words):
    start_x = 600  # Starting X position for the words list
    start_y = 100  # Starting Y position for the words list
    for word in words:
        text = font.render(word, True, red)
        screen.blit(text, (start_x, start_y))
        start_y += 40  # Move down for the next word

# Function to get cell from mouse position
def get_cell_from_mouse_pos(pos):
    x, y = pos
    row = y // 40  # Assuming block_size = 40
    col = x // 40
    if row < len(grid) and col < len(grid[0]):
        return (row, col)
    return None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update hover cell based on mouse position
    hover_cell = get_cell_from_mouse_pos(pygame.mouse.get_pos())

    screen.fill(white)

    # Draw the word search grid with the current hover cell
    draw_grid(grid, hover_cell)
    # Draw the words list
    draw_words(words)

    pygame.display.flip()

pygame.quit()