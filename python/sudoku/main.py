import cv2
from lib import image_preprocess, sudoku_detection, sudoku_solver


if __name__ == '__main__':

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while cap.isOpened():
        success, frame = cap.read()
        # frame = cv2.flip(frame, 1)

        frame_preprocessed = image_preprocess.to_black_white(frame)

        field = sudoku_detection.sudoku_field_detection(frame_preprocessed)

        numbers_frame = frame

        if field:
            warped_frame, matrix = image_preprocess.warping(field[1], frame)
            warped_frame_preprocessed = image_preprocess.to_black_white(warped_frame)

            vertical_lines_frame, horizontal_lines_frame = \
                sudoku_detection.grid_lines_detection(warped_frame_preprocessed, 10)

            mask = sudoku_detection.grid_mask_creation(vertical_lines_frame, horizontal_lines_frame)
            numbers_frame = cv2.bitwise_and(warped_frame_preprocessed, mask)

            cells_frames = image_preprocess.splitting_to_cells(numbers_frame)

            cells_frames_preprocessed = image_preprocess.cells_preprocess(cells_frames)
            print(len(cells_frames_preprocessed))

        if field:
            cv2.drawContours(frame, [field[0]], 0, (255, 0, 0), 2)
            corners = field[1]
            for corner in corners:
                cv2.circle(frame, corner, 4, (0, 0, 255), cv2.FILLED)

        cv2.imshow('detect', numbers_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
