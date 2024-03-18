import pygame
import sys
import json
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie, QFont
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QDialog
from word_search_generator import WordSearch

from util.colors import Color, generate_colors_for_words, generate_pastel_color
from gemini.ai import words_related_to_theme
from algo.lazy import calculate_minimum_grid_size_with_buffer
from core.sounds import found_word_sound, game_won_sound
# Initialize Pygame and set up the display
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Generative Word Search Game")

# Load and set up puzzle data
words = words_related_to_theme("programming")
word_colors = generate_colors_for_words(words)
size = calculate_minimum_grid_size_with_buffer(words=words)
puzzle_data = json.loads(WordSearch(", ".join(words), size=size).json)

# Extract puzzle grid and words
grid = puzzle_data['puzzle']
words = [word.lower() for word in puzzle_data['words']]
font_path = "src/assets/Horizon Type - AcherusGrotesque-Regular.otf"
font = pygame.font.Font(font_path, 36)

# Initialize game variables
MARGIN_BETWEEN_CELLS = 2.5
BLOCK_SIZE = 40
FONT_SIZE = 25
MARGIN_LEFT = 60
MARGIN_TOP = 25
LINE_SPACING = 40
WORD_BOX_WIDTH = 200  # Assuming a fixed width for the word list box
WORD_BOX_VERTICAL_AXIS_PLACEMENT_RELATIVE_TO_SCREEN = 4 / 5
start_cell = end_cell = None
selecting = False
final_selected_cells = []
valid_words_cells = {}
selected_word = ''
selected_words = []
strikethrough_word_indices = []
grid_width = len(grid[0]) * (BLOCK_SIZE + MARGIN_BETWEEN_CELLS) - MARGIN_BETWEEN_CELLS
grid_height = len(grid) * (BLOCK_SIZE + MARGIN_BETWEEN_CELLS) - MARGIN_BETWEEN_CELLS
grid_init_x = (screen_width / 3) - grid_width / 2
grid_init_y = (screen_height - grid_height) / 2
strikethrough = False

# colors
counter = 0

# GUI setup
class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        center_x = self.geometry().width() / 2
        center_y = self.geometry().height() / 2
        self.move(int(center_x), int(center_y))
        self.setWindowTitle('Congratulations!')
        self.resize(400, 200)  # Set the size of the dialog
        self.setStyleSheet('background-color: #F6EFEE;')

        # Add a layout
        layout = QVBoxLayout(self)

        # Add a label
        label = QLabel('You Won!', self)
        font = QFont(font_path, 50)
        label.setFont(font)
        layout.addWidget(label)
        # Set the alignment of the label within its cell
        layout.setAlignment(label, QtCore.Qt.AlignCenter)

        # Create a QLabel to display the background GIF
        background_label = QLabel(self)
        background_label.setAlignment(Qt.AlignCenter)

        # Set the background GIF
        movie = QMovie('assets/fireworks.gif')
        background_label.setMovie(movie)
        movie.start()

        # Add the background QLabel to the layout
        layout.addWidget(background_label)

        # Add a button
        button = QPushButton('Close')
        button.setStyleSheet('''QPushButton {
                font-size: 20px;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: darkgray;
            }
            ''')
        layout.addWidget(button)
        button.clicked.connect(self.close_all_windows)

    def close_all_windows(self):
        win_list = QApplication.allWindows()
        for w in win_list:
            w.close()
        pygame.quit()
        sys.exit()

def get_font(size):
    """Returns Press-Start-2P font in the specified size."""
    return pygame.font.Font("assets/font.ttf", size)


def draw_grid(grid, selected_cells):
    """
    Draws the puzzle grid, highlighting selected cells and applying rounded corners to each cell.

    The function iterates through each cell in the grid, determines its color based on its selection state,
    and then draws the cell with the determined color. It also renders the letter in each cell centrally.

    :param grid: A 2D list representing the puzzle grid where each element is a letter.
    :param selected_cells: A list of tuples representing the coordinates (y, x) of selected cells.
    """
    # Calculate the font size as 50% of the block size for proportional letter rendering within cells.
    font = pygame.font.Font(font_path, int(BLOCK_SIZE * 0.5))
    
    # Iterate through each row and column of the grid to draw individual cells.
    for y, row in enumerate(grid):
        for x, letter in enumerate(row):
            # Calculate the position and size of the cell's rectangle, accounting for margins between cells.
            rect = pygame.Rect(grid_init_x + x * (BLOCK_SIZE + MARGIN_BETWEEN_CELLS),
                               grid_init_y + y * (BLOCK_SIZE + MARGIN_BETWEEN_CELLS),
                               BLOCK_SIZE - 2*MARGIN_BETWEEN_CELLS,
                               BLOCK_SIZE - 2*MARGIN_BETWEEN_CELLS)
            
            # Determine the background and text color for the current cell.
            color, text_color = determine_cell_color(x, y, selected_cells)
            
            # Draw the rectangle for the cell with rounded corners. The radius is set to 10% of the BLOCK_SIZE.
            pygame.draw.rect(screen, color, rect, border_radius=int(BLOCK_SIZE * 0.1))
            
            # Render the letter in the cell, centering it within the cell's rectangle.
            text_surface = font.render(letter.lower(), True, text_color)
            screen.blit(text_surface, text_surface.get_rect(center=rect.center))


def determine_cell_color(x, y, selected_cells):
    """
    Determines the background color of a cell and the color of its text based on its selection state
    and whether it is part of a valid word.

    :param x: The x-coordinate (column index) of the cell in the grid.
    :param y: The y-coordinate (row index) of the cell in the grid.
    :param selected_cells: A list of tuples representing the coordinates (y, x) of selected cells.
    :return: A tuple containing the determined background color and text color for the cell.
    """
    # Default colors for a cell; can be overridden based on cell's state.
    color = Color.MAIN_BACKGROUND_COLOR.value  # Default background color for a cell
    text_color = Color.BLACK.value             # Default text color

    # Check if the current cell is selected; if so, change its background color.
    if (y, x) in selected_cells:
        color = Color.HOVER_CELL_COLOR.value
    
    # Iterate through each valid word and its corresponding cells to check if the current cell
    # is part of any valid word. If it is, assign a special color to indicate its validity.
    for word, cells in valid_words_cells.items():
        if (y, x) in cells:
            # If the cell is part of a valid word, use the word's specific color or a default if not specified.
            color = word_colors.get(word, Color.GREY.value)
            break  # Stop checking further if we've found the cell is part of a valid word.

    return color, text_color
    # Returns the final determined background color and text color for the cell.


def add_rect(start_x, start_y, height_in_pixels=200):
    pygame.draw.rect(screen, Color.BLACK.value, pygame.Rect(start_x, start_y, 200, height_in_pixels), 2)


def draw_words(words, strikethrough, selected_word):
    """
    Handles drawing the word list with optional strikethrough effect, ensuring that the block's
    horizontal midline is aligned with the screen's horizontal axis and its vertical midline is
    adjusted based on the WORD_BOX_VERTICAL_AXIS_PLACEMENT_RELATIVE_TO_SCREEN variable.
    
    :param words: List of words to draw.
    :param strikethrough: Indicates if a strikethrough effect should be applied.
    :param selected_word: The word currently selected (for strikethrough).
    """
    # Assume WORD_BOX_WIDTH is defined elsewhere in your code, e.g., as a constant.
    
    # First, draw the text off-screen to calculate the total height needed
    offscreen_surface = pygame.Surface((WORD_BOX_WIDTH, screen_height))
    height_of_words = add_text(words, 0, 0, strikethrough, selected_word, surface=offscreen_surface)

    # Calculate the starting X position so that the box's vertical midline is at the desired fraction of the screen's width
    start_x = screen_width * WORD_BOX_VERTICAL_AXIS_PLACEMENT_RELATIVE_TO_SCREEN - WORD_BOX_WIDTH / 2

    # Calculate the starting Y position so that the box's horizontal midline is aligned with the screen's horizontal axis
    start_y = (screen_height - height_of_words) / 2

    # Now draw the text on the actual screen
    add_text(words, start_x, start_y, strikethrough, selected_word, surface=screen)
    add_rect(start_x, start_y, height_of_words)

# Modify the add_text function signature to accept a `surface` parameter, allowing us to draw on different surfaces
def add_text(words, start_x, start_y, strikethrough, selected_word, surface):
    """
    Renders words with optional strikethrough effect to indicate selection or completion.
    This version accepts a `surface` parameter to support off-screen height calculation and actual drawing,
    and adjusts the strikethrough effect to apply only across the text width.

    :param words: List of words to display.
    :param start_x: The starting X coordinate.
    :param start_y: The starting Y coordinate.
    :param strikethrough: Boolean indicating whether to apply strikethrough.
    :param selected_word: The currently selected word.
    :param surface: The pygame Surface to draw on.
    :return: The total height of rendered text area.
    """
    font = pygame.font.Font(font_path, FONT_SIZE)
    total_height = 0
    for idx, word in enumerate(words):
        # Render the word
        text_surface = font.render(word, True, Color.BLACK.value)
        text_width = text_surface.get_width()  # Get the width of the rendered text
        surface.blit(text_surface, (start_x + MARGIN_LEFT, start_y + total_height))
        
        # Apply strikethrough if needed
        if (strikethrough and word.lower() == selected_word) or (idx in strikethrough_word_indices):
            if idx not in strikethrough_word_indices:
                strikethrough_word_indices.append(idx)
            line_y = start_y + total_height + font.get_height() / 2
            # Draw the strikethrough line across the width of the text, not the whole box
            pygame.draw.line(surface, Color.BLACK.value, (start_x + MARGIN_LEFT, line_y), (start_x + MARGIN_LEFT + text_width, line_y), 2)
        
        total_height += font.get_height() + LINE_SPACING - FONT_SIZE

    return total_height


def get_cell_from_mouse_pos(pos, grid_init_x, grid_init_y):
    """
    Converts a mouse position to grid coordinates.
    
    :param pos: The mouse position tuple (x, y).
    :param grid_init_x: The initial x position of the grid.
    :param grid_init_y: The initial y position of the grid.
    :return: The cell coordinates as a tuple (row, col), or None if outside grid.
    """
    x, y = pos
    row = int((y - grid_init_y) / BLOCK_SIZE)
    col = int((x - grid_init_x) / BLOCK_SIZE)
    if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
        return (row, col)
    return None



def compute_path(start_cell, end_cell):
    """
    Computes the path between two cells, considering diagonal, horizontal, or vertical movements.
    
    :param start_cell: The starting cell coordinates as a tuple (row, col).
    :param end_cell: The ending cell coordinates as a tuple (row, col).
    :return: A list of cell coordinates representing the path.
    """
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
    """
    Checks if the selected cells form a valid word in the word list.
    
    :param path: A list of cell coordinates.
    :return: True if the path forms a valid word, False otherwise.
    """
    try:
        selected_word = ''.join(grid[y][x] for y, x in path).lower()
    except IndexError:  # Catch out-of-bounds selections
        return False
    return selected_word in [word.lower() for word in words]

def game_over():
    game_won_sound()  # Play a sound effect for winning the game
    app = QApplication(sys.argv)
    window = MainWindow()
    window.exec_()
    sys.exit(app.exec_())


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit the loop if the game window is closed
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Reset strikethrough for new selection
            strikethrough = False
            
            # Handle selection logic
            if not selecting:
                # If not already selecting, start new selection
                start_cell = get_cell_from_mouse_pos(pygame.mouse.get_pos(), grid_init_x, grid_init_y)
                if start_cell is not None:  # Confirm the start cell is within the grid
                    selecting = True
                    final_selected_cells.clear()  # Reset the list for new selections
            else:
                # Validate the selection upon mouse button release
                if final_selected_cells and is_valid_word(final_selected_cells):
                    valid_word = ''.join(grid[y][x] for y, x in final_selected_cells).lower()
                    if valid_word not in valid_words_cells:
                        # Save the selection if it's a new valid word
                        valid_words_cells[valid_word] = list(final_selected_cells)
                        selected_word = ''.join(grid[y][x] for y, x in final_selected_cells).lower()
                        selected_words.append(selected_word)
                        selected_words = [x.lower() for x in selected_words]
                        strikethrough = True

                        found_word_sound()  # Play a sound effect for finding a word
                else:
                    # Provide feedback for invalid selections
                    print("Invalid or no word selected")

                # Reset selection status
                selecting = False
                start_cell = None
                final_selected_cells.clear()

    # Highlighting the cell under the mouse cursor
    current_hover_cell = get_cell_from_mouse_pos(pygame.mouse.get_pos(), grid_init_x, grid_init_y)
    selected_cells = []
    if selecting and start_cell and current_hover_cell:
        end_cell = current_hover_cell
        if end_cell:  # Validate end cell is within the grid
            selected_cells = compute_path(start_cell, end_cell)

            # Check if the path forms a valid word
            if is_valid_word(selected_cells):
                # Save and highlight the valid selection
                final_selected_cells = list(selected_cells)
              
            else:
                final_selected_cells.clear()  # Clear selection if the path is invalid

    # Refresh the screen
    screen.fill(Color.MAIN_BACKGROUND_COLOR.value)
    draw_grid(grid, selected_cells)  # Draw the grid with the current selection highlighted
    draw_words(words, strikethrough, selected_word)  # Draw the list of words, marking found ones
    pygame.display.flip()  # Update the display with everything drawn

    # Check for game completion
    if set(selected_words) == set(words):
        game_over()  # Call the game over function when all words are found


pygame.quit()
sys.exit()
