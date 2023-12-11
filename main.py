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
from PyQt5.QtGui import QPixmap, QImage
from pyqtgraph import ImageItem

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
        self.images_dict = {
            self.image_1_widget: [self.graphicsView_1,  # FT plot widget
                                  self.image_1_widget.objectName(),  # widget name
                                  None  # image instance
                                  ],
            self.image_2_widget: [self.graphicsView_2,  # FT plot widget
                                  self.image_2_widget.objectName(),  # widget name
                                  None  # image instance
                                  ],
            self.image_3_widget: [self.graphicsView_3,  # FT plot widget
                                  self.image_3_widget.objectName(),  # widget name
                                  None  # image instance
                                  ],
            self.image_4_widget: [self.graphicsView_4,  # FT plot widget
                                  self.image_4_widget.objectName(),  # widget name
                                  None  # image instance
                                  ],
        }  # A dictionary to store Image instances
        self.images_counter = 0  # A counter to keep track of the number of images
        self.active_widget = None  # A variable to store the active widget
        self.active_widget_name = None  # A variable to store the active widget name
        # Store the initial window state
        self.image_1_widget_active = True
        self.image_2_widget_active = False
        self.image_3_widget_active = False
        self.image_4_widget_active = False

        self.image_widget_list = [
            self.image_1_widget,
            self.image_2_widget,
            self.image_3_widget,
            self.image_4_widget
        ]

        self.FT_widget_list = [
            self.graphicsView_1,
            self.graphicsView_2,
            self.graphicsView_3,
            self.graphicsView_4
        ]

        # Set up the QGraphicsScene for the view
        scene = QGraphicsScene()
        self.setScene(scene)
        # Connect the mouse press event to the handle_buttons method
        self.handle_button()

    def handle_button(self):
        # Connect mouseDoubleClickEvent for each widget
        for widget in self.images_dict.keys():
            widget.mouseDoubleClickEvent = lambda event, w=widget: self.on_mouse_click(event, w)

            # Connect currentIndexChanged for each QComboBox using a loop
        for i, (key, values) in enumerate(self.images_dict.items()):
            combobox = getattr(self, f"FT_combo_box_{i+1}")
            combobox.currentIndexChanged.connect(functools.partial(self.plot_FT, values[0], combobox))

    def setScene(self, scene):
        for widget in self.images_dict.keys():
            widget.setScene(scene)

        for widget in self.FT_widget_list:
            widget.setScene(scene)



    def on_mouse_click(self, event, widget):
        self.active_widget = widget
        self.active_widget_name = widget.objectName()
        if event.button() == pg.QtCore.Qt.LeftButton:
            self.update_active_widget(widget)
            self.browse_image(widget)
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

    def browse_image(self, widget):
        if self.images_counter == 4:
            return
        self.images_counter += 1
        # browse and get the image path as .jpg or .gif or .png or .jpeg or .svg
        image_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.jpg *.gif *.png *.jpeg *.svg)"
        )
        image_instance = Image(str(image_path))
        # Update the third element of the list associated with self.active_widget
        self.images_dict[self.active_widget][2] = image_instance
        self.display_image()

    def display_image(self):
        min_width, min_height = self.get_min_size()

        for widget_name, value in self.images_dict.items():
            if value[2] is None:
                continue
            image_data = value[2].get_image_data()
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

            # Create the QGraphicsScene and set it for the respective image widget
            image_scene = self.create_image_scene(widget_name)

            # Clear the scene before adding a new item
            image_scene.clear()

            # Create a QGraphicsPixmapItem and add it to the scene
            pixmap_item = QGraphicsPixmapItem(pixmap)
            image_scene.addItem(pixmap_item)

            # Set the initial view to fit the scene content
            initial_view_rect = QRectF(0, 0, width, height)
            widget_name.setSceneRect(initial_view_rect)

            # Fit the view to the pixmap item's bounding rectangle
            widget_name.fitInView(pixmap_item.boundingRect(), Qt.KeepAspectRatio)

            # Set the margins to zero
            widget_name.setContentsMargins(0, 0, 0, 0)

    def create_image_scene(self, image_view):
        # Create the QGraphicsScene and set it for the respective image widget
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

    def plot_FT(self, widget, combobox):
        # Get the current text of the combobox
        current_text = combobox.currentText()

        # Get the image instance from the dictionary
        image_instance = self.images_dict[self.active_widget_name][0]
        # Get the image data
        image_data = image_instance.get_image_data()
        # Compute the Fourier transform
        fourier_transform = image_instance.get_fourier_transform()
        # Compute the magnitude spectrum
        magnitude_spectrum = image_instance.get_magnitude_spectrum()
        # Compute the phase spectrum
        phase_spectrum = image_instance.get_phase_spectrum()
        # Compute the real part
        real_part = image_instance.get_real_part()
        # Compute the imaginary part
        imaginary_part = image_instance.get_imaginary_part()
        # Get the sampling frequencies
        sampling_frequency_x, sampling_frequency_y = image_instance.get_sampling_frequencies()
        # Get the image dimensions
        image_height, image_width = image_data.shape
        # Get the maximum amplitude
        max_amplitude = image_instance.get_max_amplitude(image_data)
        # Get the maximum frequency
        max_frequency = image_instance.get_max_frequency(image_data, sampling_frequency_x)
        # Get the maximum magnitude
        max_magnitude = image_instance.get_max_magnitude(magnitude_spectrum)
        # Get the maximum phase
        max_phase = image_instance.get_max_phase(phase_spectrum)
        # Get the maximum real part
        max_real_part = image_instance.get_max_real_part(real_part)
        # Get the maximum imaginary part
        max_imaginary_part = image_instance.get_max_imaginary_part(imaginary_part)

    def delete_image(self, widget):
        # Check if the key is in the dictionary
        if widget in self.images_dict:
            # Set the third element of the list associated with the key to None
            self.images_dict[widget][2] = None

            # Clear the QGraphicsScene of the widget
            widget.scene().clear()

            # Decrement the images_counter
            self.images_counter -= 1

    def get_min_size(self):
        # Get the minimum width and height of all images in the dictionary
        min_width = min_height = sys.maxsize
        for widget_name, value in self.images_dict.items():
            if value[2] is None:
                continue
            image_data = value[2].get_image_data()
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
