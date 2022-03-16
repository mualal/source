import cv2
from lib import image_preprocess, sudoku_detection, sudoku_solver


if __name__ == '__main__':

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while cap.isOpened():
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)

        frame_preprocessed = image_preprocess.preprocess(frame)

        field = sudoku_detection.find_sudoku_field(frame_preprocessed)

        if field:
            cv2.drawContours(frame, [field[0]], 0, (255, 0, 0), 2)
            corners = field[1]
            for corner in corners:
                cv2.circle(frame, corner, 4, (0, 0, 255), cv2.FILLED)

        cv2.imshow('detect', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
