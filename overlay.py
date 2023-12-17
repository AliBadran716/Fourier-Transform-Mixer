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
    def __init__(self, plot_widget, img_data):
        self.data = img_data
        self.plot_ft = plot_widget
        # Signal emiiter class to emit custom signals
        self.sig_emitter = SignalEmitter()
        self.ROI_Maxbounds = QRectF(0, 0, 100, 100)

        self.ft_view = self.plot_ft.addViewBox()
        self.ft_view.setAspectLocked(True)
        self.ft_view.setMouseEnabled(x=False, y=False)

        self.img_item_ft = pg.ImageItem()
        self.ft_view.addItem(self.img_item_ft)



        self.ft_roi = pg.ROI(pos=self.ft_view.viewRect().center(), size=(50, 50), hoverPen='b', resizable=True,
                             invertible=True, rotatable=False, maxBounds=self.ROI_Maxbounds)
        self.ft_view.addItem(self.ft_roi)
        self.add_scale_handles_ROI(self.ft_roi)
        self.ft_roi.sigRegionChangeFinished.connect(lambda: self.region_update(self.data))

    def region_update(self, img_data):
        data = img_data.get_shifted()
        self.sig_emitter.sig_ROI_changed.emit()
        new_img = self.ft_roi.getArrayRegion(data[0], self.img_item_ft)
        self.img_item_ft.setImage(np.fft.ifft2(np.fft.ifftshift(new_img)))
        # self.img_data_modified_dict[DATA_IMG] = np.fft.ifft2(np.fft.ifftshift(new_img))
        # self.calc_imag_ft(self.img_data_modified_dict)

    def add_scale_handles_ROI(self, roi : pg.ROI):
        positions = np.array([[0,0], [1,0], [1,1], [0,1]])
        for pos in positions:
            roi.addScaleHandle(pos = pos, center = 1 - pos)