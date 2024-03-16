import pygame
import sys
import json
from word_search_generator import WordSearch
import math

from util.colors import Color
from gemini.ai import words_related_to_theme
from algo.lazy import calculate_minimum_grid_size_with_buffer
# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Generative Word Search Game")

# Puzzle data
words = words_related_to_theme("programming")
size = calculate_minimum_grid_size_with_buffer(words=words)
puzzle_data = WordSearch(", ".join(words), size=size).json

# words = ",".join(words)
# print(puzzle_data)
puzzle_data = json.loads(puzzle_data)

# Extract puzzle grid and words
grid = puzzle_data['puzzle']
# print(grid)
words = puzzle_data['words']
# print(words)
# Font for rendering text
font = pygame.font.Font("assets/AovelSansRounded-rdDL.ttf", 36)

# Keep track of the start cell, end cell, and if we're currently selecting
start_cell = None
end_cell = None
selecting = False
final_selected_cells = []

valid_words_cells = []  # List to keep track of cells that are part of valid words
surface = pygame.display.get_surface()  # get the surface of the current active display
window_width, window_height = surface.get_width(), surface.get_height()  # create an array of surface.width and surface.height
BLOCK_SIZE = 40  # Size of grid block
grid_init_x = window_width / 4  # set the initial x position of the grid
grid_init_y = window_height / 4  # set the initial y position of the grid
strikethrough = False
selected_word = ''
strikethrough_word_indices = []

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

# Display the heading
HEAD_TEXT = get_font(20).render("Generative Word Search", True, '#9B56E3')
HEAD_TEXT_RECT = HEAD_TEXT.get_rect(center=(350, 100))

def draw_grid(grid, hover_cell):

    for y, row in enumerate(grid):
        for x, letter in enumerate(row):
            rect = pygame.Rect(grid_init_x + x * BLOCK_SIZE, grid_init_y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            if (y, x) in valid_words_cells:  # Check if cell is part of a valid word
                pygame.draw.rect(screen, Color.GREEN.value, rect)  # Use a different color for valid words
                text_color = Color.BLACK.value
            elif (y, x) in selected_cells or hover_cell == (y, x):
                pygame.draw.rect(screen, Color.BLUE.value, rect)
                text_color = Color.WHITE.value
            else:
                pygame.draw.rect(screen, Color.GREY.value, rect, 1)
                text_color = Color.BLACK.value
            text_surface = font.render(letter.lower(), True, text_color)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)


def add_rect(start_x, start_y):
    pygame.draw.rect(screen, Color.BLACK.value, pygame.Rect(start_x, start_y, 200, 200), 2)


def add_text(words, start_x, start_y, strikethrough, selected_word):

    for idx, word in enumerate(words):
        if (strikethrough and word.lower() == selected_word) or (idx in strikethrough_word_indices):
            if idx not in strikethrough_word_indices:
                strikethrough_word_indices.append(idx)
            text_surface = font.render(word, True, Color.BLACK.value)
            text_rect = text_surface.get_rect()
            text_rect.topleft = (start_x + 50, start_y + 25)
            # Calculate the position of the line for strikethrough effect
            line_y = text_rect.centery
            # Draw the text
            screen.blit(text_surface, text_rect)
            # Draw the strikethrough line
            pygame.draw.line(screen, Color.BLACK.value, (text_rect.left, line_y), (text_rect.right, line_y), 2)
        else:
            text = font.render(word, True, Color.RED.value)
            screen.blit(text, (start_x + 50, start_y + 25))

        start_y += 40


# Function to draw the words list
def draw_words(words, strikethrough, selected_word):
    start_x = BLOCK_SIZE + 520
    start_y = BLOCK_SIZE + 150

    add_rect(start_x, start_y)
    add_text(words, start_x, start_y, strikethrough, selected_word)


# Function to get cell from mouse position
def get_cell_from_mouse_pos(pos, grid_init_x, grid_init_y):
    x, y = pos
    row = (x - grid_init_x) // 40
    col = (y - grid_init_y) // 40
    if row < len(grid) and col < len(grid[0]):
        return (int(col), int(row))
    return None

def compute_path(start_cell, end_cell):
    if not start_cell or not end_cell:
        return []
    path = []
    delta_row = end_cell[0] - start_cell[0]
    delta_col = end_cell[1] - start_cell[1]
    step_row = delta_row // max(abs(delta_row), 1)
    step_col = delta_col // max(abs(delta_col), 1)
    
    for i in range(int(max(abs(delta_row), abs(delta_col)) + 1)):
        path.append((start_cell[0] + i * step_row, start_cell[1] + i * step_col))
    return path

def is_valid_word(path):
    selected_word = ''.join(grid[y][x] for y, x in path).lower()
    searchable_words = [word.lower() for word in words]
    print(selected_word, searchable_words)
    return selected_word in searchable_words

def get_word_position_from_list():
    x, y = BLOCK_SIZE + 570, BLOCK_SIZE + 175

    return (x, y)

def draw_text_with_strikethrough(text):
    for word in words:
        if text == word.lower():
            position = get_word_position_from_list()
            # Render the text
            text_surface = font.render(text, True, Color.BLACK.value)
            text_rect = text_surface.get_rect()
            text_rect.topleft = position
            # Calculate the position of the line for strikethrough effect
            line_y = text_rect.centery
            # Draw the text
            screen.blit(text_surface, text_rect)
            # Draw the strikethrough line
            pygame.draw.line(screen, Color.BLACK.value, (text_rect.left, line_y), (text_rect.right, line_y), 2)

# def game_over():

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            strikthrough = False
            if not selecting:
                # Start selection
                start_cell = get_cell_from_mouse_pos(pygame.mouse.get_pos(), grid_init_x, grid_init_y)
                if start_cell is not None:  # Ensure start_cell is within the grid
                    selecting = True
                    final_selected_cells.clear()
            else:
                if final_selected_cells and is_valid_word(final_selected_cells):
                    print('Valid word selected:', ''.join(grid[y][x] for y, x in final_selected_cells))
                    valid_words_cells.extend(final_selected_cells)  # Add the valid word's cells to the list
                else:
                    print('Invalid word selected:', ''.join(grid[y][x] for y, x in final_selected_cells))
                selecting = False
                start_cell = None
                final_selected_cells.clear()  # Clear selection regardless of validity

    current_hover_cell = get_cell_from_mouse_pos(pygame.mouse.get_pos(), grid_init_x, grid_init_y)
    if selecting and start_cell and current_hover_cell:
        end_cell = current_hover_cell
        if end_cell:  # Only compute the path if end_cell is within the grid
            selected_cells = compute_path(start_cell, end_cell)

            # print(is_valid_word(selected_cells))
            if is_valid_word(selected_cells):
                final_selected_cells = list(selected_cells)
                selected_word = ''.join(grid[y][x] for y, x in selected_cells).lower()
                strikethrough = True
            else:
                final_selected_cells.clear()
            print(selected_cells)

        else:
            selected_cells = []  # Clear temporary selection path if out of bounds
    else:
        selected_cells = []  # Clear temporary selection path when not selecting

    screen.fill((151, 161, 219))
    screen.blit(HEAD_TEXT, HEAD_TEXT_RECT)
    draw_grid(grid, selected_cells)  # Pass the temporary path for visualization
    draw_words(words, strikethrough, selected_word)
    pygame.display.flip()

pygame.quit()