def generate_terrain_from_txt(txt_filename="heightmap.txt", obj_filename="terrain.obj", scale_y=1.0):
    """
    Reads a grid of 0-9 digits from a text file and builds an indexed 3D .obj mesh.
    """
    # 1. Read and parse the text file into a 2D grid of numbers
    grid = []
    with open(txt_filename, "r") as f:
        for line in f:
            # Strip whitespace/newlines and pull out digit characters
            row = [int(char) for char in line.strip() if char.isdigit()]
            if row:
                grid.append(row)
                
    if not grid:
        print(f"Error: No valid digits found in {txt_filename}")
        return

    # Check for uniform row lengths
    row_length = len(grid[0])
    for i, row in enumerate(grid):
        if len(row) != row_length:
            print(f"Warning: Row {i} has a different length. Truncating to match.")
            grid[i] = row[:row_length]

    rows = len(grid)
    cols = row_length
    
    vertices = []
    faces = []

    # 2. Generate Vertices based on the grid positions
    # X = Column Index, Y = Height from file, Z = Row Index
    for z in range(rows):
        for x in range(cols):
            height = float(grid[z][x]) * scale_y
            vertices.append((float(x), height, float(z)))

    # 3. Connect Vertices into Triangular Faces (Quads split into two triangles)
    for z in range(rows - 1):
        for x in range(cols - 1):
            # Calculate 1-based vertex index pointers for the current quad cell
            top_left  = (z * cols) + x + 1
            top_right = top_left + 1
            bot_left  = ((z + 1) * cols) + x + 1
            bot_right = bot_left + 1

            # Triangle 1
            faces.append((top_left, bot_left, top_right))
            # Triangle 2
            faces.append((top_right, bot_left, bot_right))

    # 4. Write to .obj File
    with open(obj_filename, "w") as f:
        f.write(f"# Terrain generated from {txt_filename}\n")
        
        # Write out vertex list
        for v in vertices:
            f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
            
        # Write out face list linking vertex indices
        for face in faces:
            f.write(f"f {face[0]} {face[1]} {face[2]}\n")

    print(f"Success! Map dimensions: {cols}x{rows}. Exported mesh to {obj_filename}")

if __name__ == "__main__":
    # Adjust scale_y to make the height peaks taller or flatter
    generate_terrain_from_txt(scale_y=0.5)
