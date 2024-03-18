# Installs

pip install pygame word-search-generator

pip install gitpython

pip install google-generativeai

# Cool Notes

**Greedy Algorithm**

we developed a custom greedy algorithm to find the minimum size of the word search grid

it is src->algo->greedy.py

we tested this algorithm exhaustively in order to make sure that it was as good if not better than the word search package we were using.

Our algorithim performed better than the word search package overall but not in a predictable way because the word search package used some randomness

This meant that we had to use our greedy algorithm as a starting point for the grid size and then run the word search package and then check if the word search packge was able to fit all of our desired words in the package. If the word search package failed to generate all the words in the package, we would increase the size of grid and check again. This would go on until we know for sure all of the words are there