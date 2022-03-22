import cv2
import tensorflow as tf
import os
import numpy as np
import matplotlib.pyplot as plt
from lib import image_preprocess, sudoku_detection, sudoku_solver


if __name__ == '__main__':

    # fetch ml model for digits recognition
    path_to_neural_net = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ml_model',
                                      'digit_recognition_net.h5')
    model = tf.keras.models.load_model(path_to_neural_net)

    # openCV video capture
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while cap.isOpened():

        # openCV frame
        success, frame = cap.read()
        # frame = cv2.flip(frame, 1)

        # preprocess to black-white
        frame_preprocessed = image_preprocess.to_black_white(frame)

        # detect sudoku field
        field = sudoku_detection.sudoku_field_detection(frame_preprocessed)

        # for correct display
        numbers_frame = frame

        # if sudoku field is detected
        if field:
            # warp sudoku field
            warped_frame, matrix = image_preprocess.warping(field[1], frame)

            # preprocess sudoku field to black-white
            warped_frame_preprocessed = image_preprocess.to_black_white(warped_frame)

            # detect vertical and horizontal lines
            vertical_lines_frame, horizontal_lines_frame = \
                sudoku_detection.grid_lines_detection(warped_frame_preprocessed, 10)

            # create sudoku mask based on vertical and horizontal lines
            mask = sudoku_detection.grid_mask_creation(vertical_lines_frame, horizontal_lines_frame)

            # apply mask (get frame with digits)
            numbers_frame = cv2.bitwise_and(warped_frame_preprocessed, mask)

            # cut cells from numbers frame
            cells_frames = image_preprocess.splitting_to_cells(numbers_frame)

            # preprocess cropped cells
            cells_frames_preprocessed = image_preprocess.cells_preprocess(cells_frames)

            # for process visualizing and control
            # print(np.argmax(model.predict(np.array([cells_frames_preprocessed[6]]))))
            # plt.imshow(cells_frames_preprocessed[12])
            # plt.show()
            # print(cells_frames_preprocessed)
            # print(len(cells_frames_preprocessed))

            # check if there are only 81 cells
            if len(cells_frames_preprocessed) == 81:
                # recognize digits using ml model
                sudoku_to_solve = sudoku_detection.recognize_digits(cells_frames_preprocessed, model)
                # print recognition result
                print('Отсканнированный судоку:')
                print(sudoku_to_solve)
                # print solution
                print('Решённый судоку:')
                sudoku_solver.solve(sudoku_to_solve)
                break

        # experiments with contours (check detected sudoku field)
        if field:
            cv2.drawContours(frame, [field[0]], 0, (255, 0, 0), 2)
            corners = field[1]
            for corner in corners:
                cv2.circle(frame, corner, 4, (0, 0, 255), cv2.FILLED)

        # openCV frame to display
        cv2.imshow('detect', numbers_frame)

        # key for while loop break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # openCV stuff
    cap.release()
    cv2.destroyAllWindows()
