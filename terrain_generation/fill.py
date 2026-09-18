# Rule: Identifies cells completely enclosed by numbers and fills them with a higher value, leaving the outer layer as a border ring.

import sys

# map_expanded.txt
def run_fill(toReplace_val='1', fill_val=2, input_file="heightmap.txt", output_file="heightmap.txt"):
    with open(input_file, "r") as f:
        grid = [line.strip().split() for line in f if line.strip()]
        
    rows, cols = len(grid), len(grid[0])
    new_grid = [row[:] for row in grid]
    
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            # Check if surrounded on all 4 sides by valid numbers (not 'U')
            neighbors = [grid[r-1][c], grid[r+1][c], grid[r][c-1], grid[r][c+1]]
            if all(n == (toReplace_val) for n in neighbors):
                new_grid[r][c] = str(fill_val)
                
    with open(output_file, "w") as f:
        for row in new_grid:
            f.write(" ".join(row) + "\n")
    print(f"Inner Fill complete -> Saved to {output_file}")

if __name__ == "__main__":
    toReplaceVal = '1'
    fillVal = 2

    if len(sys.argv) > 2:
        toReplaceVal = sys.argv[1]
        fillVal = int(sys.argv[2])

    run_fill(toReplaceVal, fillVal)
