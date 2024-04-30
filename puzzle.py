import time

# Constants
CAPACITY = 100

class Puzzle:
    def __init__(self):
        self.content = [[''] * CAPACITY for _ in range(CAPACITY)]
        self.m = 0
        self.n = 0

class WordList:
    def __init__(self):
        self.content = []
        self.count = 0

def file2data(file_name, P, WL):
    file_path = f"./test/{file_name}"
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Initialize indices
    i = 0
    
    # Read puzzle content
    while i < len(lines) and lines[i].strip() != "":
        line = lines[i].strip().replace(" ", "")
        P.content[i][:len(line)] = line
        i += 1
    
    P.m = i
    P.n = len(line) if i > 0 else 0

    # Read word list content
    while i < len(lines):
        line = lines[i].strip()
        if line:
            WL.content.append(line)
            WL.count += 1
        i += 1

def print_grid(P, found_grid):
    for row in range(P.m):
        line = ''
        for col in range(P.n):
            if found_grid[row][col]:
                line += P.content[row][col] + ' '
            else:
                line += '- '
        print(line)

def search_word(P, W):
    length = len(W)
    found_grid = [[False] * CAPACITY for _ in range(CAPACITY)]
    
    for i in range(P.m):
        for j in range(P.n):
            # Define the lambda function for each direction
            directions = {
                "East": lambda k: (i, j + k),
                "Southeast": lambda k: (i + k, j + k),
                "South": lambda k: (i + k, j),
                "Southwest": lambda k: (i + k, j - k),
                "West": lambda k: (i, j - k),
                "Northwest": lambda k: (i - k, j - k),
                "North": lambda k: (i - k, j),
                "Northeast": lambda k: (i - k, j + k)
            }
            
            for direction, get_pos in directions.items():
                found = True
                for k in range(length):
                    row, col = get_pos(k)
                    
                    if not (0 <= row < P.m and 0 <= col < P.n):
                        found = False
                        break
                    
                    if P.content[row][col] != W[k]:
                        found = False
                        break
                
                if found:
                    for k in range(length):
                        row, col = get_pos(k)
                        found_grid[row][col] = True
                    print(f"Word '{W}' found in direction '{direction}' starting at ({i}, {j}):")
                    print_grid(P, found_grid)
                    return
    print(f"Word '{W}' not found!")

def main():
    P = Puzzle()
    WL = WordList()

    # Read file
    file_name = input("\nInput your test file name: ")
    print("\n")
    file2data(file_name, P, WL)

    # Brute Force
    count = 0
    start = time.time()

    for i in range(WL.count):
        search_word(P, WL.content[i])
        print("\n")
    
    end = time.time()
    duration = (end - start) * 1e6  # Convert to microseconds
    print(f"Time taken: {duration:.0f} microseconds")
    print(f"Total comparisons: {count} letters\n\n")

if __name__ == "__main__":
    main()
