# ZenAPI Scripts

- [Introduction](#introduction)
- [Files](#files)
    - [Helper function files](#helper-function-files)
        - [functions_imageJ_interact.py](#functions_imagej_interactpy)
        - [functions_mic_control.py](#functions_mic_controlpy)
        - [ij_macros.py](#ij_macrospy)
        - [zen_api_utils](#zen_api_utils)
        - [Experiments](#experiments)
    - [Main script](#main-script)
        - [zstack-timelapse_positions.py](#zstack-timelapse_positionspy)
- [Instructions](#instructions)

# Introduction

# Files

## Helper function files

### [functions_imageJ_interact.py](./functions_imageJ_interact.py)
File containing the functions to perform analysis of the obtained images, there are 2 types of functions contained within the script:
1) functions that segment and measure the obtained images
    - `fiji_segmentation`
    - `fiji_segmentation_get_outputs`
2) functions that use the measurements obtained to decide the objects that will be looked into
    - `find_largest_centre_com`
    - `find_largest_centre_dims`

### [functions_mic_control.py](./functions_mic_control.py)

### [ij_macros.py](./ij_macros.py)

### [zen_api_utils](./zen_api_utils/)

### [Experiments](./Experiments/)

## Main script

### [zstack-timelapse_positions.py](./zstack-timelapse_positions.py)

# Instructions

