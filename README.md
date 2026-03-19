# MEP file contents
- [Overview](#overview)
- [Mitosis Detection](#mitosis-detection) 
    - [CellProfiler (CP)](#cell-profiler-approaches)
        - [Speckles](#speckles)
    - [ImageJ (IJ)](#image-j-approaches)
- [Microscope Implementation](#microscope-implementation)
    - [ZenAPI (ZAPI)](#zenapi-scripts)
- [Links and References](#links-and-references)

# Overview
This project aims to develop a method to detect cells that are about to mitose and change imaging parameters in order to take higher resolution images of 
those cells exclusively. In order to do this we are researching different ways to obtain a robust [Mitosis Detection Algorithm](#mitosis-detection) using 
different softwares, namely [Cell Profiler](#cell-profiler-approaches), and [ImageJ/Fiji](#image-j-approaches).  Along with developing a way to 
[communicate with the microscope](#microscope-implementation) to have the computer autonomously control the imaging parameters in real-time, for this we 
are working with a Zeiss Axio Imager.Z2 microscope and controlling it using the Zen-API control sotware.

# Mitosis Detection

Use the condensated to  identify cells about to divide

## Cell Profiler Approaches

### Speckles

Using the [Extract_Speckles.cppipe](./Mitosis%20Detection/Cell%20Profiler/Extract_Speckles.cpproj) pipeline we identify speckles smaller than 10 units and get their frame and which parent cell they belong to into a .csv file.

Then, using the [Speckle_filtering.py](./Mitosis%20Detection/Cell%20Profiler/Speckle_filtering.py) script we count the speckles per cell per timeframe and separate into a new folder the images of the cells that surpass the set threshold number of speckles.

Curently, these images then get manually checked by comparing it to the timeframe and separated once more into "correctly identified"and ïncorrectly identified" cells.

## Image J Approaches

The taken images are segmented using [Candidate_Segmentation_Measure.ijm](./Mitosis%20Detection/ImageJ/Candidate_Segmentation.ijm) to identify the cells within it and place them into distinct ROIs. Optionally the identified cells can be filtered out based on whether they are located on the edge of the frame and their size.

### Measurement Filtering

[ROI_filtering.py](./Mitosis%20Detection/ImageJ/ROI_filtering.py) is a python script that takes a .csv containing the measurements calculated in ImageJ and identifies the ROIs that are within a certain threshold of whatever parameter you chose to look at.

# Microscope Implementation

In order to interact with the Zen microscope we have used the ZenAPI functionalities along with the pyimagej python package in order to communicate with fiji and allow 
us to inmediately analyse the obtained images as soon as they are taken. 

## Setup

In order to have the smartmicroscopy setup work at the same time as the pyimagej python package we have adjusted the original environment Zeiss OAD has, this new environment is in the [env_imagej_smartmic.yml](./Microscope%20Implementation/Setup/env_imagej_smartmic.yml) file. The requirements for the method to work are contianed in the [needed_installs.txt](./Microscope%20Implementation/Setup/needed_installs.txt) file, along with the instructions ([Installation_instructions.txt](./Microscope%20Implementation/Setup/Installation_instructions.txt)) to get the system working.

## ZenAPI Scripts

The main code to control the smart microscopy setup is the [zstack-timelapse_positions](./Microscope%20Implementation/ZenAPI/zstack-timelapse_positions.py), this code calls onto the microscope interaction functions contained in the [functions_mic_control.py](./Microscope%20Implementation/ZenAPI/functions_mic_control.py) to move the hardware and begin experiments, and uses the functions within [functions_imageJ_interact.py](./Microscope%20Implementation/ZenAPI/functions_imageJ_interact.py) to communicate with fiji and analyse the results produced by the macros analysing the images, the macros are read from the [ij_macros.py](./Microscope%20Implementation/ZenAPI/ij_macros.py) file that contain the version of the [image J macros](./Mitosis%20Detection/ImageJ/) needed for pyimagej to function.

[zstack-timelapse_positions](./Microscope%20Implementation/ZenAPI/zstack-timelapse_positions.py) begins different experiments at the overview level, than the one begun when it is zoomed in, these experiments must be setup using the Zen Blue software and saved, their names must then be writen as variables in the [zstack-timelapse_positions](./Microscope%20Implementation/ZenAPI/zstack-timelapse_positions.py) code for the API to begin the determined experiments at different times. For the initial tests, the saved experiments can be found in the [Experiments](./Microscope%20Implementation/ZenAPI/Experiments/) folder.

A test to evaluate the performance of the microscope control has been carried out ([Test_Data](./Microscope%20Implementation/Test_Data/)), where the resulting images along with timestamps can be found.