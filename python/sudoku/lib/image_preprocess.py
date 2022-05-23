import cv2
import numpy as np
# from PIL import Image as im
# from datetime import datetime
# import time


def to_black_white(frame_to_preprocess):
    """
    preprocess frame to black-white frame with reduced noise
    :param frame_to_preprocess: input frame to preprocess
    :return: preprocessed black-white frame with reduced noise
    """

    # transform to GRAY colors
    frame_gray = cv2.cvtColor(frame_to_preprocess, cv2.COLOR_BGR2GRAY)

    # Gaussian blurring
    frame_blur = cv2.GaussianBlur(frame_gray, (9, 9), 0)

    # adaptive thresholding (to create binary black-white image)
    frame_threshold = cv2.adaptiveThreshold(frame_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # invert colors (white to black and black to white)
    frame_inverted = cv2.bitwise_not(frame_threshold, 0)

    # kernel for morphological transformation
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

    # opening transformation (erosion followed by dilation), useful in removing noise
    frame_morph = cv2.morphologyEx(frame_inverted, cv2.MORPH_OPEN, kernel)

    # dilation, increases the white region in the image
    frame_morph = cv2.dilate(frame_morph, kernel, iterations=1)

    return frame_morph


def warping(corners, original_frame):
    """
    warp sudoku field
    :param corners: detected sudoku field corners
    :param original_frame: original frame from camera
    :return: warped sudoku field image
    """

    # corners coordinates list to numpy array
    corners = np.array(corners, dtype='float32')

    # max euclidean distance between neighboring corners
    max_width = int(max([
        np.linalg.norm(corners[0] - corners[3]),
        np.linalg.norm(corners[1] - corners[2]),
        np.linalg.norm(corners[1] - corners[0]),
        np.linalg.norm(corners[2] - corners[3])
    ]))

    # mapping to square with given size (max_width)
    mapping = np.array([[0, 0], [max_width, 0], [max_width, max_width], [0, max_width]],
                       dtype='float32')

    # calculate perspective transform
    square_matrix = cv2.getPerspectiveTransform(corners, mapping)

    # create warped frame
    warped_frame = cv2.warpPerspective(original_frame, square_matrix, (max_width, max_width))

    return warped_frame, square_matrix


def splitting_to_cells(warped_frame):
    """
    create list with sudoku cells
    :param warped_frame: warped sudoku field
    :return: sudoku cells list
    """

    # sudoku cells list
    cells = []

    # sudoku cells count
    cells_count = 81

    # one cell width
    width = warped_frame.shape[0] // int(np.sqrt(cells_count))

    # append cells to list
    for i in range(int(np.sqrt(cells_count))):
        for j in range(int(np.sqrt(cells_count))):
            top_left_corner = (i * width, j * width)
            bottom_right_corner = ((i + 1) * width, (j + 1) * width)
            cells.append(warped_frame[top_left_corner[0]:bottom_right_corner[0],
                         top_left_corner[1]:bottom_right_corner[1]])

    return cells


def cells_preprocess(cells_frames):
    """
    center digits in cells with digits and identify empty cells (as 0 in returned list)
    :param cells_frames: list of sudoku cells frames
    :return: list with cells frames (if cell with digit) or 0 (if empty cell)
    """

    preprocessed_cells_frames = []

    for cell_frame in cells_frames:

        if np.isclose(cell_frame, 0).sum() / (cell_frame.shape[0] * cell_frame.shape[1]) >= 0.97:
            preprocessed_cells_frames.append(0)
            continue

        height, width = cell_frame.shape
        mid = width // 2

        if np.isclose(cell_frame[int(mid - width * 0.2):int(mid + width * 0.2),
                      int(mid - width * 0.2):int(mid + width * 0.2)],
                      0).sum() / (0.4 * width * 0.4 * height) >= 0.95:
            preprocessed_cells_frames.append(0)
            continue

        contours, _ = cv2.findContours(cell_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        x, y, w, h = cv2.boundingRect(contours[0])

        start_x = (width - w) // 2
        start_y = (height - h) // 2
        preprocessed_cell_frame = np.zeros_like(cell_frame)
        preprocessed_cell_frame[start_y:start_y + h, start_x:start_x + w] = cell_frame[y:y + h, x:x + w]

        # change image dimensions
        preprocessed_cell_frame = cv2.resize(preprocessed_cell_frame, dsize=(28, 28), interpolation=cv2.INTER_CUBIC)
        preprocessed_cell_frame = np.expand_dims(preprocessed_cell_frame, -1)

        # save images for ml model training
        # data = im.fromarray(preprocessed_cell_frame.reshape(28, 28))
        # data.save('../ml_model/custom_images/' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')[:-3] + '.jpeg')
        # time.sleep(0.1)

        # normalize
        preprocessed_cell_frame = preprocessed_cell_frame / 255.0

        preprocessed_cells_frames.append(preprocessed_cell_frame)

    return preprocessed_cells_frames
