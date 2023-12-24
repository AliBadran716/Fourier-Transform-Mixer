from PyQt5.QtWidgets import QWidget, QFileDialog
import pyqtgraph as pg
import numpy as np
import cv2
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QSlider
from PyQt5.QtCore import Qt, QRectF, QObject, pyqtSignal
from PyQt5.QtCore import QPointF

class SignalEmitter(QObject):
    sig_ROI_changed = pyqtSignal()


class overlay:
    def __init__(self, plot_widget, img_data, mode, area_region):
        """
        Initialize the Overlay class.

        Parameters:
        - plot_widget: PlotWidget for displaying the overlay.
        - img_data: Image instance for which overlay is created.
        - mode: Mode of the overlay (e.g., Magnitude, Phase).
        - area_region: Area region for the overlay (Inside Area or Outside Area).
        """
        self.data = img_data
        self.plot_ft = plot_widget
        self.mode = mode
        self.area_region = area_region

        # Signal emitter class to emit custom signals
        self.sig_emitter = SignalEmitter()
        shifted_data = self.data.get_shifted()
        self.ROI_Maxbounds = QRectF(0, 0, shifted_data[self.mode].shape[1], shifted_data[self.mode].shape[0])
        self.plot_ft.clear()  # This will clear all items from the PlotWidget
        self.ft_view = self.plot_ft.addViewBox()
        self.ft_view.setAspectLocked(True)
        self.ft_view.setMouseEnabled(x=False, y=False)
        self.img_item_ft = pg.ImageItem()
        self.ft_view.addItem(self.img_item_ft)
        self.calc_imag_ft()

        self.ft_roi = pg.ROI(pos=self.ft_view.viewRect().center(),
                             size=(shifted_data[self.mode].shape[1], shifted_data[self.mode].shape[0]), hoverPen='b',
                             resizable=True,
                             invertible=True, rotatable=False, maxBounds=self.ROI_Maxbounds)
        
        self.ft_view.addItem(self.ft_roi)
        self.add_scale_handles_ROI(self.ft_roi)
        self.ft_roi.sigRegionChangeFinished.connect(self.region_update)

    def region_update(self):
        """
        Signal handler for ROI region change.
        """
        shifted_data = self.data.get_shifted()
        self.sig_emitter.sig_ROI_changed.emit()
        self.update_mask_size()
        self.sig_emitter.sig_ROI_changed.emit()  # Emit the signal when the ROI changes
    
    def getRoi(self):
        """
        Get the ROI region.

        Returns:
        - x1: x-coordinate of the top-left corner of the ROI.
        - y1: y-coordinate of the top-left corner of the ROI.
        - x2: x-coordinate of the bottom-right corner of the ROI.
        - y2: y-coordinate of the bottom-right corner of the ROI.
        """
        return self.ft_roi
    def set_ROI(self, x1, y1, x2, y2):
        """
        Set the ROI region.

        Parameters:
        - x1: x-coordinate of the top-left corner of the ROI.
        - y1: y-coordinate of the top-left corner of the ROI.
        - x2: x-coordinate of the bottom-right corner of the ROI.
        - y2: y-coordinate of the bottom-right corner of the ROI.
        """
        self.ft_roi.setPos(x1, y1)
        self.ft_roi.setSize((x2 - x1), (y2 - y1))
        self.update_mask_size()

    def update_mask_size(self):
        """
        Update the size of the mask based on the ROI region.
        """
        bounds = self.ft_roi.sceneBoundingRect()
        self.x1, self.y1, self.x2, self.y2 = (
            int(bounds.x()),
            int(bounds.y()),
            int(bounds.x() + bounds.width()),
            int(bounds.y() + bounds.height()),
        )

        # Based on another condition, invert the mask
        if self.area_region == 'Outside Area':
            mask = np.ones(self.data.get_image_data().shape)
            mask[self.y1:self.y2 + 1, self.x1:self.x2 + 1] = 0
        else:
            mask = np.zeros(self.data.get_image_data().shape)
            mask[self.y1:self.y2 + 1, self.x1:self.x2 + 1] = 1

        self.data.set_window_mask(mask)

    def calc_imag_ft(self):
        """
        Calculate the FT of the image and update the overlay.
        """
        shifted_data = self.data.get_shifted()
        self.img_item_ft.setImage(shifted_data[self.mode])

    def add_scale_handles_ROI(self, roi: pg.ROI):
        """
        Add scale handles to the ROI for resizing.
        """
        positions = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
        for pos in positions:
            roi.addScaleHandle(pos=pos, center=1 - pos)

    def change_area_region(self, area_region):
        """
        Change the area region of the overlay.

        Parameters:
        - area_region: Area region for the overlay (Inside Area or Outside Area).
        """
        self.area_region = area_region
        self.update_mask_size()
        self.sig_emitter.sig_ROI_changed.emit()

