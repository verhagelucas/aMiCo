# MEP file contents

- [Image J Approaches](#image-j-approaches) 
    - [Haralick_Analysis](#haralick-analysis)
        - [Test_Data](#test_data)
        - [Process_HaralickROIs.ijm](#process_haralick_roisijm)
        - [Haralick_plots.py](#haralick_plotspy)
    - [Process_Image.ijm](#process_imageijm)
    - [Candidate_Segmentation_Measure.ijm](#candidate_segmentation_measureijm)
    - [ROI_filtering.py](#roi_filteringpy)


# Image J Approaches

## Haralick Analysis
File contents: Haralick analysis of cell ROIs

### [Test_Data](./Haralick_Analysis/Test_Data/)

folder containing the Test Data obtained frmo performing haralick analysis on different experiments

### [Process_Haralick_ROIs.ijm](./Haralick_Analysis/Process_HaralickROIs.ijm)

### [Haralick_plots.py](./Haralick_Analysis/Haralick_plots.py)


## [Process_Image.ijm](Process_Image.ijm)

Meant to be used to pre-process the z-stack experiments obtained in the overview images to ensure correct functioning of the [Candidate_Segmentation_Measure.ijm](Candidate_Segmentation_Measure.ijm) macro.

Takes the images obtained by the microscope, checks how many channels there are and keeps only the first channel if there is more than one. It then performs a maximum Z projection based on max intensity to generate a single image.

## [Candidate_Segmentation_Measure.ijm](Candidate_Segmentation_Measure.ijm)

Takes the images obtained and performs a watershed segmentation on them ###SAY FROM WHERE.

Then, if "ignore edges" is true, it will remove the selected ROIs that are in contact with the edge, as well as remove the ROIs of small dots from everywhere in the image.

Finally, the macro saves all the ROIs into the folder chosen at first, measures the remaining 
ROIs and extracts the measured values as a .csv into the same folder.

## [Reset_IJ.ijm](Reset_IJ.ijm)

Meant to clear out the fiji application and empty out the ROI manager selections to allow the analysis to be repeated on the next image taken.

It first closes all open image windows, then deletes all ROIs from the ROI manager, and finally it closes the windows displaying the results of the measurements taken.

## [ROI_filtering.py](ROI_filtering.py)

WIP

It imports the exported csv and filters based on the threshold values set.

It then separates the selected ROIs into a new folder and zips it up into `FilteredRois.zip`

It finishes off by deleting the unzipped ROIs folder to save space and allow for the next code to be ran without needing to manually delete it.