import cv2
import numpy as np


def get_grid_cells(frame_w, frame_h, grid_size, cell_size):
    total_size = grid_size * cell_size
    start_x = frame_w // 2 - total_size // 2
    start_y = frame_h // 2 - total_size // 2

    cells = []
    for row in range(grid_size):
        row_cells = []
        for col in range(grid_size):
            x1 = start_x + col * cell_size
            y1 = start_y + row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            row_cells.append((x1, y1, x2, y2))
        cells.append(row_cells)
    return cells


def classify_color(hsv_mean, lab_mean):
    h, s, v = hsv_mean
    l, a, b = lab_mean

    if s < 55 and v > 140 and abs(a - 128) < 12 and abs(b - 128) < 15:
        return "White"

    if h < 8 or h >= 172:
        return "Red"
    elif h < 18:
        return "Orange"
    elif h < 34:
        return "Yellow"
    elif h < 85:
        return "Green"
    elif h < 130:
        return "Blue"
    else:
        # trying to Using LAB to differ red and white
        if a > 140:
            return "Red"
        return "White"


def sample_cell_colors(frame, cells, sample_size):
    rows = len(cells)
    cols = len(cells[0])

    color_grid = np.empty((rows, cols), dtype="<U10")
    hsv_grid = np.zeros((rows, cols, 3), dtype=np.float32)
    lab_grid = np.zeros((rows, cols, 3), dtype=np.float32)

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lab_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    half = sample_size // 2

    for r in range(rows):
        for c in range(cols):
            x1, y1, x2, y2 = cells[r][c]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            sx1, sy1 = max(cx - half, 0), max(cy - half, 0)
            sx2, sy2 = cx + half, cy + half

            hsv_patch = hsv_frame[sy1:sy2, sx1:sx2]
            lab_patch = lab_frame[sy1:sy2, sx1:sx2]

            if hsv_patch.size == 0 or lab_patch.size == 0:
                hsv_mean = (0.0, 0.0, 0.0)
                lab_mean = (0.0, 128.0, 128.0)
            else:
                hsv_mean = tuple(hsv_patch.reshape(-1, 3).mean(axis=0))
                lab_mean = tuple(lab_patch.reshape(-1, 3).mean(axis=0))

            hsv_grid[r, c] = hsv_mean
            lab_grid[r, c] = lab_mean
            color_grid[r, c] = classify_color(hsv_mean, lab_mean)

    return color_grid, hsv_grid, lab_grid


def draw_overlay(frame, cells, color_grid, face_label):
    display = frame.copy()
    rows = len(cells)
    cols = len(cells[0])

    for r in range(rows):
        for c in range(cols):
            x1, y1, x2, y2 = cells[r][c]
            cv2.rectangle(display, (x1, y1), (x2, y2), (0, 0, 0), 2)

            text = str(color_grid[r, c])
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.55
            thickness = 2
            (tw, th), _ = cv2.getTextSize(text, font, font_scale, thickness)
            tx = x1 + ((x2 - x1) - tw) // 2
            ty = y1 + ((y2 - y1) + th) // 2
            cv2.rectangle(display, (tx - 3, ty - th - 3), (tx + tw + 3, ty + 3),
                          (255, 255, 255), -1)
            cv2.putText(display, text, (tx, ty), font, font_scale,
                        (0, 0, 0), thickness, cv2.LINE_AA)

    cv2.putText(display, f"Face: {face_label}", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(display, "ENTER = lock face   ESC = quit", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2, cv2.LINE_AA)

    return display
