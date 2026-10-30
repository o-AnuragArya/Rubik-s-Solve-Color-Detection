import os
import glob

import cv2
import numpy as np

from cube_color_utils import get_grid_cells, sample_cell_colors, draw_overlay


CAMERA_INDEX = 0
GRID_SIZE = 3            # 3x3 facelets per face
CELL_DISPLAY_SIZE = 80   # px, size of each cell squre
SAMPLE_SIZE = 20         # px, size of the small center
OUTPUT_DIR = "scanned_faces"

# go in order pls
FACE_ORDER = ["U", "R", "F", "D", "L", "B"]
FACE_HINT = {
    "U": "Up face (hold cube with this face on top)",
    "R": "Right face",
    "F": "Front face",
    "D": "Down face (bottom)",
    "L": "Left face",
    "B": "Back face",
}


def capture_single_face(cap, face_key):
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read from camera.")
            return None

        frame = cv2.flip(frame, 1)  # mirror :)
        h, w = frame.shape[:2]

        cells = get_grid_cells(w, h, GRID_SIZE, CELL_DISPLAY_SIZE)
        color_grid, hsv_grid, lab_grid = sample_cell_colors(frame, cells, SAMPLE_SIZE)

        display_frame = draw_overlay(frame, cells, color_grid,
                                      f"{face_key} - {FACE_HINT[face_key]}")

        cv2.imshow("Rubik's Cube Scanner", display_frame)
        key = cv2.waitKey(1) & 0xFF

        if key == 13:        # ENTER -> save 
            return color_grid.copy()
        elif key == 27:       # ESC -> exit
            return None


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print(f"Could not open camera index {CAMERA_INDEX}.")
        return

    all_faces = {}

    for face_key in FACE_ORDER:
        print(f"\nScanning face '{face_key}': {FACE_HINT[face_key]}")
        print("Align the cube face inside the grid. Press ENTER to lock, ESC to quit.")

        face_array = capture_single_face(cap, face_key)

        if face_array is None:
            print("Scan cancelled by user.")
            break

        all_faces[face_key] = face_array
        print(f"Locked colors for face '{face_key}':\n{face_array}")
        np.save(os.path.join(OUTPUT_DIR, f"face_{face_key}.npy"), face_array)

    cap.release()
    cv2.destroyAllWindows()

    if len(all_faces) == len(FACE_ORDER):
        print("\nAll 6 faces scanned successfully!")
        combined = np.array([all_faces[f] for f in FACE_ORDER])  # shape (6,3,3)
        combined_path = os.path.join(OUTPUT_DIR, "all_faces_combined.npy")
        np.save(combined_path, combined)
        print(f"Saved combined array with shape {combined.shape} to '{combined_path}'")
        print(f"Face order in combined array: {FACE_ORDER}")
    else:
        print(f"\nOnly {len(all_faces)}/6 faces were scanned before quitting.")

    saved = sorted(glob.glob(os.path.join(OUTPUT_DIR, "*.npy")))
    if saved:
        print("\nFiles saved:")
        for f in saved:
            print(" -", f)


if __name__ == "__main__":
    main()
