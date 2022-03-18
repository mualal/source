import cv2
import numpy as np


def sudoku_field_detection(preprocessed_frame):
    contours, _ = cv2.findContours(preprocessed_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    sudoku_field = None

    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, closed=True)
        approx = cv2.approxPolyDP(contour, 0.01*perimeter, closed=True)
        num_corners = len(approx)

        if num_corners == 4 and area > 500:
            sudoku_field = contour
            break

    if sudoku_field is not None:
        min1_pos, _ = min(enumerate([poly[0][0] + poly[0][1] for poly in sudoku_field]), key=lambda x: x[1])
        max1_pos, _ = max(enumerate([poly[0][0] - poly[0][1] for poly in sudoku_field]), key=lambda x: x[1])
        min2_pos, _ = min(enumerate([poly[0][0] - poly[0][1] for poly in sudoku_field]), key=lambda x: x[1])
        max2_pos, _ = max(enumerate([poly[0][0] + poly[0][1] for poly in sudoku_field]), key=lambda x: x[1])

        top_left = (sudoku_field[min1_pos][0][0], sudoku_field[min1_pos][0][1])
        top_right = (sudoku_field[max1_pos][0][0], sudoku_field[max1_pos][0][1])
        bot_left = (sudoku_field[min2_pos][0][0], sudoku_field[min2_pos][0][1])
        bot_right = (sudoku_field[max2_pos][0][0], sudoku_field[max2_pos][0][1])

        if bot_right[1] - top_right[1] == 0:
            return []
        if not (0.8 < (top_right[0] - top_left[0]) / (bot_right[1] - top_right[1]) < 1.2):
            return []

        return sudoku_field, [top_left, top_right, bot_right, bot_left]

    return []


def grid_lines_detection(frame, length):
    frame_copy = frame.copy()

    col = frame_copy.shape[0]
    row = frame_copy.shape[1]

    col_size = col // length
    row_size = row // length

    col_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, col_size))
    row_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (row_size, 1))

    col_frame = cv2.erode(frame_copy, col_kernel)
    col_frame = cv2.dilate(col_frame, col_kernel)

    row_frame = cv2.erode(frame_copy, row_kernel)
    row_frame = cv2.dilate(row_frame, row_kernel)

    return col_frame, row_frame


def grid_mask_creation(vertical_lines_frame, horizontal_lines_frame):
    grid_lines = cv2.add(vertical_lines_frame, horizontal_lines_frame)
    grid_lines = cv2.adaptiveThreshold(grid_lines, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 235, 2)
    grid_lines = cv2.dilate(grid_lines, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)

    pts = cv2.HoughLines(grid_lines, .3, np.pi/90, 200)

    for rho, theta in np.squeeze(pts):
        a, b = np.cos(theta), np.sin(theta)
        x0, y0 = a * rho, b * rho
        x1, y1 = int(x0 + 1000 * (-b)), int(y0 + 1000 * a)
        x2, y2 = int(x0 - 1000 * (-b)), int(y0 - 1000 * a)
        cv2.line(grid_lines, (x1, y1), (x2, y2), (255, 255, 255), 4)

    return cv2.bitwise_not(grid_lines)
