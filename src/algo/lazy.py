from word_search_generator import WordSearch
import json

def calculate_minimum_grid_size_with_buffer(words, buffer_factor=1.2):
    uppercase_words = [word.upper() for word in words]

    # Start with a base size estimate based on the longest word and total letter count
    base_size = max(len(max(words, key=len)), int((sum(len(word) for word in words) ** 0.5)))
    # Apply a buffer to the estimated size to account for placement inefficiencies
    adjusted_size = int(base_size * buffer_factor)
    
    if (adjusted_size < 5):
        adjusted_size = 5
    # print(adjusted_size)
    while True:
        # # Use WordSearch to generate the puzzle
        # puzzle_data = WordSearch(words, size=adjusted_size).json
        # puzzle_data = json.loads(puzzle_data)

        # # Check if WordSearch placed all the words
        # placed_words = set(word.upper() for word in puzzle_data['words'])
        # all_words_placed = all(word.upper() in placed_words for word in words)
        # # print(placed_words, all_words_placed)
        # if all_words_placed:
        #     return adjusted_size  # If successful, the current size with buffer is sufficient
        # else:
        #     # If not, increment the size and try again
        #     adjusted_size += 1  

        puzzle_data = WordSearch(", ".join(words), size=adjusted_size).json
        puzzle_data = json.loads(puzzle_data)
        output_words = puzzle_data['words']

        # Check if all uppercase generated words are in the output
        if all(word in output_words for word in uppercase_words):
            print(f"Minimum grid size : {adjusted_size}")

            return adjusted_size
        else:
            adjusted_size += 1  


# Assuming that the run function is part of the same module that contains the 
# calculate_minimum_grid_size_with_buffer function.
def run():
    # Example usage with a buffer factor
    words = ["python", "java", "kotlin", "script"]
    minimum_grid_size = calculate_minimum_grid_size_with_buffer(words)
    print(f"Minimum grid size with buffer: {minimum_grid_size}")

if __name__ == "__main__":
    run()
