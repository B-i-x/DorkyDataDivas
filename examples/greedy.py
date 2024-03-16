def can_place(word, grid, row, col, direction, size):
    """Check if a word can be placed in the grid from (row, col) in the specified direction."""
    if direction == 'h':
        if col + len(word) > size: return False
    elif direction == 'v':
        if row + len(word) > size: return False
    else:  # direction == 'd'
        if row + len(word) > size or col + len(word) > size: return False

    for i in range(len(word)):
        if direction == 'h':
            if grid[row][col + i] not in ('', word[i]): return False
        elif direction == 'v':
            if grid[row + i][col] not in ('', word[i]): return False
        else:  # direction == 'd'
            if grid[row + i][col + i] not in ('', word[i]): return False
    return True

def place_word(word, grid, row, col, direction):
    """Place a word in the grid from (row, col) in the specified direction."""
    for i in range(len(word)):
        if direction == 'h':
            grid[row][col + i] = word[i]
        elif direction == 'v':
            grid[row + i][col] = word[i]
        else:  # direction == 'd'
            grid[row + i][col + i] = word[i]

def fit_words_in_grid(words):
    size = max(len(word) for word in words)
    while True:
        grid = [['' for _ in range(size)] for _ in range(size)]
        all_placed = True
        for word in words:
            placed = False
            for direction in ('h', 'v', 'd'):
                if placed: break
                for row in range(size):
                    if placed: break
                    for col in range(size):
                        if can_place(word, grid, row, col, direction, size):
                            place_word(word, grid, row, col, direction)
                            placed = True
                            break
            if not placed:
                all_placed = False
                break  # Exit early if any word can't be placed
        if all_placed:
            return size  # All words placed successfully
        size += 1  # Increase grid size and try again

# Example usage
words = ["python", "java", "kotlin", "swift", "javascript"]
min_size = fit_words_in_grid(words)
print(f"Minimum grid size: {min_size}")
