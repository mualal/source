import cv2
import tensorflow as tf
import os
import numpy as np
import matplotlib.pyplot as plt
import threading
from lib import sudoku_detection, sudoku_solver


class ThreadWithResult(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)


if __name__ == '__main__':

    # fetch ml model for digits recognition
    path_to_neural_net = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ml_model',
                                      'printed_digit_recognition_net.h5')
    model = tf.keras.models.load_model(path_to_neural_net)

    # openCV video capture
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # list of threads for digits recognition
    my_threads = []

    while cap.isOpened():

        sudoku_to_solve = None
        # openCV frame
        success, frame = cap.read()
        # frame = cv2.flip(frame, 1)

        # detect all 81 sudoku cells and coordinates of sudoku field
        cells_frames_preprocessed, field = sudoku_detection.full_pipeline(frame)

        # recognize detected cells
        if cells_frames_preprocessed is not None:
            if len(my_threads) < 3:
                new_thread = ThreadWithResult(target=sudoku_detection.recognize_digits,
                                              args=(cells_frames_preprocessed, model))
                my_threads.append(new_thread)
                my_threads[-1].start()

        if len(my_threads) == 3:
            if [thread.is_alive() for thread in my_threads] == [False, False, False]:
                results = [thread.result for thread in my_threads]
                if (results[0] == results[1]).all() and (results[1] == results[2]).all():
                    sudoku_to_solve = results[0]
                my_threads = []

            if field is not None:
                cv2.drawContours(frame, [field[0]], 0, (255, 0, 0), 2)
                corners = field[1]
                for corner in corners:
                    cv2.circle(frame, corner, 4, (0, 0, 255), cv2.FILLED)

            # for process visualizing and control
            # print(np.argmax(model.predict(np.array([cells_frames_preprocessed[6]]))))
            # print(cells_frames_preprocessed[12])
            # plt.imshow(cells_frames_preprocessed[12])
            # plt.show()
            # print(cells_frames_preprocessed)
            # print(len(cells_frames_preprocessed))

            # print recognition result
            if sudoku_to_solve is not None:
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
