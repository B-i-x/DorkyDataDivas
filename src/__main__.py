import pygame
import sys
import json
from word_search_generator import WordSearch
import math

from util.colors import Color
from gemini.ai import words_related_to_theme

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1200
screen_height = 800

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Word Search Game")

# Puzzle data
words = words_related_to_theme("programming")
puzzle_data = WordSearch(words, size=6).json
print(puzzle_data)
puzzle_data = json.loads(puzzle_data)

# Extract puzzle grid and words
grid = puzzle_data['puzzle']
words = puzzle_data['words']
print(words)
# Font for rendering text
font = pygame.font.Font(None, 36)

# Keep track of the start cell, end cell, and if we're currently selecting
start_cell = None
end_cell = None
selecting = False
final_selected_cells = []

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
    start_y = 50
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

def compute_path(start_cell, end_cell):
    if not start_cell or not end_cell:
        return []
    path = []
    delta_row = end_cell[0] - start_cell[0]
    delta_col = end_cell[1] - start_cell[1]
    step_row = delta_row // max(abs(delta_row), 1)
    step_col = delta_col // max(abs(delta_col), 1)
    
    for i in range(max(abs(delta_row), abs(delta_col)) + 1):
        path.append((start_cell[0] + i * step_row, start_cell[1] + i * step_col))
    return path

def is_valid_word(path):
    word = ''.join(grid[y][x] for y, x in path).lower()
    return word in words

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not selecting:
                # Start selection
                start_cell = get_cell_from_mouse_pos(pygame.mouse.get_pos())
                selecting = True
                final_selected_cells.clear()
            else:
                # Finalize selection
                if is_valid_word(final_selected_cells):
                    print('Valid word selected:', ''.join(grid[y][x] for y, x in final_selected_cells))
                selecting = False
                start_cell = None

    current_hover_cell = get_cell_from_mouse_pos(pygame.mouse.get_pos())
    if selecting and start_cell and current_hover_cell:
        end_cell = current_hover_cell
        selected_cells = compute_path(start_cell, end_cell)
        if is_valid_word(selected_cells):
            final_selected_cells = list(selected_cells)
        else:
            final_selected_cells.clear()
    else:
        selected_cells = []

    screen.fill(Color.WHITE.value)
    draw_grid(grid, selected_cells)
    draw_words(words)
    pygame.display.flip()

pygame.quit()