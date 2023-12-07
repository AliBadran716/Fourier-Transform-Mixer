
---

# Project Overview

This PyQt5-based desktop program aims to illustrate the importance of magnitude and phase components in a 2D signal, emphasizing different frequency contributions. The software includes various features for image processing, Fourier Transform (FT) components, mixer controls, and real-time mixing.

## User Interface (UI) Design:

### Main Window Layout:

- [ ] Create a main window layout with placeholders for image viewports and output viewports.
- [ ] Include sliders for brightness/contrast adjustments.

### Image Viewports:

- [ ] Implement the ability to open and view four grayscale images.
- [ ] Convert colored images to grayscale if necessary.
- [ ] Ensure all opened images have the same size (resize if needed).
- [ ] Enable double-click functionality for changing images.

### Fourier Transform (FT) Components:

- [ ] Create a combo-box or drop-menu for selecting FT components (Magnitude, Phase, Real, Imaginary).
- [ ] Implement displays for each image's selected FT component.

### Output Viewports:

- [ ] Implement two output viewports similar to image viewports.
- [ ] Allow the user to control where the mixer result will be displayed.

### Brightness/Contrast Controls:

- [ ] Enable mouse dragging for adjusting brightness and contrast in image viewports.
- [ ] Extend this functionality to all four components.

### Components Mixer:

- [ ] Implement sliders for customizing weights of each image's FT.
- [ ] Calculate the weighted average of FT components for the mixer result.

### Regions Mixer:

- [ ] Implement rectangle drawing for selecting regions in each FT component.
- [ ] Include options for selecting inner or outer regions.
- [ ] Allow customization of region size via sliders or resize handles.

### Realtime Mixing:

- [ ] Implement a progress bar to indicate the mixing process.
- [ ] Ensure the mixing process can be canceled if the user initiates a new operation.

## Back-End Logic:

### Image Processing:

- [ ] Implement image loading and conversion to grayscale.
- [ ] Ensure resizing of images to a unified size.

### Fourier Transform:

- [ ] Implement Fourier Transform for each image.
- [ ] Calculate Magnitude, Phase, Real, and Imaginary components.

### Mixer Logic:

- [ ] Implement the mixer logic using weighted averages of FT components.
- [ ] Ensure the customization of weights via sliders.

### Regions Mixer Logic:

- [ ] Implement logic for selecting inner or outer regions in FT components.
- [ ] Allow the user to customize the size of the selected region.

### Realtime Mixing Logic:

- [ ] Implement the mixing process with an ifft operation.
- [ ] Handle the cancellation of ongoing mixing processes.

## Threading:

### Thread Management:

- [ ] Implement threading to handle time-consuming ifft operations.
- [ ] Ensure proper cancellation of previous operations when new requests are made.

## Testing:

### Unit Testing:

- [ ] Test individual components and functions.
- [ ] Ensure UI elements and backend logic work as expected.

### Integration Testing:

- [ ] Test the integration of UI and backend components.
- [ ] Check for responsiveness and real-time updates.

## Documentation:

### Code Documentation:

- [ ] Add comments and documentation to your code for future reference.

### User Guide:

- [ ] Prepare a user guide explaining how to use each feature.

## Additional Considerations:

### Error Handling:

- [ ] Implement error handling for potential issues during image loading, processing, and mixing.

### UI Enhancements:

- [ ] Consider adding visual indicators for the selected regions in FT components.

### User Feedback:

- [ ] Provide feedback to the user during lengthy operations, such as mixing.

---

This format allows for easy tracking of completed tasks by marking the checkboxes. Update the checkboxes as tasks are completed during the development process.
