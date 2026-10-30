import os
import glob

import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIR = "scanned_faces"

COLOR_MAP = {
    "White":  (1.00, 1.00, 1.00),
    "Red":    (0.85, 0.10, 0.10),
    "Orange": (1.00, 0.55, 0.00),
    "Yellow": (1.00, 0.90, 0.10),
    "Green":  (0.10, 0.65, 0.20),
    "Blue":   (0.10, 0.30, 0.90),
}


def load_faces():
    files = sorted(glob.glob(os.path.join(OUTPUT_DIR, "face_*.npy")))
    faces = {}
    for f in files:
        key = os.path.splitext(os.path.basename(f))[0].replace("face_", "")
        faces[key] = np.load(f)
    return faces


def plot_faces(faces):
    n = len(faces)
    if n == 0:
        print(f"No face_*.npy files found in '{OUTPUT_DIR}'. Run main.py first.")
        return

    _ , axes = plt.subplots(1, n, figsize=(3 * n, 3))
    if n == 1:
        axes = [axes]

    for ax, (face_key, grid) in zip(axes, faces.items()):
        rows, cols = grid.shape
        for r in range(rows):
            for c in range(cols):
                color_name = str(grid[r, c])
                rgb = COLOR_MAP.get(color_name, (0.5, 0.5, 0.5))
                ax.add_patch(plt.Rectangle((c, rows - 1 - r), 1, 1,
                                            facecolor=rgb, edgecolor="black"))

                text_color = "black" if color_name in ("White", "Yellow") else "white"
                ax.text(c + 0.5, rows - 1 - r + 0.5, color_name[:1],
                        ha="center", va="center", color=text_color, fontsize=10)
        ax.set_xlim(0, cols)
        ax.set_ylim(0, rows)
        ax.set_aspect("equal")
        ax.set_title(f"Face {face_key}")
        ax.axis("off")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_faces(load_faces())
