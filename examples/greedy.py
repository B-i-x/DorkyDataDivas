def calculate_minimum_grid_size(words):
    # Initial grid size is set to the length of the longest word to ensure it fits in at least one direction
    size = max(len(word) for word in words)
    
    while True:
        # Attempt to create a puzzle with the current size
        puzzle, success = try_create_puzzle(words, size)
        if success:
            return size  # If successful, the current size is sufficient
        size += 1  # Otherwise, increment the size and try again

def try_create_puzzle(words, size):
    # Initialize an empty grid
    grid = [['' for _ in range(size)] for _ in range(size)]
    for word in words:
        placed = False
        for direction in [(0, 1), (1, 0), (1, 1), (-1, 1)]:  # Right, Down, Diagonal down-right, Diagonal up-right
            if placed:
                break
            for row in range(size):
                if placed:
                    break
                for col in range(size):
                    if can_place_word(word, grid, row, col, direction, size):
                        place_word(word, grid, row, col, direction)
                        placed = True
                        break
        if not placed:
            return None, False  # Return immediately if any word can't be placed
    return grid, True

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

# Example usage
words = ["python", "kotlin", "java", "script"]
minimum_grid_size = calculate_minimum_grid_size(words)
print(f"Minimum grid size: {minimum_grid_size}")
