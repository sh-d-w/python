def generate_terrain_from_txt(txt_filename="heightmap.txt", obj_filename="terrain.obj", scale_y=1.0):
    """
    Reads a grid of space-separated strings from a text file. Builds an indexed 
    3D sloped .obj mesh that handles all diagonal cases to complete mountain sides.
    """
    grid = []
    with open(txt_filename, "r") as f:
        for line in f:
            tokens = line.strip().split()
            if tokens:
                row = []
                for token in tokens:
                    if token.upper() == 'U':
                        row.append('U')
                    else:
                        try:
                            row.append(int(token))
                        except ValueError:
                            row.append('U')
                grid.append(row)
                
    if not grid:
        print(f"Error: No valid data found in {txt_filename}")
        return

    # Check for uniform row lengths based on the first row
    row_length = len(grid[0])
    for i, row in enumerate(grid):
        if len(row) != row_length:
            print(f"Warning: Row {i} has a different length. Truncating/padding to match.")
            grid[i] = row[:row_length]

    rows = len(grid)
    cols = row_length
    
    vertices = []
    faces = []
    coord_to_idx = {}
    vertex_counter = 1

    # 1. Generate Vertices for valid numbers
    for z in range(rows):
        for x in range(cols):
            val = grid[z][x]
            if val == 'U':
                continue
                
            height = float(val) * scale_y
            vertices.append((float(x), height, float(z)))
            coord_to_idx[(z, x)] = vertex_counter
            vertex_counter += 1

    # 2. Connect Vertices into Triangles (All-diagonal coverage)
    for z in range(rows - 1):
        for x in range(cols - 1):
            p1 = (z, x)         # Top Left
            p2 = (z, x + 1)     # Top Right
            p3 = (z + 1, x)     # Bottom Left
            p4 = (z + 1, x + 1) # Bottom Right

            # Flags to see which vertices actually exist
            has_p1 = p1 in coord_to_idx
            has_p2 = p2 in coord_to_idx
            has_p3 = p3 in coord_to_idx
            has_p4 = p4 in coord_to_idx

            # Case A: All 4 corners exist -> Split into standard two triangles cleanly
            if has_p1 and has_p2 and has_p3 and has_p4:
                faces.append((coord_to_idx[p1], coord_to_idx[p3], coord_to_idx[p2]))
                faces.append((coord_to_idx[p2], coord_to_idx[p3], coord_to_idx[p4]))
            
            # Case B: Only 3 corners exist -> Figure out which corner is missing and fill it
            else:
                # Missing Bottom Right (p4) -> Draw Top-Left triangle
                if has_p1 and has_p2 and has_p3:
                    faces.append((coord_to_idx[p1], coord_to_idx[p3], coord_to_idx[p2]))
                
                # Missing Top Left (p1) -> Draw Bottom-Right triangle
                if has_p2 and has_p3 and has_p4:
                    faces.append((coord_to_idx[p2], coord_to_idx[p3], coord_to_idx[p4]))
                
                # Missing Bottom Left (p3) -> Alternate diagonal split (Top-Left, Top-Right, Bottom-Right)
                if has_p1 and has_p2 and has_p4:
                    faces.append((coord_to_idx[p1], coord_to_idx[p4], coord_to_idx[p2]))
                
                # Missing Top Right (p2) -> Alternate diagonal split (Top-Left, Bottom-Left, Bottom-Right)
                if has_p1 and has_p3 and has_p4:
                    faces.append((coord_to_idx[p1], coord_to_idx[p3], coord_to_idx[p4]))

    # 3. Write to .obj File
    with open(obj_filename, "w") as f:
        f.write(f"# Terrain generated from {txt_filename}\n")
        
        for v in vertices:
            f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
            
        for face in faces:
            f.write(f"f {face[0]} {face[1]} {face[2]}\n")

    print(f"Success! Map dimensions: {cols}x{rows}. Exported sloped mesh to {obj_filename}")

if __name__ == "__main__":
    generate_terrain_from_txt(scale_y=1.0)
