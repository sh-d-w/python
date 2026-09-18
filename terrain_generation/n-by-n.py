# Rule: Identifies cells completely enclosed by numbers and fills them with a higher value, leaving the outer layer as a border ring.

import sys

# map_expanded.txt
def run_nByN(w=250, h=250, output_file="heightmap.txt", fill_val='U'):
    rows, cols = h, w
    new_grid = [[fill_val for _ in range(cols)] for _ in range(rows)]

    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            new_grid[r][c] = str(fill_val)
                
    with open(output_file, "w") as f:
        for row in new_grid:
            f.write(" ".join(row) + "\n")
    print(f"Inner Fill complete -> Saved to {output_file}")

if __name__ == "__main__":
    # Check if the user provided an argument
    width = 50
    height = 50

    if len(sys.argv) > 2:
        width = int(sys.argv[1])
        height = int(sys.argv[2])

    run_nByN(width, height)
