import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap

class Image:
    def __init__(self, image_path):
        """
        Initialize the Image class.

        Parameters:
        - image_path: Path to the image file.
        """
        self.image_data = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        self.window_mask = np.ones(self.image_data.shape)
        self.compute_fourier_transform()

    def get_selected_region(self, selected_region, main_region):
        """
        Extract the selected region from the image_data.

        Parameters:
        - selected_region: QRectF representing the selected region.
        - main_region: Original image region.

        Returns:
        - selected_region_data: Extracted data from the selected region.
        """
        x = int(selected_region.topLeft().x())
        y = int(selected_region.topLeft().y())
        width = int(selected_region.width())
        height = int(selected_region.height())
        selected_region_data = main_region[y:y + height, x:x + width]
        return selected_region_data

    def set_image_data(self, image_data):
        """
        Set the image data and compute the Fourier transform.

        Parameters:
        - image_data: New image data.
        """
        self.image_data = image_data
        self.compute_fourier_transform()

    def set_window_mask(self, window_mask):
        """
        Set the window mask.

        Parameters:
        - window_mask: New window mask.
        """
        self.window_mask = window_mask

    def get_window_mask(self):
        """
        Get the window mask.

        Returns:
        - window_mask: Current window mask.
        """
        return self.window_mask

    def compute_fourier_transform(self):
        """Compute the Fourier transform and related spectra."""
        self.fourier_transform = np.fft.fft2(self.image_data)
        self.shifted_fourier_transform = np.fft.fftshift(self.fourier_transform)

        self.magnitude_spectrum = np.abs(self.fourier_transform)
        self.shifted_magnitude_spectrum = 20 * np.log(self.shifted_fourier_transform)
        self.shifted_magnitude_spectrum_norm_abs = np.abs(self.shifted_fourier_transform)

        self.phase_spectrum = np.angle(self.fourier_transform)
        self.shifted_phase_spectrum = np.angle(self.shifted_fourier_transform)

        self.real_part = np.real(self.fourier_transform)
        self.shifted_real_part = 20 * np.log(np.abs(np.real(self.shifted_fourier_transform)))
        self.shifted_real_part_norm_abs = np.real(self.shifted_fourier_transform)

        self.imaginary_part = np.imag(self.fourier_transform)
        self.shifted_imaginary_part = np.imag(self.shifted_fourier_transform)

    def get_fourier_transform(self):
        """
        Get the Fourier transform.

        Returns:
        - fourier_transform: Current Fourier transform.
        """
        return self.fourier_transform
    
    def get_magnitude_spectrum(self):
        """
        Get the magnitude spectrum.

        Returns:
        - magnitude_spectrum: Current magnitude spectrum.
        """
        return self.magnitude_spectrum
    
    def get_phase_spectrum(self):
        """
        Get the phase spectrum.

        Returns:
        - phase_spectrum: Current phase spectrum.
        """
        return self.phase_spectrum
    
    def get_real_part(self):
        """
        Get the real part.

        Returns:
        - real_part: Current real part.
        """
        return self.real_part
    
    def get_imaginary_part(self):
        """
        Get the imaginary part.

        Returns:
        - imaginary_part: Current imaginary part.
        """
        return self.imaginary_part
    
    def get_image_data(self):
        """
        Get the image data.

        Returns:
        - image_data: Current image data.
        """
        return self.image_data

    def get_shifted(self):
        """
        Get the shifted Fourier transform and related spectra.

        Returns:
        - shifted_data: Dictionary containing various shifted spectra.
        """
        shifted_data = {
            "FT": self.shifted_fourier_transform,
            "FT Magnitude": self.shifted_magnitude_spectrum,
            "FT Phase": self.shifted_phase_spectrum,
            "FT Real": self.shifted_real_part,
            "FT Imaginary": self.shifted_imaginary_part
        }
        return shifted_data

    def get_shifted_norm_abs(self):
        """
        Get the shifted Fourier transform with normalized absolute values.

        Returns:
        - shifted_data: Dictionary containing various shifted spectra with normalized absolute values.
        """
        shifted_data = {
            "FT": self.shifted_fourier_transform,
            "FT Magnitude": self.shifted_magnitude_spectrum_norm_abs,
            "FT Phase": self.shifted_phase_spectrum,
            "FT Real": self.shifted_real_part_norm_abs,
            "FT Imaginary": self.shifted_imaginary_part
        }
        return shifted_data

    def set_image_size(self, width, height):
        """
        Resize the image and compute the Fourier transform.

        Parameters:
        - width: New width.
        - height: New height.
        """
        self.image_data = cv2.resize(self.image_data, (width, height))
        self.compute_fourier_transform()

    def get_image_size(self):
        """
        Get the size of the image.

        Returns:
        - image_size: Tuple containing (height, width) of the image.
        """
        return self.image_data.shape
    def set_image_data(self, image_data):
        """
        Set the image data and compute the Fourier transform.

        Parameters:
        - image_data: New image data.
        """
        self.image_data = image_data
        self.compute_fourier_transform()


