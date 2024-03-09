# Fourier Transform Mixer
![Images-Mixing](https://github.com/Muhannad159/Fourier-Transform-Mixer/assets/104541242/6ab94d7f-aeb4-4a1f-82bc-4b823c63850f)

## Project Overview

The Fourier Transform Mixer is a desktop program designed to provide users with advanced tools for visualizing and manipulating Fourier Transform components of grayscale images. By offering a comprehensive set of features, this application facilitates in-depth analysis and exploration of image signals in the frequency domain.

Additionally, the program includes a feature for edge detection, which enhances the application's capabilities by allowing users to identify and highlight edges within images. Edge detection is a fundamental technique in image processing, enabling various applications such as object detection, image segmentation, and feature extraction.

The importance of edge detection lies in its ability to extract meaningful information from images, allowing users to identify boundaries and transitions between different objects or regions. This information is crucial for tasks such as image segmentation, where separating objects from background or identifying specific features within an image is necessary.

## Features

### Image Viewers

- **Open and View Images**: The application supports the simultaneous loading and viewing of up to four grayscale images. If a colored image is opened, the program automatically converts it to grayscale to maintain consistency.
- **Unified Sizes**: Regardless of their original dimensions, the sizes of all opened images are adjusted to match the smallest size among them. This ensures uniformity in visualization.
- **FT Components Display**: Each image viewport is equipped with two displays: one for the image itself and another for Fourier Transform components. Users can select from a dropdown menu to view Magnitude, Phase, Real, and Imaginary parts of the Fourier Transform.
- **Easy Browse**: Users can effortlessly switch between images by double-clicking on the viewer, providing a seamless browsing experience.

### Output Ports

- **Two Output Viewports**: Mixer results can be displayed in one of two output viewports. Each output viewport mirrors the input image viewport, allowing users to compare the original and mixed images side by side.
- **User Control**: Users have the flexibility to choose which viewport displays the mixer result, enabling convenient analysis and comparison.

### Brightness/Contrast Adjustment

- **Dynamic Adjustment**: Users can dynamically adjust the brightness and contrast of images and their components via mouse dragging. This feature enhances visualization and facilitates detailed analysis by allowing users to fine-tune image parameters.

### Components Mixer

- **Customizable Weights**: Users can customize Fourier Transform weights for each image using sliders. This feature enables users to control the contribution of each image to the mixing process, facilitating fine-grained control over the output.
- **Intuitive Interface**: Customized weights for two components are implemented in an intuitive user interface, ensuring ease of use and efficient interaction with the application.

### Regions Mixer

- **Region Selection**: Users can select regions for output, including inner (low frequencies) or outer (high frequencies) regions, by drawing rectangles on each Fourier Transform display. The selected region is highlighted to indicate the user's choice.
- **Customizable Region Size**: The size or percentage of the selected region can be customized using a slider or resize handles, providing users with flexibility in region selection and adjustment.

### Realtime Mixing

- **Progress Bar**: During lengthy mixing operations, a progress bar is displayed to indicate the status of the process. This feature keeps users informed about the progress and duration of the operation.
- **Thread Handling**: The application handles threads effectively by canceling previous operations and starting new ones upon user request. This ensures smooth operation and responsiveness, preventing delays and interruptions.


### Edge Detection

- Edge detection plays a vital role in computer vision applications, as it helps in identifying and locating objects within images by detecting abrupt changes in intensity or color. This feature enables users to highlight edges, contours, and boundaries, making it easier to analyze and interpret visual data.

- Edge detection algorithms, such as the Sobel operator, Canny edge detector, and Roberts cross operator, are commonly used to detect edges in images. These algorithms analyze the gradient of pixel intensities to identify regions with significant changes, indicating the presence of edges.

- By integrating edge detection capabilities into the Fourier Transform Mixer, users can perform more advanced image analysis tasks, such as object recognition, image enhancement, and image segmentation. This enhances the versatility and utility of the application, making it a valuable tool for researchers, engineers, and image processing enthusiasts.
![image](https://github.com/AliBadran716/Fourier-Transform-Mixer/assets/102072821/6107764b-6ae0-4085-8f63-7abb0ca71d71)




## Code Practices

- **Object-Oriented Approach**: The program follows an object-oriented approach to code organization and encapsulation. By encapsulating functionality within classes, the codebase remains modular and maintainable.
- **Logging**: Python's logging library is utilized for tracking user interactions and debugging. Detailed logs help developers identify and resolve issues more efficiently, improving overall code quality and reliability.

## Tools Used

- **Python**: Core programming language used for development.
- **PyQt5**: GUI library used for creating the desktop application's interface.
- **OpenCV**: Image processing library used for image manipulation tasks.
- **NumPy**: Numerical computing library used for array operations and mathematical calculations.
- **PyQtGraph**: Graphics library used for displaying and interacting with images and their components.


## Getting Started

### Clone Repository:

```bash
git clone https://github.com/Muhannad159/Fourier-Transform-Mixer
```

### Install Dependencies:

```bash
pip install -r requirements.txt
```

### Run the Application:

```bash
python main.py
```

## Contributors <a name = "Contributors"></a>

<table>
  <tr>
    <td align="center">
    <a href="https://github.com/Muhannad159" target="_black">
    <img src="https://avatars.githubusercontent.com/u/104541242?v=4" width="150px;" alt="Muhannad Abdallah"/>
    <br />
    <sub><b>Muhannad Abdallah</b></sub></a>
    </td>
  <td align="center">
    <a href="https://github.com/AliBadran716" target="_black">
    <img src="https://avatars.githubusercontent.com/u/102072821?v=4" width="150px;" alt="Ali Badran"/>
    <br />
    <sub><b>Ali Badran</b></sub></a>
    </td>
     <td align="center">
    <a href="https://github.com/ahmedalii3" target="_black">
    <img src="https://avatars.githubusercontent.com/u/110257687?v=4" width="150px;" alt="Ahmed Ali"/>
    <br />
    <sub><b>Ahmed Ali</b></sub></a>
    </td>
<td align="center">
    <a href="https://github.com/hassanowis" target="_black">
    <img src="https://avatars.githubusercontent.com/u/102428122?v=4" width="150px;" alt="Hassan Hussein"/>
    <br />
    <sub><b>Hassan Hussein</b></sub></a>
    </td>
      </tr>
 </table>
