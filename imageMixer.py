import numpy as np
import cv2
class ImageMixer:
    def __init__(self, images_list):
        self.images_list = images_list

    def mix_images(self, mix_ratios ,min_width, min_height , mode):
        # Initialize variables for the mixed amplitude and phase
        mixed_amplitudes = np.zeros_like(self.images_list[0].get_magnitude_spectrum()).astype(np.float64)
        mixed_phases = np.zeros_like(self.images_list[0].get_phase_spectrum()).astype(np.float64)

        # Mix the amplitudes and phases based on the mix ratios
        for i, image in enumerate(self.images_list):
            mix_ratio = mix_ratios[i]
            if mode[i] == 'Magnitude':
                mixed_amplitudes += mix_ratio * image.get_magnitude_spectrum()
            elif mode[i] == 'Phase':
                mixed_phases += mix_ratio * image.get_phase_spectrum()
            elif mode[i] == 'Real':
                mixed_amplitudes += mix_ratio * image.get_real_part()
            elif mode[i] == 'Imaginary':    
                mixed_phases += mix_ratio * image.get_imaginary_part()

        # Reconstruct the mixed image using the inverse Fourier transform
        if mode[0] == 'Magnitude' or mode[0] == 'Phase':
            mixed_transform = mixed_amplitudes * np.exp(1j * mixed_phases)
        if mode[0] == 'Real' or mode[0] == 'Imaginary':
            mixed_transform = mixed_amplitudes + 1j * mixed_phases  
        mixed_image_data = np.fft.ifft2(mixed_transform)
        mixed_image_data = np.abs(mixed_image_data).astype(np.uint8)
        mixed_image_data = cv2.resize(mixed_image_data, (min_width, min_height))

        return mixed_image_data
