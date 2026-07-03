# aMiCo: Automated Microscope Control repository contents
- [Overview](#overview)
- [Mitosis Detection](#mitosis-detection) 
    - [CellProfiler (CP)](#cell-profiler-approaches)
        - [Speckles](#speckles)
    - [ImageJ (IJ)](#image-j-approaches)
- [Microscope Implementation](#microscope-implementation)
    - [Zen-API](#zenapi-scripts)
- [Links and References](#links-and-references)

# Overview
This project aims to develop a method to detect cells that are about to mitose and change imaging parameters in order to take higher resolution images of 
those cells exclusively. In order to do this we are researching different ways to obtain a robust [Mitosis Detection Algorithm](#mitosis-detection) using 
different softwares, namely [Cell Profiler](#cell-profiler-approaches), and [ImageJ/Fiji](#image-j-approaches).  Along with developing a way to 
[communicate with the microscope](#microscope-implementation) to have the computer autonomously control the imaging parameters in real-time, for this we 
are working with a Zeiss Axio Imager.Z2 microscope and controlling it using the Zen-API control sotware.

# Mitosis Detection

The mitosis-detection approach plans to make use of the condensing DNA signal showcased during prophase to identify nuclei belonging to cells entering mitosis that are about to divide. To do this, strategies using both [Cell Profiler](#cell-profiler-approaches) and [ImageJ/FIJI](#image-j-approaches) were developed. 

## Cell Profiler Approaches

### Speckles

Using the [Extract_Speckles.cppipe](./Mitosis%20Detection/Cell%20Profiler/Speckles/Extract_Speckles.cpproj) pipeline created we identify speckles smaller than 10 units and get their frame and which parent cell they belong to into a .csv file.

Then, using the [Speckle_filtering.py](./Mitosis%20Detection/Cell%20Profiler/Speckles/Speckle_filtering.py) script we count the speckles per cell per timeframe and separate into a new folder the images of the cells that surpass the set threshold number of speckles.

Curently, these images then get manually checked by comparing it to the timeframe and separated once more into "correctly identified"and "incorrectly identified" cells.

Initial tests using this pipeline have shown successful identification of prophase cells with more defined DNA speckles, however persistent false-positive detection of the same interphase cells across timeframes occured even when using different speckle sizes and thresholds. This likely indicates that the biological variability in ``homogeneous" interphase DNA might interphere with speckle counting as a method for prophase detection. --Further validation in extended image-sets to be done.


## Image J Approaches

Commented macro files developed for mitosis detection can be found in the [ImageJ](./Mitosis%20Detection/ImageJ/) directory.


# Microscope Implementation

In order to interact with the Zen microscope we have used the ZenAPI functionalities along with the pyimagej python package in order to communicate with FIJI and allow 
us to inmediately analyse the obtained images as soon as they are taken. 

## Setup

In order to have the smartmicroscopy setup work at the same time as the pyimagej python package we have adjusted the original environment Zeiss OAD has, this new environment is in the [env_imagej_smartmic.yml](./Microscope%20Implementation/Setup/env_imagej_smartmic.yml) file. The requirements for the method to work are contianed in the [needed_installs.txt](./Microscope%20Implementation/Setup/needed_installs.txt) file, along with the instructions ([Installation_instructions.txt](./Microscope%20Implementation/Setup/Installation_instructions.txt)) to get the system working.

## ZenAPI Scripts

The main code to control the smart microscopy setup is the [zstack-timelapse_positions](./Microscope%20Implementation/ZenAPI/zstack-timelapse_positions.py), this code calls onto the microscope interaction functions contained in the [functions_mic_control.py](./Microscope%20Implementation/ZenAPI/functions_mic_control.py) to move the hardware and begin experiments, and uses the functions within [functions_imageJ_interact.py](./Microscope%20Implementation/ZenAPI/functions_imageJ_interact.py) to communicate with fiji and analyse the results produced by the macros analysing the images, the macros are read from the [ij_macros.py](./Microscope%20Implementation/ZenAPI/ij_macros.py) file that contain the version of the [image J macros](./Mitosis%20Detection/ImageJ/) needed for pyimagej to function.

[zstack-timelapse_positions](./Microscope%20Implementation/ZenAPI/zstack-timelapse_positions.py) begins different experiments at the overview level, than the one begun when it is zoomed in, these experiments must be setup using the Zen Blue software and saved, their names must then be writen as variables in the [zstack-timelapse_positions](./Microscope%20Implementation/ZenAPI/zstack-timelapse_positions.py) code for the API to begin the determined experiments at different times. For the initial tests, the saved experiments can be found in the [Experiments](./Microscope%20Implementation/ZenAPI/Experiments/) folder.

A test to evaluate the performance of the microscope control has been carried out ([Test_Data](./Microscope%20Implementation/Test_Data/)), where the resulting images along with timestamps can be found.
