import math

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
    vertexNormals = []
    vertex_counter = 1

    # 1. Generate Vertices for valid numbers
    for z in range(rows):
        for x in range(cols):
            val = grid[z][x]
            if val == 'U':

                if x < cols - 1 and z < rows - 1:
                    topLeft = grid[z][x]
                    topRight = grid[z][x + 1]
                    bottomLeft = grid[z + 1][x]
                    bottomRight = grid[z + 1][x + 1]

                    if topLeft == 'U' and topRight == 'U' and bottomLeft == 'U' and bottomRight == 'U':
                        continue
                    else:
                        val = '0' # treat as a 0 plane so isn't blocky but rather like 42's fdf.
                else:
                    val = '0'

            height = float(val) * scale_y
            vertices.append((float(x), height, float(z)))

            coord_to_idx[(z, x)] = vertex_counter
            vertex_counter += 1

    # 2. Connect Vertices into Triangles (All-diagonal coverage)
    for z in range(rows - 1):
        for x in range(cols - 1):
            # // for each grid item              # grid[z][x]

            # 0 1
            # 1 0

            # form triangles:
                # there should be a topleft to topright to bottomleft
                #  and below topright and bottom right
            # topLeft = grid[z][x]
            # topRight = grid[z][x + 1]
            # bottomLeft = grid[z + 1][x]
            # bottomRight = grid[z + 1][x + 1]

            # vertices = {x: topLeft, y: grid[z][x],z: z}

            # then each triangle formed is a vertice 1 2 and 3 that make the face and each vertices goes x y and z wise in the vertices section.





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
                # faces.append((coord_to_idx[p1], coord_to_idx[p3], coord_to_idx[p2]))
                # faces.append((coord_to_idx[p2], coord_to_idx[p3], coord_to_idx[p4]))
                faces.append((coord_to_idx[p1], coord_to_idx[p2], coord_to_idx[p4], coord_to_idx[p3]))

                calculateVertexNormal(vertices[coord_to_idx[p1] - 1], vertices[coord_to_idx[p2] - 1], vertices[coord_to_idx[p3] - 1], vertexNormals)

            # Case B: Only 3 corners exist -> Figure out which corner is missing and fill it
            else:# this should not happen now:
                # Missing Bottom Right (p4) -> Draw Top-Left triangle
                if has_p1 and has_p2 and has_p3:
                    # p4
                    faces.append((coord_to_idx[p1], coord_to_idx[p3], coord_to_idx[p2]))

                    calculateVertexNormal(vertices[coord_to_idx[p1] - 1], vertices[coord_to_idx[p2] - 1], vertices[coord_to_idx[p3] - 1], vertexNormals)
                    print("REACHED p4")

                # Missing Top Left (p1) -> Draw Bottom-Right triangle
                if has_p2 and has_p3 and has_p4:
                    # p1
                    faces.append((coord_to_idx[p2], coord_to_idx[p3], coord_to_idx[p4]))

                    calculateVertexNormal(vertices[coord_to_idx[p2] - 1], vertices[coord_to_idx[p3] - 1], vertices[coord_to_idx[p4] - 1], vertexNormals)
                    print("REACHED p1")
                
                # Missing Bottom Left (p3) -> Alternate diagonal split (Top-Left, Top-Right, Bottom-Right)
                if has_p1 and has_p2 and has_p4:
                    # p3
                    faces.append((coord_to_idx[p1], coord_to_idx[p4], coord_to_idx[p2]))

                    calculateVertexNormal(vertices[coord_to_idx[p1] - 1], vertices[coord_to_idx[p4] - 1], vertices[coord_to_idx[p2] - 1], vertexNormals)
                    print("REACHED p3")
                
                # Missing Top Right (p2) -> Alternate diagonal split (Top-Left, Bottom-Left, Bottom-Right)
                if has_p1 and has_p3 and has_p4:
                    # p2
                    faces.append((coord_to_idx[p1], coord_to_idx[p3], coord_to_idx[p4]))

                    calculateVertexNormal(vertices[coord_to_idx[p1] - 1], vertices[coord_to_idx[p3] - 1], vertices[coord_to_idx[p4] - 1], vertexNormals)
                    print("REACHED p2")


    # 3. Write to .obj File
    with open(obj_filename, "w") as f:
        f.write(f"# Terrain generated from {txt_filename}\n")

        for v in vertices:
            f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")

        for vn in vertexNormals:
            f.write(f"vn {vn[0]:.6f} {vn[1]:.6f} {vn[2]:.6f}")

        for face in faces:
            if len(face) == 4:
                f.write(f"f {face[0]} {face[1]} {face[2]} {face[3]}\n")
            else:
                f.write(f"f {face[0]} {face[1]} {face[2]}\n")


    print(f"Success! Map dimensions: {cols}x{rows}. Exported sloped mesh to {obj_filename}")



def calculateVertexNormal(v1, v2, v4, vertexNormals):
    # vn = calculate_normal(v1, v2, v4)
    vn = calculate_invertNormal(v1, v2, v4)
    vertexNormals.append(vn)

def calculate_normal(v1, v2, v4):
    # Calculate edges
    e1 = [v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]]
    e2 = [v4[0] - v2[0], v4[1] - v2[1], v4[2] - v2[2]]
    
    # Cross product (e1 x e2)
    nx = e1[1] * e2[2] - e1[2] * e2[1]
    ny = e1[2] * e2[0] - e1[0] * e2[2]
    nz = e1[0] * e2[1] - e1[1] * e2[0]
    
    # Normalize length
    length = math.sqrt(nx**2 + ny**2 + nz**2)
    if length == 0:
        return [0.0, 0.0, 0.0]
        
    return [nx / length, ny / length, nz / length]

def calculate_invertNormal(v1, v2, v4):
    # Calculate edges
    e1 = [v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]]
    e2 = [v4[0] - v2[0], v4[1] - v2[1], v4[2] - v2[2]]
    
    # Cross product (e1 x e2)
    nx = e1[1] * e2[2] - e1[2] * e2[1]
    ny = e1[2] * e2[0] - e1[0] * e2[2]
    nz = e1[0] * e2[1] - e1[1] * e2[0]
    
    # Normalize length
    length = math.sqrt(nx**2 + ny**2 + nz**2)
    if length == 0:
        return [0.0, 0.0, 0.0]
        
    return [nx / -length, ny / -length, nz / -length]


if __name__ == "__main__":
    generate_terrain_from_txt(scale_y=0.5)




