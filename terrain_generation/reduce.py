# Rule: Shrinks a specific number footprint from the outside
#	inward, turning its outer edges back into U (empty space).
#	This is the perfect counterpart to expanse.py for eroding
#	structures or opening up cave entrances.

def run_reduce(filename="heightmap.txt", output_file="map_reduced.txt", target=1):
    # Read the current grid state
    with open(filename, "r") as f:
        grid = [line.strip().split() for line in f if line.strip()]
    
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    new_grid = [row[:] for row in grid]
    
    # Erode the target number inward
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == str(target):
                # Check if it touches a 'U' or the map boundary
                is_outer_edge = False
                for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] == 'U':
                            is_outer_edge = True
                    else:
                        is_outer_edge = True # Border of the map acts as an edge
                
                # Turn the outside edge back into air/void
                if is_outer_edge:
                    new_grid[r][c] = 'U'
                        
    # Overwrite the file with the new grid state
    with open(output_file, "w") as f:
        for row in new_grid:
            f.write(" ".join(row) + "\n")
            
    print(f"Reduction complete -> Inward erosion applied to target '{target}' in {output_file}")

if __name__ == "__main__":
    # Example: Erode the outer edges of your base layer '1's into 'U's
    run_reduce(target=1)
