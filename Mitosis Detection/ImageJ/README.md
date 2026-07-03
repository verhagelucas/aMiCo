# MEP file contents

- [Image J Approaches](#image-j-approaches) 
    - [Image_Preprocessing.ijm](#process_imageijm)
    - [Candidate_Segmentation.ijm](#candidate_segmentation_measureijm)
    - [Normalised_8_to_4-bit_Transform.ijm](#normalised_8to4bit_transformijm)
    - [Extract_Measurements.ijm](#extract_measurementsijm)
    - [Extact_Haralick_Measurements.ijm](#extract_haralick_measurementsijm)
    - [Reset_IJ.ijm](#reset_ijijm)


# Image J Approaches

## [Image_Preprocessing.ijm](Image_Prepocessing.ijm)

Meant to be used to pre-process the z-stack experiments obtained by extracting a single channel of the overview images to ensure correct functioning of the [Candidate_Segmentation.ijm](Candidate_Segmentation.ijm) macro.

Takes the images obtained by the microscope, checks how many channels there are and keeps only the specified channel if there is more than one. It then performs a maximum Z projection based on max intensity to generate a single image.

## [Candidate_Segmentation.ijm](Candidate_Segmentation.ijm)

Takes the images obtained and segments them using the MorphoLibJ distance transform watershed with the borgefors method. Labelled composite ROIs are extracted through PTBIOP's plugin into a whole list of ROIs.

Then, if ``ignore edges`` is true, it will remove the selected ROIs that are in contact with the edge, as well as remove the ROIs smaller than the set ``min_sel`` pixels from everywhere in the image.

Finally, the macro saves all the ROIs into the folder chosen.

## [Normalised_8to4bit_Transform.ijm](Normalised_8to4bit_Transform.ijm)
Takes an image and converts it to an 8-bit image. The maximum intensity value is then extracted and used to calculate a scaled and binned 4-bit transform for each image pixel using the following equation:

$$
\text{px intensity}_{\text{4-bit}}^{\text{final}} = \lceil \frac{\text{px intensity}_{\text{8-bit}}^{\text{original}} \cdot 15}{\text{max intensity}_{\text{8-bit}}^{\text{original}} } \rceil\
$$

## [Extract_Measurements.ijm](Extract_Measurements.ijm)
ROI selections are measured on the opened image for the  standard deviation, perimeter, center of mass x and y coordinates, bounding box x and y coordinates, perimeter, selection width and height, and kurtosis. These values are then extracted into a ``Results.csv`` file. 

## [Extract_Haralick_Measurements.ijm](Extract_Haralick_Measurements.ijm)

Duplicates each ROI, clears the outside of the selection, and pre-processes the resulting image acording to the selected method (gaussian, normalised 4-bit, or none). Then the first 11 0&deg; GLCM Haralick values are calculated using two distinct offsets for each extracted ROI image, where each of the offsets is extracted as a ``Results_Haralick_d_offset.ijm``. The ROI label names are stored in a ``Files_list.csv`` with the ``frame_objectID`` format

## [Reset_IJ.ijm](Reset_IJ.ijm)

Meant to clear out the fiji application and empty out the ROI manager selections to allow the analysis to be repeated on the next image taken.

It first closes all open image windows, then deletes all ROIs from the ROI manager, and finally it closes the windows displaying the results of the measurements taken.