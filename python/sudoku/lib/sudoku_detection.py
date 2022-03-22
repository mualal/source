import cv2
import numpy as np


def sudoku_field_detection(preprocessed_frame):
    """
    detect entire sudoku field
    :param preprocessed_frame: preprocessed frame with or without sudoku field
    :return: sudoku field contour and corner points of this field
    """

    # find contours on the frame (only the outer contours as cv2.RETR_EXTERNAL)
    contours, _ = cv2.findContours(preprocessed_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # sort found contours based on its area
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # variable for sudoku field contour
    sudoku_field = None

    # iterate through sorted contours to find sudoku field
    for contour in contours:

        # contour area
        area = cv2.contourArea(contour)
        # contour perimeter
        perimeter = cv2.arcLength(contour, closed=True)

        # approximate a contour shape to another shape with less number of vertices
        approx = cv2.approxPolyDP(contour, 0.01*perimeter, closed=True)

        # corners count
        num_corners = len(approx)

        # only quadrilaterals with sufficient area can be sudoku field
        if num_corners == 4 and area > 500:
            sudoku_field = contour
            break

    # if sudoku field is found
    if sudoku_field is not None:

        # find list position of point with min x+y (top left corner)
        min1_pos, _ = min(enumerate([poly[0][0] + poly[0][1] for poly in sudoku_field]), key=lambda x: x[1])

        # find list position of point with max x-y (top right corner)
        max1_pos, _ = max(enumerate([poly[0][0] - poly[0][1] for poly in sudoku_field]), key=lambda x: x[1])

        # find list position of point with min x-y (bottom left corner)
        min2_pos, _ = min(enumerate([poly[0][0] - poly[0][1] for poly in sudoku_field]), key=lambda x: x[1])

        # find list position of point with max x+y (bottom right corner)
        max2_pos, _ = max(enumerate([poly[0][0] + poly[0][1] for poly in sudoku_field]), key=lambda x: x[1])

        # retrieve corners coordinates
        top_left = (sudoku_field[min1_pos][0][0], sudoku_field[min1_pos][0][1])
        top_right = (sudoku_field[max1_pos][0][0], sudoku_field[max1_pos][0][1])
        bot_left = (sudoku_field[min2_pos][0][0], sudoku_field[min2_pos][0][1])
        bot_right = (sudoku_field[max2_pos][0][0], sudoku_field[max2_pos][0][1])

        # check for near squares shapes (not empty and not elongated rectangle)
        if bot_right[1] - top_right[1] == 0:
            return []
        if not (0.8 < (top_right[0] - top_left[0]) / (bot_right[1] - top_right[1]) < 1.2):
            return []

        return sudoku_field, [top_left, top_right, bot_right, bot_left]

    return []


def grid_lines_detection(preprocessed_frame, length):
    """
    detect horizontal and vertical lines on black-white frame
    :param preprocessed_frame: preprocessed black-white frame
    :param length: specify lines size
    :return: 2 frames: 1 with horizontal lines and 1 with vertical lines
    """

    # pixels count in columns and rows
    col = preprocessed_frame.shape[0]
    row = preprocessed_frame.shape[1]

    # specify sizes on horizontal and vertical axes
    col_size = col // length
    row_size = row // length

    # create kernel for extracting horizontal and vertical lines through morphology operations
    col_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, col_size))
    row_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (row_size, 1))

    # apply morphology operations
    col_frame = cv2.morphologyEx(preprocessed_frame, cv2.MORPH_OPEN, col_kernel)
    row_frame = cv2.morphologyEx(preprocessed_frame, cv2.MORPH_OPEN, row_kernel)

    return col_frame, row_frame


def grid_mask_creation(vertical_lines_frame, horizontal_lines_frame):
    """
    create sudoku mask without digits
    :param vertical_lines_frame: preprocessed frame with horizontal lines
    :param horizontal_lines_frame: preprocessed frame with vertical lines
    :return: sudoku grid mask
    """

    # adding horizontal and vertical lines to one frame
    grid_lines = cv2.add(vertical_lines_frame, horizontal_lines_frame)

    # dilation, increases the white region in the image
    grid_lines = cv2.dilate(grid_lines, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)

    # also lines detected using hough transform will be added
    pts = cv2.HoughLines(grid_lines, .3, np.pi/90, 200)

    if pts is not None:
        for rho, theta in np.squeeze(pts):
            a, b = np.cos(theta), np.sin(theta)
            x0, y0 = a * rho, b * rho
            x1, y1 = int(x0 + 1000 * (-b)), int(y0 + 1000 * a)
            x2, y2 = int(x0 - 1000 * (-b)), int(y0 - 1000 * a)
            cv2.line(grid_lines, (x1, y1), (x2, y2), (255, 255, 255), 4)

    # black to white and white to black
    grid_lines = cv2.bitwise_not(grid_lines)

    return grid_lines


def recognize_digits(preprocessed_cells, ml_model):
    """
    recognize digits in sudoku cells
    :param preprocessed_cells: list of preprocessed sudoku cells
    :param ml_model: machine learning model to predict digits
    :return: numpy array with sudoku to solve
    """

    cells_count = 81
    sudoku_to_solve = np.zeros((int(np.sqrt(cells_count)), int(np.sqrt(cells_count))))

    for i in range(int(np.sqrt(cells_count))):
        for j in range(int(np.sqrt(cells_count))):
            current_cell = preprocessed_cells[int(np.sqrt(cells_count)) * i + j]
            if type(current_cell) is not int:
                sudoku_to_solve[i][j] = np.argmax(ml_model.predict(np.array([current_cell])))

    return sudoku_to_solve
