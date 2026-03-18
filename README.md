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
This project aims to develop a method to detect cells that are about to mitose and change imaging parameters in order to take higher resolution images of those cells exclusively. In order to do this we are researching different ways to 
obtain a robust [Mitosis Detection Algorithm](#mitosis-detection) using different softwares, namely [Cell Profiler](3cell-profiler-approaches), and [ImageJ/Fiji](#image-j-approaches).  Along with developing a way to 
[communicate with the microscope](#microscope-implementation) to have the computer autonomously control the imaging parameters in real-time, for this we are working with a Zeiss Axio Imager.Z2 microscope and controlling it using the
Zen-API control sotware.

# Mitosis Detection

Use the condensated to  identify cells about to divide

## Cell Profiler Approaches

### Speckles

Using the [Extract_Speckles.cppipe](./CellProfiler/Speckles/Extract_Speckles.cpproj) pipeline we identify speckles smaller than 10 units and get their frame and which parent cell they belong to into a .csv file.

Then, using the [Speckle_filtering.py](./CellProfiler/Speckles/Speckle_filtering.py) script we count the speckles per cell per timeframe and separate into a new folder the images of the cells that surpass the set threshold number of speckles.

Curently, these images then get manually checked by comparing it to the timeframe and separated once more into "correctly identified"and ïncorrectly identified" cells.

## Image J Approaches

The taken images are segmented using [Candidate_Segmentation_Measure.ijm](./Image%20J/Candidate_Segmentation_Measure.ijm) to identify the cells within it and place them into distinct ROIs. Optionally the identified cells can be filtered out based on whether they are located on the edge of the frame and their size.

### Measurement Filtering

[ROI_filtering.py](./Image%20J/ROI_filtering.py) is a python script that takes a .csv containing the measurements calculated in ImageJ and identifies the ROIs that are within a certain threshold of whatever parameter you chose to look at.

# Microscope Implementation

## ZenAPI Scripts


