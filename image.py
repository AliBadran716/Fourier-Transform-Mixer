import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap

class Image:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image_data = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        self.compute_fourier_transform()

    def compute_fourier_transform(self):
        f_transform = np.fft.fft2(self.image_data)
        self.amplitudes = np.abs(f_transform)
        self.phases = np.angle(f_transform)

    def get_amplitudes(self):
        return self.amplitudes

    def get_phases(self):
        return self.phases

    def get_image_data(self):
        return self.image_data

    def apply_mixer(self, images_list, mix_ratio):
        # Mix the amplitudes and phases of the images
        mixed_amplitudes = mix_ratio * self.amplitudes + (1 - mix_ratio) * images_list.amplitudes
        mixed_phases = mix_ratio * self.phases + (1 - mix_ratio) * images_list.phases

        # Reconstruct the mixed image using the inverse Fourier transform
        mixed_transform = mixed_amplitudes * np.exp(1j * mixed_phases)
        mixed_image_data = np.fft.ifft2(mixed_transform).real

        return mixed_image_data
