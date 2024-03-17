import pygame
import sys
import json

from PyQt5.QtWidgets import QMessageBox, QApplication
from word_search_generator import WordSearch

from util.colors import Color, generate_colors_for_words, generate_pastel_color
from gemini.ai import words_related_to_theme
from algo.lazy import calculate_minimum_grid_size_with_buffer

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

# words = ",".join(words)
# print(puzzle_data)
puzzle_data = json.loads(puzzle_data)

# Extract puzzle grid and words
grid = puzzle_data['puzzle']
words = [word.lower() for word in puzzle_data['words']]
font_path = "src/assets/Horizon Type - AcherusGrotesque-Regular.otf"
font = pygame.font.Font(font_path, 36)

# Initialize game variables
MARGIN_BETWEEN_CELLS = 2.5
BLOCK_SIZE = 40
start_cell = end_cell = None
selecting = False
final_selected_cells = []
valid_words_cells = {}
selected_word = ''
selected_words = []
strikethrough_word_indices = []
grid_init_x = screen_width / 4  # set the initial x position of the grid
grid_init_y = screen_height / 4  # set the initial y position of the grid
strikethrough = False

# colors
counter = 0
# GUI setup
class MainWindow(QMessageBox):
    def __init__(self):
        super().__init__()
        center_x = self.geometry().width() / 2
        center_y = self.geometry().height() / 2
        self.move(int(center_x), int(center_y))
        self.information(self, "Congratulations!", "You Won!", QMessageBox.Ok)

def get_font(size):
    """Returns Press-Start-2P font in the specified size."""
    return pygame.font.Font("assets/font.ttf", size)


def draw_grid(grid, selected_cells):
    """Draws the puzzle grid and highlights selected cells."""
    font = pygame.font.Font(font_path, int(BLOCK_SIZE * 0.5))
    for y, row in enumerate(grid):
        for x, letter in enumerate(row):
            rect = pygame.Rect(grid_init_x + x * (BLOCK_SIZE + MARGIN_BETWEEN_CELLS),
                               grid_init_y + y * (BLOCK_SIZE + MARGIN_BETWEEN_CELLS),
                               BLOCK_SIZE - 2*MARGIN_BETWEEN_CELLS,
                               BLOCK_SIZE - 2*MARGIN_BETWEEN_CELLS)
            color, text_color = determine_cell_color(x, y, selected_cells)
            pygame.draw.rect(screen, color, rect, border_radius=int(BLOCK_SIZE * 0.1))
            text_surface = font.render(letter.lower(), True, text_color)
            screen.blit(text_surface, text_surface.get_rect(center=rect.center))


def determine_cell_color(x, y, selected_cells):
    """Determines the color of a cell based on its state."""
    color = Color.MAIN_BACKGROUND_COLOR.value
    text_color = Color.BLACK.value
    if (y, x) in selected_cells:
        color = Color.HOVER_CELL_COLOR.value
    for word, cells in valid_words_cells.items():
        if (y, x) in cells:
            color = word_colors.get(word, Color.GREY.value)
            break
    return color, text_color


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
    app = QApplication(sys.argv)
    window = MainWindow()
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
                selected_word = ''.join(grid[y][x] for y, x in selected_cells).lower()
                selected_words.append(selected_word)
                selected_words = [x.lower() for x in selected_words]
                strikethrough = True
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
