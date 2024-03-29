import numpy as np
import cv2

class ImageMixer:
    def __init__(self, images_list):
        """
        Constructor to initialize the ImageMixer.

        Parameters:
        - images_list: List of Image instances to be mixed.
        """
        self.images_list = images_list

    def mix_images(self, mix_ratios, min_width, min_height, mode):
        """
        Mix images based on specified mix ratios, minimum width, height, and mode.

        Parameters:
        - mix_ratios: List of mixing ratios for each image.
        - min_width: Minimum width for resizing.
        - min_height: Minimum height for resizing.
        - mode: List of mixing modes for each image.

        Returns:
        - Mixed image data.
        """
        # Initialize variables for the mixed amplitude and phase
        mixed_amplitudes = np.zeros_like(self.images_list[0].get_magnitude_spectrum()).astype(np.float64)
        mixed_phases = np.zeros_like(self.images_list[0].get_phase_spectrum()).astype(np.float64)

        # Mix the amplitudes and phases based on the mix ratios
        for i, image in enumerate(self.images_list):
            shifted = image.get_shifted_norm_abs()
            mix_ratio = mix_ratios[i]
            if mode[i] == 'Magnitude':
                mixed_amplitudes += mix_ratio * shifted['FT Magnitude'] * image.get_window_mask()
            elif mode[i] == 'Phase':
                mixed_phases += mix_ratio * shifted['FT Phase'] * image.get_window_mask()
            elif mode[i] == 'Real':
                mixed_amplitudes += mix_ratio * shifted['FT Real'] * image.get_window_mask()
            elif mode[i] == 'Imaginary':
                mixed_phases += mix_ratio * shifted['FT Imaginary'] * image.get_window_mask()

        # Reconstruct the mixed image using the inverse Fourier transform
        if mode[0] == 'Magnitude' or mode[0] == 'Phase':
            mixed_transform = mixed_amplitudes * np.exp(1j * mixed_phases)
        if mode[0] == 'Real' or mode[0] == 'Imaginary':
            mixed_transform = mixed_amplitudes + 1j * mixed_phases
        mixed_image_data = np.fft.ifft2(mixed_transform)
        mixed_image_data = np.abs(mixed_image_data).astype(np.uint8)
        mixed_image_data = cv2.resize(mixed_image_data, (min_width, min_height))

        return mixed_image_data

