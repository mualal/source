import cv2


def preprocess(frame_to_preprocess):
    frame_gray = cv2.cvtColor(frame_to_preprocess, cv2.COLOR_BGR2GRAY)
    frame_blur = cv2.GaussianBlur(frame_gray, (9, 9), 0)
    frame_threshold = cv2.adaptiveThreshold(frame_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    frame_inverted = cv2.bitwise_not(frame_threshold, 0)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    frame_morph = cv2.morphologyEx(frame_inverted, cv2.MORPH_OPEN, kernel)

    return cv2.dilate(frame_morph, kernel, iterations=1)
