# MEP file contents

- [Image J Approaches](#image-j-approaches) 
    - [Candidate_Segmentation_Measure.ijm](#candidate_segmentation_measureijm)
    - [ROI_filtering.py](#roi_filteringpy)


# Image J Approaches

## [Candidate_Segmentation_Measure.ijm](Candidate_Segmentation_Measure.ijm)

Takes the images obtained and performs a watershed segmentation on them ###SAY FROM WHERE.

Then, if "ignore edges" is true, it will remove the selected ROIs that are in contact with the edge, as well as remove the ROIs of small dots from everywhere in the image.

Finally, the macro saves all the ROIs into the folder chosen at first, measures the remaining 
ROIs and extracts the measured values as a .csv into the same folder.

## [ROI_filtering.py](ROI_filtering.py)

WIP

It imports the exported csv and filters based on the threshold values set.

It then separates the selected ROIs into a new folder and zips it up into `FilteredRois.zip`

It finishes off by deleting the unzipped ROIs folder to save space and allow for the next code to be ran without needing to manually delete it.