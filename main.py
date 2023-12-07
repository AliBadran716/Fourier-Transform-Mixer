from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.uic import loadUiType
import pyqtgraph as pg

import numpy as np
import pandas as pd

from image import Image

import os
import sys
from os import path
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
import sys
from image import Image

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))  # connects the Ui file with the Python file

class MainApp(QMainWindow, FORM_CLASS): # go to the main window in the form_class file

    def __init__(self, parent=None):  # constructor to initiate the main window  in the design
        """
                 Constructor to initiate the main window in the design.

                 Parameters:
                 - parent: The parent widget, which is typically None for the main window.
        """
        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        self.images_list = []  # List to store Image instances
        self.browsing_pushButton.clicked.connect(self.browse_image)
        # Load the original image
        original_pixmap = QPixmap("contrast.png")

        # Resize the image to 5x5 pixels
        resized_pixmap = original_pixmap.scaled(35, 35, Qt.KeepAspectRatio)

        # Calculate the initial position
        self.calculate_position()

        # Create a QLabel and set its size and position
        self.image_label = QLabel(self)
        self.image_label.setGeometry(self.center_x, self.top_y, resized_pixmap.width(), resized_pixmap.height())
        self.image_label.setPixmap(resized_pixmap)

        # Store the initial window state
        self.prev_window_state = self.windowState()

    def calculate_position(self):
        # Calculate the position to center at the top
        if self.isMaximized():
            self.center_x = 824
        else:
            self.center_x = 585
        self.top_y = 0  # Set the top y-coordinate as an instance variable

    def changeEvent(self, event):
        if event.type() == event.WindowStateChange:
            # Check if the window state has changed
            if self.prev_window_state != self.windowState():
                # Recalculate the position when the window state changes (e.g., maximized)
                self.calculate_position()
                self.image_label.setGeometry(self.center_x, self.top_y, self.image_label.pixmap().width(),
                                             self.image_label.pixmap().height())

                # Update the previous window state
                self.prev_window_state = self.windowState()


    def browse_image(self):
        # browse and get the image path as .jpg or .gif or .png or .jpeg or .svg
        image_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.jpg *.gif *.png *.jpeg *.svg)")
        self.image_instance = Image(str(image_path))
        #self.display_image()
        #print(image_path)

    # def display_image(self):
    #     if self.image_instance:
    #         image_data = self.image_instance.get_image_data()
    #         h, w = image_data.shape
    #         bytes_per_line = w
    #         q_image = QImage(image_data.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
    #         pixmap = QPixmap.fromImage(q_image)
    #         self.image_label.setPixmap(pixmap)

    # def mix_images(self):
    #     # Implement logic to mix images using the slider value
    #     if self.images_list:
    #         mix_ratio = self.slider.value() / 100.0
    #         mixed_image_data = self.image_instnace.apply_mixed_transform(self.images_list, mix_ratio)
    #         h, w = mixed_image_data.shape
    #         bytes_per_line = w
    #         q_image = QImage(mixed_image_data.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
    #         pixmap = QPixmap.fromImage(q_image)
    #         self.image_label.setPixmap(pixmap)

def main():  # method to start app
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()  # infinte Loop


if __name__ == '__main__':
    main()









