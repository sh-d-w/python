# Rule: Finds the outer edges of a specific high layer
#   and strips them back down to a lower value so the inner
#   volume footprint becomes smaller.


# map_filled.txt
def run_topping(input_file="heightmap.txt", output_file="map_flattened.txt", target_layer=2, lower_to=1):
    with open(input_file, "r") as f:
        grid = [line.strip().split() for line in f if line.strip()]
        
    rows, cols = len(grid), len(grid[0])
    new_grid = [row[:] for row in grid]
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == str(target_layer):
                # If any neighbor is not the target layer, this cell is an edge block
                is_edge = False
                for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] != str(target_layer):
                            is_edge = True
                    else:
                        is_edge = True # Border of map is an edge
                
                if is_edge:
                    new_grid[r][c] = str(lower_to)
                    
    with open(output_file, "w") as f:
        for row in new_grid:
            f.write(" ".join(row) + "\n")
    print(f"Topping complete -> Saved to {output_file}")

if __name__ == "__main__":
    run_topping()
