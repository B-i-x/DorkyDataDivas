import pygame
import sys
import json
from word_search_generator import WordSearch
import math

from util.colors import Color

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1200
screen_height = 800

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Word Search Game")

# Puzzle data
words = ["python", "java", "kotlin", "swift", "javascript"]
words = ", ".join(words)
puzzle_data = WordSearch(words, size=10).json
puzzle_data = json.loads(puzzle_data)

# Extract puzzle grid and words
grid = puzzle_data['puzzle']
words = puzzle_data['words']

# Font for rendering text
font = pygame.font.Font(None, 36)

# List to keep track of selected cells
selected_cells = []

# Function to draw the grid
def draw_grid(grid, hover_cell):
    block_size = 40  # Size of grid block
    for y, row in enumerate(grid):
        for x, letter in enumerate(row):
            rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
            # Check if cell is selected or hovered over
            if (y, x) in selected_cells or hover_cell == (y, x):
                pygame.draw.rect(screen, Color.BLUE.value, rect)
                text_color = Color.WHITE.value
            else:
                pygame.draw.rect(screen, Color.GREY.value, rect, 1)
                text_color = Color.BLACK.value
            text_surface = font.render(letter.lower(), True, text_color)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)

# Function to draw the words list
def draw_words(words):
    start_x = 600
    start_y = 100
    for word in words:
        text = font.render(word, True, Color.RED.value)
        screen.blit(text, (start_x, start_y))
        start_y += 40

# Function to get cell from mouse position
def get_cell_from_mouse_pos(pos):
    x, y = pos
    row = y // 40
    col = x // 40
    if row < len(grid) and col < len(grid[0]):
        return (row, col)
    return None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Add clicked cell to selected cells list
            cell = get_cell_from_mouse_pos(pygame.mouse.get_pos())
            if cell and cell not in selected_cells:
                selected_cells.append(cell)

    # Get current hover cell
    hover_cell = get_cell_from_mouse_pos(pygame.mouse.get_pos())

    screen.fill(Color.WHITE.value)

    # Draw the word search grid and words list
    draw_grid(grid, hover_cell)
    draw_words(words)

    pygame.display.flip()

pygame.quit()
