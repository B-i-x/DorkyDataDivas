import pkgutil


import sys
import os

src_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(src_dir)

# Now you should be able to import the algo package and its modules
from src.algo.greedy import calculate_minimum_grid_size_with_buffer
from src.algo.lazy import calculate_minimum_grid_size_with_buffer

import json
from word_search_generator import WordSearch
import random
import string

def generate_random_words(n, length=5):
    """Generate a list of 'n' random words, each of specified 'length'."""
    words = []
    for _ in range(n):
        word = ''.join(random.choices(string.ascii_lowercase, k=length))
        words.append(word)
    return words

def test_word_search(words, max_grid_size=20):
    """Test WordSearch for various grid sizes to see if all words fit."""
    # Convert the generated words to uppercase for comparison
    uppercase_words = [word.upper() for word in words]
    
    # for size in range(5, max_grid_size + 1):
        # Calculate minimum grid size with a buffer
    size = calculate_minimum_grid_size_with_buffer(words=words)
    
    # Generate puzzle with the calculated grid size
    puzzle_data = WordSearch(", ".join(words), size=size).json
    puzzle_data = json.loads(puzzle_data)
    output_words = puzzle_data['words']

    # Check if all uppercase generated words are in the output
    if all(word in output_words for word in uppercase_words):
        print(f"All words fit in a grid of size {size}x{size}.")
        return size
    else:
        missing_words = [word for word in uppercase_words if word not in output_words]
        print(f"Not all words fit in a grid of size {size}x{size}. Missing words: {missing_words}")

    print(f"Unable to fit all words in a grid up to size {max_grid_size}x{max_grid_size}.")
    return -1

# Example usage
# n_words = 10  # Number of random words to generate
for i in range(5, 25):
    print(f"Test {i}:")
    words = generate_random_words(i, length=5)
    print("Generated words:", words)

    test_word_search(words)
# words = generate_random_words(n_words, length=5)
# print("Generated words:", words)

# # Test WordSearch with these words for various grid sizes
# test_word_search(words)
