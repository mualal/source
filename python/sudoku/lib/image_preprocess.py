import cv2
import numpy as np


def preprocess(frame_to_preprocess):
    frame_gray = cv2.cvtColor(frame_to_preprocess, cv2.COLOR_BGR2GRAY)
    frame_blur = cv2.GaussianBlur(frame_gray, (9, 9), 0)
    frame_threshold = cv2.adaptiveThreshold(frame_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    frame_inverted = cv2.bitwise_not(frame_threshold, 0)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    frame_morph = cv2.morphologyEx(frame_inverted, cv2.MORPH_OPEN, kernel)

    return cv2.dilate(frame_morph, kernel, iterations=1)


def warp_image(corners, original_image):
    corners = np.array(corners, dtype='float32')

    max_width = int(max([
        np.linalg.norm(corners[0] - corners[3]),
        np.linalg.norm(corners[1] - corners[2]),
        np.linalg.norm(corners[1] - corners[0]),
        np.linalg.norm(corners[2] - corners[3])
    ]))

    mapping = np.array([[0, 0], [max_width, 0], [max_width, max_width], [0, max_width]],
                       dtype='float32')

    square_matrix = cv2.getPerspectiveTransform(corners, mapping)

    return cv2.warpPerspective(original_image, square_matrix, (max_width, max_width)), square_matrix
