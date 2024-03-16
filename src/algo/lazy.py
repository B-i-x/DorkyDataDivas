import random

def can_place_word(word, grid, row, col, direction, size):
    for i in range(len(word)):
        new_row = row + i * direction[0]
        new_col = col + i * direction[1]
        if new_row >= size or new_col >= size or new_row < 0 or new_col < 0:
            return False  # Out of bounds
        if grid[new_row][new_col] != '' and grid[new_row][new_col] != word[i]:
            return False  # Conflict
    return True

def place_word(word, grid, row, col, direction):
    for i in range(len(word)):
        new_row = row + i * direction[0]
        new_col = col + i * direction[1]
        grid[new_row][new_col] = word[i]
        
def calculate_minimum_grid_size_with_buffer(words, buffer_factor=1.2):
    base_size = max(len(max(words, key=len)), int((sum(len(word) for word in words) ** 0.5)))
    adjusted_size = int(base_size * buffer_factor)
    
    words_sorted = sorted(words, key=len, reverse=True)  # Sort words by length in descending order for better packing
    while True:
        grid = [['' for _ in range(adjusted_size)] for _ in range(adjusted_size)]
        if try_place_words(grid, words_sorted, 0):
            return adjusted_size
        adjusted_size += 1

def try_place_words(grid, words, index):
    if index == len(words):
        return True

    word = words[index]
    for direction in [(0, 1), (1, 0), (1, 1), (-1, 1)]:
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if can_place_word(word, grid, row, col, direction, len(grid)):
                    place_word(word, grid, row, col, direction)
                    if try_place_words(grid, words, index + 1):
                        return True
                    remove_word(word, grid, row, col, direction)
    return False

def remove_word(word, grid, row, col, direction):
    for i in range(len(word)):
        new_row = row + i * direction[0]
        new_col = col + i * direction[1]
        grid[new_row][new_col] = ''

# can_place_word and place_word functions remain the same.

def run():
    words = ["python", "java", "kotlin", "script"]  # Example word list
    minimum_grid_size = calculate_minimum_grid_size_with_buffer(words)
    print(f"Minimum grid size with buffer: {minimum_grid_size}")

if __name__ == "__main__":
    run()
