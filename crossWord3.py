import random

def create_empty_grid(rows, cols):
    grid = {}
    for row in range(1, rows + 1):
        for col in range(1, cols + 1):
            grid[f"{chr(64 + col)}{row}"] = ' '
    return grid



def try_place_word(grid, word, cell, direction):
    row, col = int(cell[1:]), ord(cell[0]) - 64
    # Check if the word fits horizontally
    if direction == 'h':
        if col + len(word) - 1 > max([ord(cell[0]) - 64 for cell in grid.keys()]) or \
                any(grid[f"{chr(64 + col + i)}{row}"] != ' ' and grid[f"{chr(64 + col + i)}{row}"] != word[i] for i in range(len(word))):
            return False
    # Check if the word fits vertically
    elif direction == 'v':
        if row + len(word) - 1 > max([int(cell[1:]) for cell in grid.keys()]) or \
                any(grid[f"{chr(64 + col)}{row + i}"] != ' ' and grid[f"{chr(64 + col)}{row + i}"] != word[i] for i in range(len(word))):
            return False
    else:
        raise ValueError("Invalid direction. Use 'h' for horizontal or 'v' for vertical.")

    return True


def place_word(grid, word, cell, direction):
    row, col = int(cell[1:]), ord(cell[0]) - 64
    if direction == 'h':
        for i in range(len(word)):
            grid[f"{chr(64 + col + i)}{row}"] = word[i]
    elif direction == 'v':
        for i in range(len(word)):
            grid[f"{chr(64 + col)}{str(row + i)}"] = word[i]  # Convert 'row + i' back to a string


def fill_empty_cells(grid):
    for cell, value in grid.items():
        if value == ' ':
            grid[cell] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

def has_common_vowels(word1, word2):
    vowels = set('AEIOU')
    return any(char in vowels for char in word1) and any(char in vowels for char in word2)

def intersect_words(words):
    intersecting_pairs = []
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            if has_common_vowels(words[i], words[j]):
                intersecting_pairs.append((words[i], words[j]))
    return intersecting_pairs

def generate_crossword(words, rows, cols):
    grid = create_empty_grid(rows, cols)
    intersecting_pairs = intersect_words(words)
    placed_words = []
    word_map = {}

    for word in words:
        placed = False
        for _ in range(10):  # Try placing the word multiple times
            cell = random.choice(list(grid.keys()))
            direction = random.choice(['h', 'v'])
            if try_place_word(grid, word, cell, direction):
                place_word(grid, word, cell, direction)
                placed_words.append((word, cell, direction))
                last_cell = f"{chr(ord(cell[0]) + len(word) - 1)}{int(cell[1:]) + len(word) - 1}"
                word_map[f"{cell} to {last_cell}"] = word
                placed = True
                break
        if not placed:
            print(f"Warning: Unable to place word '{word}' in the crossword.")

    fill_empty_cells(grid)
    display_grid(grid)

    print("Intersecting pairs with common vowels:")
    for word1, word2 in intersecting_pairs:
        print(f"{word1} intersects with {word2}")

    return word_map

def display_grid(grid):
    max_row = max([int(cell[1:]) for cell in grid.keys()])
    max_col = max([ord(cell[0]) - 64 for cell in grid.keys()])
    for row in range(1, max_row + 1):
        for col in range(1, max_col + 1):
            cell = f"{chr(64 + col)}{row}"
            print(grid[cell], end=' ')
        print()

# Example usage:
if __name__ == "__main__":
    predefined_words = ["PYTHON", "ALGORITHM", "PUZZLE", "CROSSWORD", "GRID", "WORD", "EXAMPLE", "VOWEL"]
    rows, cols = 10, 10  # Specify the desired grid dimensions here
    word_map = generate_crossword(predefined_words, rows, cols)
    print("\nWord Map:")
    for key, value in word_map.items():
        print(f"{key}: {value}")
