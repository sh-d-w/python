# Rule: Finds any target number (like 1) and duplicates it outward into any touching U empty spaces.

import sys
import random

def run_expanse(target=1, replace = 'U', input_file="heightmap.txt", output_file="heightmap.txt"):
    # Read grid
    with open(input_file, "r") as f:
        grid = [line.strip().split() for line in f if line.strip()]
    
    rows, cols = len(grid), len(grid[0])
    new_grid = [row[:] for row in grid]
    
    # Expand target number to cardinal neighbors
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == str(target):
                for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nr, nc = r + dr, c + dc
                    randomlyGenOrNot = bool(random.getrandbits(1))

                    if randomlyGenOrNot and 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == replace:
                        new_grid[nr][nc] = str(target)
                        
    # Write output file
    with open(output_file, "w") as f:
        for row in new_grid:
            f.write(" ".join(row) + "\n")
    print(f"Expanse complete -> Saved to {output_file}")

if __name__ == "__main__":
    targetValue = 1
    replaceValue = 'U'
    if len(sys.argv) > 1:
        targetValue = int(sys.argv[1])
    if len(sys.argv) > 2:
        replaceValue = sys.argv[2] # str

    run_expanse(targetValue, replaceValue)
