# Fourier Transform Mixer

## Project Overview

- The Fourier Transform Mixer is a desktop program designed and implemented to illustrate the relative importance of magnitude and phase components in a 2D signal, particularly images. This tool provides insights into the frequencies and contributions of different components to the signal. It allows users to mix and visualize Fourier components of grayscale images, offering a versatile educational and analytical platform.

## Features

### Image Viewers

- Open and View Images: Load up to four grayscale images simultaneously.
- Color Conversion: Automatically converts colored images to grayscale.
- Unified Sizes: Maintain a unified size for opened images based on the smallest size among them.
- FT Components Display: View Fourier Transform components, including Magnitude, Phase, Real, and Imaginary parts.
- Easy Browse: Change images by double-clicking on the viewer.
- Brightness/Contrast: Adjust brightness and contrast for each image and its components.

### Components Mixer

- Customizable Weights: Allow users to customize Fourier Transform weights for each image using sliders.
- Realtime Mixing: Provide a progress bar for lengthy mixing operations.
- Thread Handling: Cancel previous operations when a new mixing request is made.

### Regions Mixer

- Region Selection: Enable users to pick regions for output, including inner (low frequencies) and outer (high frequencies).
- Customizable Region Size: Allow users to customize the size or percentage of the selected region.

## Code Practices

- Object-Oriented Approach: Implement OOP concepts for better code organization and readability.
- Logging: Utilize Python's logging library for tracking user interactions and debugging.

## Tools Used

- Python: The core programming language for implementation.
- PyQt5: Used for creating the desktop application's GUI.
- OpenCV: Employed for image processing tasks.
- NumPy: Utilized for numerical operations and array manipulations.
- PyQtGraph: Used for displaying and interacting with images and their components.

## Getting Started

### Clone Repository:

```bash
git clone https://github.com/your-username/Fourier-Transform-Mixer.git
```

### Install Dependencies:

```bash
pip install -r requirements.txt
```

### Run the Application:

```bash
python main.py
```

## Contributors

| Name              | GitHub                                           |
| ----------------- | ------------------------------------------------ |
| Muhannad Abdallah | [@Muhannad159](https://github.com/Muhannad159)   |
| Ali Badran        | [@AliBadran716](https://github.com/AliBadran716) |
| Ahmed Ali         | [@ahmedalii3](https://github.com/ahmedalii3)     |
| Hassan Hussein    | [@hassanowis](https://github.com/hassanowis)     |
