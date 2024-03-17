import pygame
import sys
import json
from word_search_generator import WordSearch
from tkinter import *

from pgu import gui

#from PyQt5.QtWidgets import QMessageBox
from assets.git_path_setter import add_src_subdirs_to_path

add_src_subdirs_to_path()

from util.colors import Color, generate_colors_for_words, generate_pastel_color
from gemini.ai import words_related_to_theme
from algo.lazy import calculate_minimum_grid_size_with_buffer

font_path = "src/assets/Horizon Type - AcherusGrotesque-Regular.otf"
# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

MARGIN_BETWEEN_CELLS = 2.5  # Adjust the margin size as needed
# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Generative Word Search Game")

# Puzzle data
words = words_related_to_theme("programming")
word_colors = generate_colors_for_words(words)
# print(word_colors)
size = calculate_minimum_grid_size_with_buffer(words=words)
puzzle_data = WordSearch(", ".join(words), size=size).json

# words = ",".join(words)
# print(puzzle_data)
puzzle_data = json.loads(puzzle_data)

# Extract puzzle grid and words
grid = puzzle_data['puzzle']
# print(grid)
words = puzzle_data['words']
words = [x.lower() for x in words]
# print(words)
# Font for rendering text
font = pygame.font.Font(font_path, 36)

# Keep track of the start cell, end cell, and if we're currently selecting
start_cell = None
end_cell = None
selecting = False
final_selected_cells = []

valid_words_cells = {}  # List to keep track of cells that are part of valid words

surface = pygame.display.get_surface()  # get the surface of the current active display
window_width, window_height = surface.get_width(), surface.get_height()  # create an array of surface.width and surface.height

BLOCK_SIZE = 40  # Size of grid block
grid_init_x = window_width / 4  # set the initial x position of the grid
grid_init_y = window_height / 4  # set the initial y position of the grid
strikethrough = False
selected_word = ''
selected_words = []  # List to keep track of the words selected by the user
strikethrough_word_indices = []  # List to keep track of indices of the completed words

# colors
counter = 0

# Class widget or pop-up window
class POPDialog(gui.Dialog):

    # Class Constructor with variable-length Arguments
    def __init__(self, value, **params):
        # Title of the widget
        title = gui.Label("Popup Box")

        # Table in the Widget of size 100X70
        main = gui.Table(width=100, height=70)

        # Table Content or sample text
        label = gui.Label("This is a sample pop up!")

        # Ok Button
        btn = gui.Button("Ok")

        # Click Event and self.close Connection will
        # terminate the pop-up when Click event will perform
        btn.connect(gui.CLICK, self.close, None)

        # Next row is created in table
        main.tr()

        # Label is added in the TD Container of the row
        main.td(label)

        # Next row
        main.tr()

        # Next row
        main.tr()

        # Adding the button in the TD container
        main.td(btn)
        # Initializing the Constructor
        gui.Dialog.__init__(self, title, main)


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


# Display the heading
#HEAD_TEXT = get_font(20).render("Generative Word Search", True, '#9B56E3')
#HEAD_TEXT_RECT = HEAD_TEXT.get_rect(center=(350, 100))


def draw_grid(grid, hover_cell):
    global counter, valid_words_cells
    # Calculate the font size based on BLOCK_SIZE, adjust this ratio as needed
    font_size = int(BLOCK_SIZE * 0.5)  # Example ratio
    font = pygame.font.Font(font_path, font_size)
    
    for y, row in enumerate(grid):
        for x, letter in enumerate(row):
            # Adjusted rect size and position to add space between cells
            rect = pygame.Rect(grid_init_x + x * (BLOCK_SIZE + MARGIN_BETWEEN_CELLS) + MARGIN_BETWEEN_CELLS,
                               grid_init_y + y * (BLOCK_SIZE + MARGIN_BETWEEN_CELLS) + MARGIN_BETWEEN_CELLS,
                               BLOCK_SIZE - 2*MARGIN_BETWEEN_CELLS, BLOCK_SIZE - 2*MARGIN_BETWEEN_CELLS)
            # Define rounded corners, adjust radius as needed
            border_radius = int(BLOCK_SIZE * 0.1)  # Example radius, adjust as needed
            
            # if (y, x) in valid_words_cells:  # Check if cell is part of a valid word
            #     # Find the word that the cell belongs to
            #     for word, cells in valid_words_cells.items():
            #         if (y, x) in cells:
            #             color = word_colors[word]  # Use the stored color for this word
            #             break
            #     pygame.draw.rect(screen, color, rect, border_radius=border_radius)
            #     text_color = Color.BLACK.value

            #     text_color = Color.BLACK.value
            # elif (y, x) in selected_cells or hover_cell == (y, x):
            #     pygame.draw.rect(screen, Color.HOVER_CELL_COLOR.value, rect, border_radius=border_radius)
            #     text_color = Color.MAIN_BACKGROUND_COLOR.value
            # else:
            #     pygame.draw.rect(screen, Color.GREY.value, rect, 1, border_radius=border_radius)
            #     text_color = Color.BLACK.value

            # Default cell properties
            color = Color.MAIN_BACKGROUND_COLOR.value
            text_color = Color.BLACK.value
            
            # Check if current cell is part of any valid word
            cell_is_valid_word = False
            for word, cells in valid_words_cells.items():
                
                if (y, x) in cells:
                    color = word_colors.get(word, Color.GREY.value)
                    # print(color)
                    break

            # Highlight cells part of the current selection path
            if (y, x) in selected_cells:
                color = Color.HOVER_CELL_COLOR.value  # Adjust color for selected cells

            # Drawing the cell rectangle and letter as before
            pygame.draw.rect(screen, color, rect, border_radius=border_radius)
            text_surface = font.render(letter.lower(), True, text_color)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)



def add_rect(start_x, start_y, height_in_pixels=200):
    pygame.draw.rect(screen, Color.BLACK.value, pygame.Rect(start_x, start_y, 200, height_in_pixels), 2)


def add_text(words, start_x, start_y, strikethrough, selected_word):
    search_words_on_the_left_font = pygame.font.Font(font_path, 25)
    font_row_width, font_row_height = search_words_on_the_left_font.size(words[0])
    for idx, word in enumerate(words):
        if (strikethrough and word.lower() == selected_word) or (idx in strikethrough_word_indices):
            if idx not in strikethrough_word_indices:
                strikethrough_word_indices.append(idx)
            text_surface = search_words_on_the_left_font.render(word, True, Color.BLACK.value)
            text_rect = text_surface.get_rect()
            text_rect.topleft = (start_x + 60, start_y + 25)
            # Calculate the position of the line for strikethrough effect
            line_y = text_rect.centery
            # Draw the text
            screen.blit(text_surface, text_rect)
            # Draw the strikethrough line
            pygame.draw.line(screen, Color.BLACK.value, (text_rect.left, line_y), (text_rect.right, line_y), 2)
        else:
            text = search_words_on_the_left_font.render(word, True, Color.BLACK.value)
            screen.blit(text, (start_x + 60, start_y + 25))

        start_y += 40

    return ((40 - font_row_height) + 40)  * len(words)

# Function to draw the words list
def draw_words(words, strikethrough, selected_word):
    start_x = BLOCK_SIZE + 520
    start_y = BLOCK_SIZE + 150

    height_of_words = add_text(words, start_x, start_y, strikethrough, selected_word)
    # print(height_of_words)
    add_rect(start_x, start_y, height_of_words)


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
    try:
        selected_word = ''.join(grid[y][x] for y, x in path).lower()
    except IndexError:
        return False
    searchable_words = [word.lower() for word in words]
    # print(selected_word, searchable_words)
    return selected_word in searchable_words


def game_over():
    # empty = gui.Container(width=100, height=100)
    # gui.init(empty)
    # Initial Application is created with default theme
    app = gui.Desktop()
    # Connecting the Quit event with app.quit function,
    # which will terminate the gui execution
    app.connect(gui.QUIT, app.quit, None)
    # Initial Table
    c = gui.Table(width=320, height=240)
    # Object of the Class or widget
    dialog = POPDialog("#00ffff")
    # Click me button
    e = gui.Button("Click Me")
    # Connection Click event and open widget function,
    # which will open the class widget or pop-up
    e.connect(gui.CLICK, dialog.open, None)
    # next row
    c.tr()
    # adding the connection in TD container
    c.td(e)
    # Running the initial application
    app.run(c)

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
                # print(f"Before adding: {valid_words_cells}")
                if final_selected_cells and is_valid_word(final_selected_cells):
                    valid_word = ''.join(grid[y][x] for y, x in final_selected_cells).lower()
                    # print(f"Adding {valid_word}: {final_selected_cells}")
                    if valid_word not in valid_words_cells:
                        valid_words_cells[valid_word] = list(final_selected_cells)
                    # else:
                    #     valid_words_cells[valid_word].extend(final_selected_cells)  # Consider if this logic is necessary for your game
                    # print(f"After adding: {valid_words_cells}")
                else:
                    print("Invalid or no word selected")

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
                selected_words.append(selected_word)
                selected_words = [x.upper() for x in selected_words]
                strikethrough = True
            else:
                final_selected_cells.clear()
            # print(selected_cells)

        else:
            selected_cells = []  # Clear temporary selection path if out of bounds
    else:
        selected_cells = []  # Clear temporary selection path when not selecting

    screen.fill(Color.MAIN_BACKGROUND_COLOR.value)
    #screen.blit(HEAD_TEXT, HEAD_TEXT_RECT)
    draw_grid(grid, selected_cells)  # Pass the temporary path for visualization
    draw_words(words, strikethrough, selected_word)
    pygame.display.flip()
    if set(selected_words) == set(words):
        game_over()


pygame.quit()
