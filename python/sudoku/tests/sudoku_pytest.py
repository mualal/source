# to launch testing type in terminal: python -m pytest tests/sudoku_pytest.py

import pytest
import tensorflow as tf
import os
import cv2
from lib import sudoku_detection


def fetch_ml():
    # fetch ml model for digits recognition
    path_to_neural_net = os.path.join(os.getcwd(), 'ml_model',
                                      'digit_recognition_net.h5')
    model = tf.keras.models.load_model(path_to_neural_net)
    return model


class TestSudokuRecognition:

    def test_recognition_1(self):
        file_path = os.path.join(os.getcwd(), 'images', 'Sudoku_example1.png')
        print(file_path)
        image = cv2.imread(file_path)
        preprocessed_cells, _ = sudoku_detection.full_pipeline(image)
        model = fetch_ml()
        assert (sudoku_detection.recognize_digits(preprocessed_cells, model) == [[5, 3, 0, 0, 7, 0, 0, 0, 0],
                                                                                 [5, 0, 0, 1, 9, 5, 0, 0, 0],
                                                                                 [0, 9, 8, 0, 0, 0, 0, 6, 0],
                                                                                 [8, 0, 0, 0, 6, 0, 0, 0, 3],
                                                                                 [4, 0, 0, 8, 0, 3, 0, 0, 1],
                                                                                 [7, 0, 0, 0, 2, 0, 0, 0, 6],
                                                                                 [0, 6, 0, 0, 0, 0, 2, 8, 0],
                                                                                 [0, 0, 0, 4, 1, 9, 0, 0, 5],
                                                                                 [0, 0, 0, 0, 8, 0, 0, 7, 9]]).all()

    def test_recognition_2(self):
        file_path = os.path.join(os.getcwd(), 'images', 'Sudoku_example2.JPG')
        print(file_path)
        image = cv2.imread(file_path)
        preprocessed_cells, _ = sudoku_detection.full_pipeline(image)
        model = fetch_ml()
        assert (sudoku_detection.recognize_digits(preprocessed_cells, model) == [[0, 0, 0, 0, 0, 9, 4, 7, 0],
                                                                                 [0, 0, 2, 0, 3, 0, 0, 9, 8],
                                                                                 [0, 6, 0, 0, 0, 2, 0, 0, 1],
                                                                                 [0, 0, 0, 0, 0, 0, 5, 0, 7],
                                                                                 [0, 7, 0, 0, 0, 0, 0, 6, 0],
                                                                                 [8, 0, 3, 0, 0, 0, 0, 0, 0],
                                                                                 [6, 0, 0, 1, 0, 0, 0, 2, 0],
                                                                                 [7, 4, 0, 0, 6, 0, 9, 0, 0],
                                                                                 [0, 1, 9, 4, 0, 0, 0, 0, 0]]).all()
