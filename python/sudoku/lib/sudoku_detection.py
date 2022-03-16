import cv2


def find_sudoku_field(preprocessed_frame):
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
