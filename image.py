import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap

class Image:
    def __init__(self, image_path):
        self.image_data = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        self.sampling_frequency_x = 1.0 / self.image_data.shape[1]
        self.sampling_frequency_y = 1.0 / self.image_data.shape[0]
        self.compute_fourier_transform()

    def compute_fourier_transform(self):
        self.fourier_transform = np.fft.fft2(self.image_data)
        self.magnitude_spectrum = np.abs(self.fourier_transform)
        self.phase_spectrum = np.angle(self.fourier_transform)
        self.real_part = np.real(self.fourier_transform)
        self.imaginary_part = np.imag(self.fourier_transform)


    def get_sampling_frequencies(self):
        return self.sampling_frequency_x, self.sampling_frequency_y
    
    def get_fourier_transform(self):
        return self.fourier_transform
    
    def get_magnitude_spectrum(self):
        return self.magnitude_spectrum
    
    def get_phase_spectrum(self):
        return self.phase_spectrum
    
    def get_real_part(self):
        return self.real_part
    
    def get_imaginary_part(self):
        return self.imaginary_part
    
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
