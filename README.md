# Rubik's Cube Detector

A Python/OpenCV project that scans the six faces of a Rubik's Cube through a
webcam, classifies each facelet by color, saves the captured data as NumPy
arrays, and uses the `kociemba` package to calculate a solution.

## Features

- Live webcam preview with a centered 3x3 scanning grid.
- HSV and LAB color sampling for each facelet.
- Color labels displayed on the camera overlay.
- Individual face data saved as `.npy` files.
- Combined cube state generated in the expected face order.
- Optional visualization of scanned faces.
- Cube solution generated using Kociemba's two-phase algorithm.

## Requirements

- Python 3.9 or newer is recommended.
- A working webcam.
- A Rubik's Cube with distinguishable face colors.

Install the Python dependencies from `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

## Project structure

```text
.
├── algo.py                  # Loads the scanned cube and calculates a solution
├── cube_color_utils.py      # Grid creation, color sampling, classification, and overlay drawing
├── main.py                  # Webcam scanner
├── view_results.py          # Visualizes saved face arrays
├── requirements.txt         # Python dependencies
└── scanned_faces/
    ├── face_U.npy
    ├── face_R.npy
    ├── face_F.npy
    ├── face_D.npy
    ├── face_L.npy
    ├── face_B.npy
    └── all_faces_combined.npy
```

The files in `scanned_faces/` are generated or updated by the scanner. Existing
`.npy` files can be used by `view_results.py` and `algo.py`.

## Usage

### 1. Scan all six faces

From the project directory, run:

```bash
python main.py
```

The scanner processes faces in this order:

```text
U → R → F → D → L → B
```

For each face:

1. Hold the cube so the requested face is aligned with the on-screen grid.
2. Keep the nine facelets centered inside the grid.
3. Press **Enter** to save the current face.
4. Press **Esc** to stop scanning.

When all six faces are captured, the scanner writes:

- `scanned_faces/face_U.npy`
- `scanned_faces/face_R.npy`
- `scanned_faces/face_F.npy`
- `scanned_faces/face_D.npy`
- `scanned_faces/face_L.npy`
- `scanned_faces/face_B.npy`
- `scanned_faces/all_faces_combined.npy`

The combined array has shape `(6, 3, 3)` and follows the order
`[U, R, F, D, L, B]`.

### 2. View captured results

To display the saved face grids:

```bash
python view_results.py
```

This opens a Matplotlib window showing each detected face and its classified
colors.

### 3. Calculate a solution

After a complete scan, run:

```bash
python algo.py
```

The script prints the generated cube string, counts each color, and prints the
solution returned by `kociemba`.

## Color and solver mapping

The scanner classifies facelets using these names:

```text
White, Red, Orange, Yellow, Green, Blue
```

`algo.py` converts those names to the Kociemba face notation as follows:

| Detected color | Kociemba face |
|---|---|
| White | U |
| Red | B |
| Green | R |
| Blue | L |
| Yellow | D |
| Orange | F |

The center facelets and the physical orientation used during scanning must be
consistent with this mapping. If the solver reports an invalid cube, verify
the camera lighting, face order, cube orientation, and color classifications.

## Troubleshooting

### The camera does not open

- Check that the webcam is connected and available to other applications.
- Close applications that may already be using the webcam.
- Change `CAMERA_INDEX` in `main.py` from `0` to another camera index.
- Run the script from the project directory so relative paths resolve correctly.

### Colors are classified incorrectly

- Use steady, even lighting and avoid strong reflections.
- Keep each facelet inside the center of its grid cell.
- Avoid covering the facelet center with your fingers.
- Review the detected labels in the live overlay or with `view_results.py`.
- Adjust the HSV/LAB thresholds in `cube_color_utils.py` for your camera and
  lighting conditions if necessary.

### Kociemba rejects the cube state

`kociemba` expects exactly 54 valid facelets: nine for each of `U`, `R`, `F`,
`D`, `L`, and `B`. Check that:

- All six faces were scanned successfully.
- Each color occurs exactly nine times.
- The cube was held in the requested orientation for every scan.
- The color mapping in `algo.py` matches the physical cube.

## Notes

- `main.py` mirrors the webcam image to make alignment more natural.
- Pressing **Esc** stops the scan without creating a new combined file.
- Running the scanner again overwrites face files with the same names.
- The current implementation uses fixed camera and grid settings defined at the
  top of `main.py`.
