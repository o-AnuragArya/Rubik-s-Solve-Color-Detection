import kociemba
import numpy as np


colours = {
    'Red': "B",
    'Green': "R",
    'Blue': "L",
    'Yellow': "D",
    'Orange': "F",
    'White': "U"
}

all_faces = np.load("scanned_faces/all_faces_combined.npy")

cube_string = ''.join(colours[color] for color in all_faces.flatten())
print("Cube String:", cube_string)
for i in colours.keys():
    print(f"{i}: {cube_string.count(colours[i])} facelets")

print("Solving the cube...")
print(kociemba.solve(cube_string))