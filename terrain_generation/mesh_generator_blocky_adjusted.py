# If you configure your workflow to run multiple passes and merge them,
#	this block engine will render actual floating arches and hollow tunnels:

def export_block_mesh(input_file="heightmap.txt", output_obj="terrain.obj", block_size=1.0):
    with open(input_file, "r") as f:
        grid = [line.strip().split() for line in f if line.strip()]
        
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    vertices = []
    faces = []
    v_idx = 1
    
    for r in range(rows):
        for c in range(cols):
            val = grid[r][c]
            if val == 'U':
                continue # Pure empty air/cave passage
                
            height = float(val)
            
            x0, x1 = c * block_size, (c + 1) * block_size
            z0, z1 = r * block_size, (r + 1) * block_size
            
            # --- THE CAVERN UPDATE ---
            # To allow tunnels under mountains, a block should be a discrete voxel slab
            # rather than stretching all the way to the floor.
            y0 = height - 1.0  # Base of the block sits exactly one unit below its value
            y1 = height        # Top of the block
            
            # 8 Vertices for this specific layer block
            block_verts = [
                (x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1), # Bottom plate
                (x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)  # Top plate
            ]
            vertices.extend(block_verts)
            
            # Standard solid 6-sided cubic face connectivity
            block_faces = [
                (v_idx+4, v_idx+5, v_idx+6), (v_idx+4, v_idx+6, v_idx+7), # Top
                (v_idx,   v_idx+2, v_idx+1), (v_idx,   v_idx+3, v_idx+2), # Bottom
                (v_idx,   v_idx+1, v_idx+5), (v_idx,   v_idx+5, v_idx+4), # Front
                (v_idx+1, v_idx+2, v_idx+6), (v_idx+1, v_idx+6, v_idx+5), # Right
                (v_idx+2, v_idx+3, v_idx+7), (v_idx+2, v_idx+7, v_idx+6), # Back
                (v_idx+3, v_idx,   v_idx+4), (v_idx+3, v_idx+4, v_idx+7)  # Left
            ]
            faces.extend(block_faces)
            v_idx += 8

    with open(output_obj, "w") as f:
        f.write(f"# Modular Block Terrain\n")
        for v in vertices:
            x, y, z = v
            f.write(f"v {x:.4f} {y:.4f} {z:.4f}\n")
        for face in faces:
            fx, fy, fz = face
            f.write(f"f {fx} {fy} {fz}\n")
            
    print(f"3D Structural Mesh compiled to {output_obj}")

if __name__ == "__main__":
    export_block_mesh()
