from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGridLayout, QTextEdit, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QFont
import sys
import os
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from lib import image_preprocess, sudoku_detection
import tensorflow as tf


def get_sudoku_from_file(scanned_field):
    file_name, check = QFileDialog.getOpenFileName(None, 'Выберите изображение',
                                                   os.path.dirname(os.getcwd()).replace(os.sep, '/'),
                                                   'Image files (*.jpg *.jpeg *.png)')
    if check:
        image = cv2.imread(file_name)
        preprocessed_cells, _ = sudoku_detection.full_pipeline(image)

        # fetch ml model for digits recognition
        path_to_neural_net = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ml_model',
                                          'printed_digit_recognition_net.h5')
        model = tf.keras.models.load_model(path_to_neural_net)

        if preprocessed_cells is not None:
            sudoku_to_solve = sudoku_detection.recognize_digits(preprocessed_cells, model)
            scanned_field.setText(np.array2string(np.array(sudoku_to_solve)))
        else:
            scanned_field.setText('No solvable sudoku field found!')


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    detected_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # openCV video capture
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        last_detect = False
        while self._run_flag:
            success, frame = cap.read()
            if success:
                frame_preprocessed = image_preprocess.to_black_white(frame)
                sudoku_field = sudoku_detection.sudoku_field_detection(frame_preprocessed)
                if sudoku_field:
                    self.detected_signal.emit(True)
                    last_detect = True
                    cv2.drawContours(frame, [sudoku_field[0]], 0, (255, 0, 0), 2)
                    sudoku_corners = sudoku_field[1]
                    for corner in sudoku_corners:
                        cv2.circle(frame, corner, 4, (0, 0, 255), cv2.FILLED)
                else:
                    if last_detect:
                        self.detected_signal.emit(False)
                        last_detect = False
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

        # create the video capture thread
        self.thread = VideoThread()
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

    @pyqtSlot(bool)
    def update_text(self, detected):
        """Updates the image_label with a new openCV image"""
        if detected:
            self.scanned_sudoku.setText('Square found!')
        else:
            self.scanned_sudoku.setText('No solvable sudoku field found!')

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
