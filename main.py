from PyQt5.QtCore import *
import functools
import sys
from os import path
import cv2
import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QRubberBand,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QSizePolicy,
)
from PyQt5.uic import loadUiType
from image import Image
from imageMixer import ImageMixer
from overlay import overlay

# Load the UI file
FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))

class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        """
        Constructor to initiate the main window in the design.

        Parameters:
        - parent: The parent widget, which is typically None for the main window.
        """
        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        self.images_dict = {  # A dictionary to store Image instances and their associated widgets
            self.image_1_widget: [self.graphicsView_1,  # FT plot widget
                                  self.image_1_widget.objectName(),  # widget name
                                  None,  # image instance
                                  self.FT_combo_box_1,  # FT combo box
                                  None,  # overlay instance
                                  None #modified image
                                  ],
            self.image_2_widget: [self.graphicsView_2,  # FT plot widget
                                  self.image_2_widget.objectName(),  # widget name
                                  None,  # image instance
                                  self.FT_combo_box_2,  # FT combo box
                                  None,  # overlay instance
                                  None #modified image
                                  ],
            self.image_3_widget: [self.graphicsView_3,  # FT plot widget
                                  self.image_3_widget.objectName(),  # widget name
                                  None,  # image instance
                                  self.FT_combo_box_3,  # FT combo box
                                  None,  # overlay instance
                                  None #modified image
                                  ],
            self.image_4_widget: [self.graphicsView_4,  # FT plot widget
                                  self.image_4_widget.objectName(),  # widget name
                                  None,  # image instance
                                  self.FT_combo_box_4,  # FT combo box
                                  None,  # overlay instance
                                  None #modified image
                                  ],
        }
        self.images_counter = 0  # A counter to keep track of the number of images
        self.active_widget = None  # A variable to store the active widget
        self.mode_combobox_list = [self.mode_comboBox_1, self.mode_comboBox_2, self.mode_comboBox_3,
                                   self.mode_comboBox_4]
        self.output_dictionary = {
            "Viewport 1": self.output_image_1,
            "Viewport 2": self.output_image_2,
        }
        self.sliders_list = [self.slider_1, self.slider_2, self.slider_3, self.slider_4]
        self.selection_modes_dict = {"Magnitude": ["Magnitude", "Phase"],
                                     "Phase": ["Magnitude", "Phase"],
                                     "Real": ["Real", "Imaginary"],
                                     "Imaginary": ["Real", "Imaginary"]
                                     }
        self.brightness = 0
        self.contrast = 0
        self.mouse_dragging = False  # Flag to track if the mouse is dragging

        self.initial_mouse_pos = QPoint(0, 0)
        self.progressBar.setValue(0)
        # Connect the mouse press event to the handle_buttons method
        self.handle_button()
        self.slider_1.setFixedHeight(161)
        self.slider_2.setFixedHeight(161)
        self.slider_3.setFixedHeight(161)
        self.slider_4.setFixedHeight(161)

    def handle_button(self):
        """
        Connect signals to corresponding slots.
        """
        # Connect the clicked signal to the browse_image method
        for slider in self.sliders_list:
            slider.valueChanged.connect(self.mix_images)
        self.pushButton_reset.clicked.connect(self.reset_brightness_contrast)

        # Connect mouseDoubleClickEvent for each widget
        for widget, value in self.images_dict.items():
            widget.mouseDoubleClickEvent = lambda event, w=widget: self.on_double_mouse_click(event, w)
            widget.mousePressEvent = lambda event, w=widget: self.mouse_press_event(event, w)
            widget.mouseMoveEvent = lambda event, w=widget: self.mouse_move_event(event, w)
            widget.mouseReleaseEvent = lambda event, w=widget: self.mouse_release_event(event, w)

        # Connect currentIndexChanged for each QComboBox using a loop
        for key, values in self.images_dict.items():
            values[3].currentIndexChanged.connect(functools.partial(self.plot_FT, values[0], values[3]))

        self.connect_comboboxes()

        # Connect the currentIndexChanged signal to the change_area_region method
        self.area_taken_region.currentIndexChanged.connect(
            lambda index: self.change_area_region(self.area_taken_region.currentText()))
    
    def connect_comboboxes(self, is_connected=True):
        """
        Connect or disconnect currentIndexChanged signals for combo-boxes.

        Parameters:
        - is_connected: Boolean flag indicating whether to connect or disconnect signals.
        """
        if is_connected:
            for i in range(1, 5):
                combobox = getattr(self, f"mode_comboBox_{i}")
                combobox.currentIndexChanged.connect(functools.partial(self.handle_mode_combobox_change, i))
        else:
            for i in range(1, 5):
                combobox = getattr(self, f"mode_comboBox_{i}")
                combobox.currentIndexChanged.disconnect()

    def on_double_mouse_click(self, event, widget):
        """
        Handle double mouse click event.

        Parameters:
        - event: The mouse event.
        - widget: The widget associated with the event.
        """
        self.active_widget = widget
        if event.button() == pg.QtCore.Qt.LeftButton:
            self.browse_image(widget)
        if event.button() == pg.QtCore.Qt.RightButton:
            self.delete_image(widget)

    def mouse_press_event(self, event, w):
        """
        Handle mouse press event.

        Parameters:
        - event: The mouse event.
        - w: The widget associated with the event.
        """
        if event.button() == Qt.LeftButton:
            self.mouse_dragging = True
            self.initial_mouse_pos = event.pos()
            self.active_widget = w

    def mouse_move_event(self, event, w):
        """
        Handle mouse move event.

        Parameters:
        - event: The mouse event.
        - w: The widget associated with the event.
        """
        if self.images_dict[w][2] is None:
            return

        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            self.mouse_dragging = True
            self.initial_mouse_pos = event.pos()

        elif event.type() == QEvent.MouseMove and self.mouse_dragging:
            diff = event.pos() - self.initial_mouse_pos
            self.brightness = diff.x()  # Use positive values for right movement
            self.contrast = -diff.y()  # Invert for up movement
            self.apply_brightness_contrast(w)

        elif event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
            self.mouse_dragging = False

    def mouse_release_event(self, event, w):
        """
        Handle mouse release event.

        Parameters:
        - event: The mouse event.
        - w: The widget associated with the event.
        """
        if event.button() == Qt.LeftButton:
            self.mouse_dragging = False

    def handle_mode_combobox_change(self, index):
        """
        Handle the change in mode combo-box.

        Parameters:
        - index: The index of the combo-box that triggered the signal.
        """
        # Get the current combobox that triggered the signal
        current_combobox = self.sender()

        # Get the current text of the combobox
        current_text = current_combobox.currentText()

        # Disconnect the signal temporarily
        self.connect_comboboxes(False)

        # Update the items of the remaining combo-boxes
        for i in range(1, 5):
            if i != index:
                combobox = getattr(self, f"mode_comboBox_{i}")
                combobox.clear()
                combobox.addItems(self.selection_modes_dict[current_text])

        # Reconnect the signal
        self.connect_comboboxes(True)

    def browse_image(self, widget):
        """
        Browse and open an image file.

        Parameters:
        - widget: The widget associated with the image.
        """
        if self.images_counter == 4:
            return
        self.images_counter += 1
        # browse and get the image path as .jpg or .gif or .png or .jpeg or .svg
        image_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.jpg *.gif *.png *.jpeg *.svg)"
        )
        image_instance = Image(str(image_path))
        image_instance_2 = Image(str(image_path))
        if self.images_counter != 1:
            min_width, min_height = self.get_min_size()
            image_instance.set_image_size(min_width, min_height)
            image_instance_2.set_image_size(min_width, min_height)
        # Update the image instance of the list associated with widget
        self.images_dict[widget][2] = image_instance
        self.images_dict[widget][5] = image_instance_2
        self.display_image()
        # Call Plot FT
        self.plot_FT(self.images_dict[widget][0], self.images_dict[widget][3])

    def display_image(self):
        """
        Display images in the associated widgets.
        """
        min_width, min_height = self.get_min_size()

        for widget_name, value in self.images_dict.items():
            if value[5] is None:
                continue
            value[5].set_image_size(min_width, min_height)
            value[2].set_image_size(min_width, min_height)
            image_data = value[5].get_image_data()
            resized_image = cv2.resize(image_data, (min_width, min_height))
            height, width = resized_image.shape
            image_data = bytes(resized_image.data)
            self.plot_images(width, height, widget_name, image_data, True)


    def plot_images(self, width, height, widget_name, image_data, is_input_image=False):
        """
        Plot images in the specified widget.

        Parameters:
        - width: Width of the image.
        - height: Height of the image.
        - widget_name: The name of the widget to plot the image.
        - image_data: Image data to be displayed.
        - is_input_image: Boolean flag indicating whether the image is an input image.
        """
        bytes_per_line = width

        q_image = QImage(
            image_data,
            width,
            height,
            bytes_per_line,
            QImage.Format_Grayscale8,
        )
        pixmap = QPixmap.fromImage(q_image)

        image_scene = self.create_image_scene(widget_name)
        image_scene.clear()

        pixmap_item = QGraphicsPixmapItem(pixmap)
        image_scene.addItem(pixmap_item)

        if is_input_image:
            # Set the size of the view to match the size of the image
            widget_name.setFixedSize(width, height)

            # Disable scroll bars
            widget_name.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            widget_name.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

            # Set the size policy to ignore the size hint
            widget_name.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        else:
            # Fit the view to the pixmap item's bounding rectangle without keeping the aspect ratio
            widget_name.fitInView(pixmap_item.boundingRect(), Qt.IgnoreAspectRatio)

        # Set the margins to zero
        widget_name.setContentsMargins(0, 0, 0, 0)

    def create_image_scene(self, image_view):
        """
        Create a QGraphicsScene for the specified image view.

        Parameters:
        - image_view: The QGraphicsView associated with the scene.

        Returns:
        - The created QGraphicsScene.
        """
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
        """
        Plot the Fourier Transform of the image in the specified widget.

        Parameters:
        - widget: The widget associated with the image.
        - combobox: The combo-box associated with the widget.
        """
        # Get the current text of the combobox
        current_text = combobox.currentText()

        area_region = self.area_taken_region.currentText()
        # Get the dictionary key associated with the widget
        desired_key = next((key for key, value in self.images_dict.items() if value[0] == widget and value[5]), None)

        # If desired_key is None, then there was no matching widget in the dictionary
        if desired_key is None:
            return

        # Create an instance of the overlay class
        overlay_instance = overlay(self.images_dict[desired_key][0],
                                   self.images_dict[desired_key][5],
                                   current_text,
                                   area_region,
                                   )
        # Connect the sig_ROI_changed signal to the mix_images method
        overlay_instance.sig_emitter.sig_ROI_changed.connect(self.mix_images)
        overlay_instance.sig_emitter.sig_ROI_changed.connect(lambda: self.modify_all_regions(overlay_instance.getRoi()))
        # Update the dictionary
        self.images_dict[desired_key][4] = overlay_instance
        self.mix_images()
    
    def modify_all_regions(self, roi: pg.ROI):
        new_state = roi.getState()
        for view in self.images_dict.values():
            if view[4].getRoi() is not roi:
                view[4].getRoi().setState(new_state, update = False) # Set the state of the other views without sending update signal
                view[4].getRoi().stateChanged(finish = False) # Update the views after changing without sending stateChangeFinished signal
                view[4].region_update(view[4].getRoi(),finish = False)  
   
    def reset_brightness_contrast(self):
        """
        Reset the brightness and contrast values.
        """
        self.brightness = 0
        self.contrast = 0
        self.apply_brightness_contrast(self.active_widget)

    def apply_brightness_contrast(self, widget, alpha=1.0, beta=0):
        """
        Apply brightness and contrast to the displayed image.

        Parameters:
        - widget: The widget associated with the image.
        - alpha: Alpha value for contrast adjustment.
        - beta: Beta value for brightness adjustment.
        """
        if self.images_dict[widget][2] is None:
            return

        image = np.float32(self.images_dict[widget][2].get_image_data())
        alpha = 1.0 + self.contrast / 100.0
        beta = self.brightness
        image = alpha * (image - 128) + 128 + beta
        image = np.clip(image, 0, 255).astype("uint8")

        height, width = image.shape
        self.images_dict[widget][5].set_image_data(image)
        self.plot_images(width, height, widget, image)

    def delete_image(self, widget):
        """
        Delete the specified image.

        Parameters:
        - widget: The widget associated with the image.
        """
        # Check if the key is in the dictionary
        if widget in self.images_dict:
            # Set the third element of the list associated with the key to None
            self.images_dict[widget][2] = None
            self.images_dict[widget][5] = None

            # Clear the QGraphicsScene of the widget
            widget.scene().clear()

            # Decrement the images_counter
            self.images_counter -= 1
        # clear the FT plot
        self.images_dict[widget][0].clear()
        # delete all instances
        self.images_dict[widget][2] = None
        self.images_dict[widget][5] = None
        self.images_dict[widget][4] = None
        # recompute the images
        self.mix_images()

    def get_min_size(self):
        """
        Get the minimum width and height of all images.

        Returns:
        - A tuple containing the minimum width and height.
        """
        # Get the minimum width and height of all images in the dictionary
        min_width = min_height = sys.maxsize

        for widget_name, value in self.images_dict.items():
            if value[5] is None:
                continue
            image_data = value[5].get_image_data()
            h, w = image_data.shape
            min_width = min(min_width, w)
            min_height = min(min_height, h)
        return min_width, min_height

    def mix_images(self):
        """
        Mix images based on the slider values.
        """
        # Implement logic to mix images using the slider value
        self.progressBar.setValue(0)
        if self.images_counter > 0:
            min_width, min_height = self.get_min_size()
            images_lists = []

            for image_list in self.images_dict.values():

                if image_list[5] is None:
                    continue
                else:
                    image_list[5].set_image_size(min_width, min_height)
                    image_list[2].set_image_size(min_width, min_height)
                    images_lists.append(image_list[5])

                image_list[4].update_mask_size()

            mix = ImageMixer(images_lists)
            slider_values, mode = self.get_slider_mode_values()
            self.progressBar.setValue(25)

            output_image = mix.mix_images(slider_values, min_width, min_height, mode)
            self.progressBar.setValue(50)
            # Create a QImage from the output_image
            bytes_per_line = min_width
            image_data = bytes(output_image.data)
            current_view = self.comboBox_2.currentText()
            self.progressBar.setValue(75)
            self.plot_images(min_width, min_height, self.output_dictionary[current_view], image_data)
            self.progressBar.setValue(100)

    def get_slider_mode_values(self):
        """
        Get the normalized slider values and selected mode from combo-boxes.

        Returns:
        - A tuple containing normalized slider values and the selected mode.
        """
        # Get the slider values
        slider_values = [
            self.slider_1.value(),
            self.slider_2.value(),
            self.slider_3.value(),
            self.slider_4.value(),
        ]
        # Normalize the slider values
        normalized_slider_values = [value / 100 for value in slider_values]
        mode = []
        for combox_mode in self.mode_combobox_list:
            mode.append(combox_mode.currentText())
        return normalized_slider_values, mode

    def change_area_region(self, region):
        """
        Change the area region based on the user's selection.

        Parameters:
        - region: The selected region.
        """
        for key, value in self.images_dict.items():
            if value[4] is None:
                continue
            value[4].change_area_region(region)
        # Mix images
        self.mix_images()


def main():
    """
    Main method to start the application.
    """
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()  # infinite Loop


if __name__ == "__main__":
    main()
