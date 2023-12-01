import bpy
import os
import numpy as np

def import_pdb_files(directory_path):
    framek = 0

    # Iterate through all files in the specified directory
    for filename in os.listdir(directory_path):
        if filename.endswith("b.pdb"):
            filepath = os.path.join(directory_path, filename)

            with open(filepath, "r") as f:
                atoms = parse_pdb(f)

            if framek == 0:
                mesh1 = bpy.data.meshes.new("atoms")
                mesh1.from_pydata(atoms, [], [])

                obj = bpy.data.objects.new("atoms", mesh1)
                bpy.context.scene.collection.objects.link(obj)
                bpy.context.view_layer.objects.active = obj

                mesh1.update()

            bpy.context.view_layer.objects.active = obj
            verts = obj.data.vertices

            # Convert the 'atoms' list to a NumPy array for faster operations
            atoms_np = np.array(atoms)

            # Update vertex coordinates using NumPy for better performance
            verts.foreach_set("co", atoms_np.flatten())

            # Keyframe insertion for all vertices in a single operation
            for i in range(len(verts)):
                verts[i].keyframe_insert("co", frame=framek)

            framek += 1

    return {"FINISHED"}

# Function to parse PDB file using NumPy
def parse_pdb(pdb):
    atoms = []

    for line in pdb:
        if line.startswith('ATOM'):
            try:
                # Extract atomic coordinates from PDB format
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())

                # Append atomic coordinates as a tuple to the list
                atoms.append((x, y, z))
            except ValueError:
                pass

    return atoms

directory_path = "C:/Users/Paul/Desktop/ppb"
import_pdb_files(directory_path)