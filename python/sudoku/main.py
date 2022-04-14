import cv2
import tensorflow as tf
import os
import numpy as np
import matplotlib.pyplot as plt
from lib import sudoku_detection, sudoku_solver


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

        # detect all 81 sudoku cells and coordinates of sudoku field
        cells_frames_preprocessed, field = sudoku_detection.full_pipeline(frame)

        # recognize detected cells
        if cells_frames_preprocessed is not None:

            sudoku_to_solve = sudoku_detection.recognize_digits(cells_frames_preprocessed, model)

            cv2.drawContours(frame, [field[0]], 0, (255, 0, 0), 2)
            corners = field[1]
            for corner in corners:
                cv2.circle(frame, corner, 4, (0, 0, 255), cv2.FILLED)

            # for process visualizing and control
            # print(np.argmax(model.predict(np.array([cells_frames_preprocessed[6]]))))
            # plt.imshow(cells_frames_preprocessed[12])
            # plt.show()
            # print(cells_frames_preprocessed)
            # print(len(cells_frames_preprocessed))

            # print recognition result
            if sudoku_solver.check_sudoku_field(sudoku_to_solve):
                solution = []
                sudoku_solver.solve(solution, sudoku_to_solve)
                if solution:
                    print('Отсканированный судоку:')
                    print(sudoku_to_solve)
                    # print solution
                    print('Решённый судоку:')
                    print(solution[0])

        # openCV frame to display
        cv2.imshow('detect', frame)

        # key for while loop break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # openCV stuff
    cap.release()
    cv2.destroyAllWindows()
