import numpy as np
import tensorflow as tf
import cv2
import os
import re
import sys
import threading
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGridLayout, QTextEdit, QPushButton, QFileDialog
from lib import image_preprocess, sudoku_detection, sudoku_solver, solver_algorithm_x


class ThreadWithResult(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        self.result = None

        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)


def get_sudoku_from_file(scanned_field):
    file_name, check = QFileDialog.getOpenFileName(None, 'Выберите изображение',
                                                   os.path.dirname(os.getcwd()).replace(os.sep, '/'),
                                                   'Image files (*.jpg *.jpeg *.png)')
    if check:
        image = cv2.imread(file_name)
        preprocessed_cells, _ = sudoku_detection.full_pipeline(image)

        # fetch ml model for digits recognition
        path_to_neural_net = '../ml_model/neural_net_classifier_2.h5'
        model = tf.keras.models.load_model(path_to_neural_net)

        if preprocessed_cells is not None:
            sudoku_to_solve = sudoku_detection.recognize_digits(preprocessed_cells, model)
            scanned_field.setText(np.array2string(np.array(sudoku_to_solve)))
        else:
            scanned_field.setText('No solvable sudoku field found!')


def solve_sudoku_puzzle(scanned_field):
    s1 = scanned_field.toPlainText()
    s2 = re.sub(r'\[', r'', s1)
    s3 = re.sub(r'\n', r'', s2)
    s4 = re.sub(r'\]', r'', s3)
    s5 = re.sub(r'\.', r'', s4)
    s6 = re.sub(r' ', r',', s5)
    try:
        sudoku_arr = np.array(eval('[' + s6 + ']')).reshape(9, 9)
        solution = solver_algorithm_x.solver_pipeline(sudoku_arr)
        if type(solution) is not str:
            scanned_field.setText(np.array2string(solution))
        else:
            scanned_field.setText(solution)
    except Exception as ex:
        print(ex)
        scanned_field.setText('No solvable sudoku field detected!')


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    detected_signal = pyqtSignal(np.ndarray)

    def __init__(self, ml_model):
        super().__init__()
        self._run_flag = True
        self.ml_model = ml_model

    def run(self):
        # openCV video capture
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        my_threads = []
        while self._run_flag:
            success, frame = cap.read()
            if success:
                frame_preprocessed = image_preprocess.to_black_white(frame)
                sudoku_field = sudoku_detection.sudoku_field_detection(frame_preprocessed)
                preprocessed_cells, _ = sudoku_detection.full_pipeline(frame)
                if preprocessed_cells is not None:
                    if len(my_threads) < 3:
                        new_thread = ThreadWithResult(target=sudoku_detection.recognize_digits,
                                                      args=(preprocessed_cells, self.ml_model))
                        my_threads.append(new_thread)
                        my_threads[-1].start()

                if len(my_threads) == 3:
                    if [thread.is_alive() for thread in my_threads] == [False, False, False]:
                        results = [thread.result for thread in my_threads]
                        if (results[0] == results[1]).all() and (results[1] == results[2]).all():
                            result = results[0]
                            self.detected_signal.emit(result)
                        my_threads = []

                if sudoku_field:
                    cv2.drawContours(frame, [sudoku_field[0]], 0, (255, 0, 0), 2)
                    sudoku_corners = sudoku_field[1]
                    for corner in sudoku_corners:
                        cv2.circle(frame, corner, 4, (0, 0, 255), cv2.FILLED)
                self.change_pixmap_signal.emit(frame)
        # shut down openCV video capture
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Solver")
        self.display_width = 800
        self.display_height = 600
        # create the label that holds the image
        self.frame_field = QLabel(self)
        self.frame_field.resize(self.display_width, self.display_height)
        # create a text labels
        self.text_label = QLabel('Camera image')
        self.scan_label = QLabel('Current scanned solvable sudoku field')
        # create text field for scanned sudoku
        self.scanned_sudoku = QTextEdit(self)
        self.scanned_sudoku.setText('No solvable sudoku field found!')
        # create Run button
        self.run_button = QPushButton('Run Sudoku Solver')
        self.run_button.clicked.connect(lambda: solve_sudoku_puzzle(self.scanned_sudoku))
        self.file_select_button = QPushButton('Select image with sudoku field manually')
        self.file_select_button.clicked.connect(lambda: get_sudoku_from_file(self.scanned_sudoku))
        # set font
        widgets = (self.frame_field, self.text_label, self.scan_label, self.scanned_sudoku,
                   self.run_button, self.file_select_button)
        for widget in widgets:
            widget.setFont(QFont('Times New Roman', 14))

        # create a grid layout and add widgets to it
        grid_box = QGridLayout()
        grid_box.addWidget(self.text_label, 0, 0)
        grid_box.addWidget(self.frame_field, 1, 0)
        grid_box.addWidget(self.scan_label, 0, 1)
        grid_box.addWidget(self.scanned_sudoku, 1, 1)
        grid_box.addWidget(self.run_button, 2, 0, 2, 2)
        grid_box.addWidget(self.file_select_button, 4, 0, 4, 2)
        # set the grid layout as the widgets layout
        self.setLayout(grid_box)

        path_to_neural_net = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ml_model',
                                          'neural_net_classifier_2.h5')
        model = tf.keras.models.load_model(path_to_neural_net)

        # create the video capture thread
        self.thread = VideoThread(model)
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.detected_signal.connect(self.update_text)
        # start the thread
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new openCV image"""
        qt_img = self.convert_cv_to_qt(cv_img)
        self.frame_field.setPixmap(qt_img)

    @pyqtSlot(np.ndarray)
    def update_text(self, sudoku_to_solve):
        """Updates the image_label with a new openCV image"""
        self.scanned_sudoku.setText(np.array2string(sudoku_to_solve))

    def convert_cv_to_qt(self, cv_img):
        """Convert from an openCV image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())
