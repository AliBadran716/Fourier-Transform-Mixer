from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.uic import loadUiType
import pyqtgraph as pg
import cv2
import numpy as np
import pandas as pd

from image import Image

import os
import sys
from os import path
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QSlider,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
import sys
import functools
from image import Image
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QPainter

FORM_CLASS, _ = loadUiType(
    path.join(path.dirname(__file__), "main.ui")
)  # connects the Ui file with the Python file


class MainApp(QMainWindow, FORM_CLASS):  # go to the main window in the form_class file
    def __init__(
        self, parent=None
    ):  # constructor to initiate the main window  in the design
        """
        Constructor to initiate the main window in the design.

        Parameters:
        - parent: The parent widget, which is typically None for the main window.
        """
        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        self.images_dict = {}  # A dictionary to store Image instances
        self.images_counter = 0  # A counter to keep track of the number of images
        # Store the initial window state
        self.image_1_widget_active = True
        self.image_2_widget_active = False
        self.image_3_widget_active = False
        self.image_4_widget_active = False
        # Set up the QGraphicsScene for the view
        scene = QGraphicsScene()
        self.setScene(scene)
        # Connect the mouse press event to the handle_buttons method
        self.handle_button()

    def handle_button(self):
        self.browsing_pushButton.clicked.connect(self.browse_image)
        # List of widgets to handle
        widgets_to_handle = [
            self.image_1_widget,
            self.image_2_widget,
            self.image_3_widget,
            self.image_4_widget
        ]
        # Connect mouseDoubleClickEvent for each widget
        for widget in widgets_to_handle:
            widget.mouseDoubleClickEvent = lambda event, w=widget: self.on_mouse_click(event, w)

            # Connect currentIndexChanged for each QComboBox using a loop
        for i in range(1, 4):
            combobox = getattr(self, f"FT_combo_box_{i}")
            widget = getattr(self, f"graphicsView_{i}")
            combobox.currentIndexChanged.connect(functools.partial(self.plot_FT, widget, combobox))



    def setScene(self, scene):
        self.image_1_widget.setScene(scene)
        self.image_2_widget.setScene(scene)
        self.image_3_widget.setScene(scene)
        self.image_4_widget.setScene(scene)

    def on_mouse_click(self, event, widget):
        if event.button() == pg.QtCore.Qt.LeftButton:
            self.update_active_widget(widget)
            self.browse_image()
        if event.button() == pg.QtCore.Qt.RightButton:
            self.delete_image(widget)

    def update_active_widget(self, active_widget):
        # Define a list containing all the widgets you want to manage
        widgets = [
            self.image_1_widget,
            self.image_2_widget,
            self.image_3_widget,
            self.image_4_widget
        ]

        # Iterate through each widget
        for widget in widgets:
            # Check if the current widget is the active_widget
            widget_active = widget == active_widget

            # Set the stylesheet based on whether the widget is active or not
            widget.setStyleSheet(
                "border: 1px solid  rgb(0, 133, 255);" if widget_active else "border: 1px solid rgba(0, 0, 0, 0.20);"
            )

        # Update the active state variables based on the active_widget
        self.image_1_widget_active, self.image_2_widget_active, self.image_3_widget_active, self.image_4_widget_active = [
            widget == active_widget for widget in widgets
        ]

    def browse_image(self):
        if self.images_counter == 4:
            return
        self.images_counter += 1
        # browse and get the image path as .jpg or .gif or .png or .jpeg or .svg
        image_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.jpg *.gif *.png *.jpeg *.svg)"
        )
        self.image_instance = Image(str(image_path))
        image_name = f"image_{self.images_counter}"
        # Store the ImageProcessor instance in the dictionary
        self.images_dict[image_name] = self.image_instance
        self.display_image()

        # Call plot_FT for each widget and combobox
        for i in range(1, 4):
            widget = getattr(self, f"graphicsView_{i}")
            combobox = getattr(self, f"FT_combo_box_{i}")
            self.plot_FT(widget, combobox)

    def display_image(self):
        min_width, min_height = self.get_min_size()

        for image_index, (image_name, image_instance) in enumerate(
                self.images_dict.items(), start=1
        ):
            image_data = image_instance.get_image_data()

            # Resize the image while maintaining the aspect ratio
            resized_image = cv2.resize(image_data, (min_width, min_height))
            height, width = resized_image.shape
            bytes_per_line = width

            q_image = QImage(
                resized_image.data,
                width,
                height,
                bytes_per_line,
                QImage.Format_Grayscale8,
            )
            pixmap = QPixmap.fromImage(q_image)

            # Get the corresponding image widget
            image_widget = getattr(self, f"image_{image_index}_widget")

            # Create the QGraphicsScene and set it for the respective image widget
            image_scene = self.create_image_scene(image_widget)

            # Clear the scene before adding a new item
            image_scene.clear()

            # Create a QGraphicsPixmapItem and add it to the scene
            pixmap_item = QGraphicsPixmapItem(pixmap)
            image_scene.addItem(pixmap_item)
            # Set the initial view to fit the scene content
            initial_view_rect = QRectF(0, 0, width, height)
            image_widget.setSceneRect(initial_view_rect)
            image_widget.fitInView(initial_view_rect, Qt.KeepAspectRatio)

    def plot_FT(self, widget, combobox):
        # Get the corresponding image name
        image_name = f"image_{widget.objectName().split('_')[-1]}"

        # Check if the image exists in the dictionary
        if image_name in self.images_dict:
            # Get the Image instance from the dictionary
            image_instance = self.images_dict[image_name]

            # Get the magnitude spectrum and flatten it
            magnitude_spectrum = image_instance.get_magnitude_spectrum().flatten()

            # Get the phase spectrum and flatten it
            phase_spectrum = image_instance.get_phase_spectrum().flatten()

            # Get the real part
            real_part = image_instance.get_real_part().flatten()

            # Get the imaginary part
            imaginary_part = image_instance.get_imaginary_part().flatten()

            # Get the current combobox text
            combobox_text = combobox.currentText()

            widget.clear()
            # Plot the Fourier transform
            if combobox_text == 'FT Magnitude':
                widget.plot(magnitude_spectrum, pen='r')
                Y_min, Y_max = min(magnitude_spectrum), max(magnitude_spectrum)
            elif combobox_text == 'FT Phase':
                widget.plot(phase_spectrum, pen='g')
                Y_min, Y_max = min(phase_spectrum), max(phase_spectrum)
            elif combobox_text == 'FT Real':
                widget.plot(real_part, pen='b')
                Y_min, Y_max = min(real_part), max(real_part)
            elif combobox_text == 'FT Imaginary':
                widget.plot(imaginary_part, pen='y')
                Y_min, Y_max = min(imaginary_part), max(imaginary_part)

            # Set the y range to fit the data
            widget.getViewBox().setYRange(Y_min, Y_max)

            # Set the x range to a specific range
            widget.getViewBox().setXRange(0, 100)

    def create_image_scene(self, image_view):
        image_scene = QGraphicsScene(image_view)
        image_view.setScene(image_scene)
        # Set size policy and other properties as needed
        image_view.setAlignment(Qt.AlignCenter)
        image_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Set render hints for smoother rendering (optional)
        image_view.setRenderHint(QPainter.Antialiasing, True)
        image_view.setRenderHint(QPainter.SmoothPixmapTransform, True)
        image_view.setRenderHint(QPainter.HighQualityAntialiasing, True)
        return image_scene

    def delete_image(self, widget):
        # Get the corresponding image name
        image_name = f"image_{widget.objectName().split('_')[-1]}"

        # Remove the image from the dictionary
        if image_name in self.images_dict:
            del self.images_dict[image_name]

        # Clear the QGraphicsScene of the widget
        widget.scene().clear()

        # Decrement the images_counter
        self.images_counter -= 1

    def get_min_size(self):
        # Get the minimum width and height of all images in the dictionary
        min_width = min_height = sys.maxsize
        for image_name, image_instance in self.images_dict.items():
            image_data = image_instance.get_image_data()
            h, w = image_data.shape
            min_width = min(min_width, w)
            min_height = min(min_height, h)
        return min_width, min_height



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


if __name__ == "__main__":
    main()
