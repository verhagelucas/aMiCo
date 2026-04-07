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

1) If setup is needed follow the instructions found in the [Setup](../Setup/) folder

2) Open VS code by right clicking on the Visual Studio Code application and selecting "Run as administrator"

3) Open the `[zstack-timelapse_positions.py](./zstack-timelapse_positions.py)` file, and change the variables: `exp_choice`, and `zoomed_exp_choice` to the names of the experiments you want to run during the overview image acquisition phase, and the zoomed image acquisition phase respectively.

4) Explian here how to extract the positions and store in a folder dedicated to those positions, which for now we will call `positions folder`

4) When you run the code it will prompt you for a series of things:
    1) `selected_folder`: a pop up file explorer dialogue will ask for the folder in which the experiments files will be stored in, this folder must also contain the positions csv file, and as such must be the same as the `positions folder` mentioned in step 3.
    2) `experiment_name`: the terminal will prompt for a name it will give the experiment's folder, this name will be used to create a new directory within the `selected_folder` location where all the images acquired will be stored in
    3) `timepoints`: a second terminal prompt will ask how many timepoints you want to take. This must be a n integer number and will be used in the latter timepoint while loop.

After this the code will run and perform the experiments, this will look as follows:

1) For each timepoint t a new folder named `timepoint_<t>` will be created within the `selected_folder/experiment_name/` folder.
2) Within that timepoint folder each overview position `<i>` taken by `<overview_obj>` will be stored as `Pos<i>_Z-Exp.czi`.
3) The intermediate files `process.tif`, `Results.csv` and `RoiSet.zip` produced by the fiji analysis of the overview positions will also be stored in the same `selected_folder/experiment_name/timepoint_<t>/` folder as the images. However, for each overview position these files will be overwriten in order to help reduce data content.
4) Once it has been determined whether an object of interest is present the stage will move to the defined `new_posx` and `new_posy` at the centre of said object and the objective will change to the defined `zoomed_obj`. Each of the zoomed in acquisitions will be saved in the same timepoint `selected_folder/experiment_name/timepoint_<t>/` folder as `Pos<i>_Zoomed_TL-Exp.czi`. 
5) Once the whole code experiment is done the csv file containing the timed benchmarks is saved in the `selected_folder/experiment_name/` folder as `timing_data.csv`

The final file tree will look as follows:

    . Positions/ => Manually created folder == <selected_folder>
    ├── positions.csv => Manually exported positions file
    └── <experiment_name>/ => Automatically created folder with specified <experiment_name>
        ├── "timepoint_<t>"/ => Automatically created folder
        │   ├── Pos<i>_Z-Exp.czi => z-stack experiment file of position i
        │   ├── Pos<i>_Zoomed_TL-Exp.czi => timelapse experiment file of zoomed position i
        │   └── ...(Done for all positions <i> in `positions.csv` file)
        ├── ...(Done for <t> in specified <timepoints>)
        └── timing_data.csv => Automatically created file with experiment timing information

