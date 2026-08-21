# Rule: Generates distinct, independent 3D column blocks for each grid cell. It skips U positions completely and prevents numbers from blending into slants.

# map_topped.txt
def export_block_mesh(input_file="heightmap.txt", output_obj="terrain.obj", block_size=1.0):
    with open(input_file, "r") as f:
        grid = [line.strip().split() for line in f if line.strip()]
        
    rows, cols = len(grid), len(grid[0])
    vertices = []
    faces = []
    v_idx = 1
    
    for r in range(rows):
        for c in range(cols):
            val = grid[r][c]
            if val == 'U':
                continue # Skip drawing anything at this point
                
            height = float(val)
            
            # Define coordinates for the 8 corners of an independent 3D block column
            x0, x1 = c * block_size, (c + 1) * block_size
            z0, z1 = r * block_size, (r + 1) * block_size
            y0, y1 = 0.0, height # Base sits at zero, top sits at the specified height number
            
            # 8 Vertices for a single block
            block_verts = [
                (x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1), # Bottom 4
                (x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)  # Top 4
            ]
            vertices.extend(block_verts)
            
            # 6 Faces (2 triangles per side) for this isolated block
            block_faces = [
                (v_idx+4, v_idx+5, v_idx+6), (v_idx+4, v_idx+6, v_idx+7), # Top Face
                (v_idx,   v_idx+2, v_idx+1), (v_idx,   v_idx+3, v_idx+2), # Bottom Face
                (v_idx,   v_idx+1, v_idx+5), (v_idx,   v_idx+5, v_idx+4), # Front Face
                (v_idx+1, v_idx+2, v_idx+6), (v_idx+1, v_idx+6, v_idx+5), # Right Face
                (v_idx+2, v_idx+3, v_idx+7), (v_idx+2, v_idx+7, v_idx+6), # Back Face
                (v_idx+3, v_idx,   v_idx+4), (v_idx+3, v_idx+4, v_idx+7)  # Left Face
            ]
            faces.extend(block_faces)
            v_idx += 8

    # Write out the .obj file
    with open(output_obj, "w") as f:
        f.write(f"# Blocky Terrain Generated From {input_file}\n")
        for v in vertices:
            f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
        for face in faces:
            f.write(f"f {face[0]} {face[1]} {face[2]}\n")
            
    print(f"3D Block Model Saved Successfully to {output_obj}!")

if __name__ == "__main__":
    export_block_mesh()
