# MEP file contents

- [Speckles(CP)](#speckles-cp) 
    - [Extract_Speckles.cpproj](#extract_specklescpproj)
    - [Speckle_filtering.py](#speckle_filteringpy)


# Speckles (CP)


## [Extract_Speckles.cpproj](Speckles/Extract_Speckles.cpproj)

Identifies speckles smaller than 10 units and get their frame and which parent cell they belong to into a .csv file.

It outputs a .csv file containing the information of each speckle found, and a folder containing the cropped cells for each timeframe.

## [Speckle_filtering.py](Speckles/Speckle_filtering.py)

Takes the path to the .csv file containing information of each speckle found, "SpeckleTest_X_wImageExtraction_CondensedDNA.csv".
Takes the path to the folder containing the cropped cell images "SaveIm_X".
`speckle_thresholds` should be a list of integers containing the thresholds on which the speckle count will be filtered with.

It takes "File frame" and "Parent Cell" from the csv file. Using these two values it computes the speckles per cell for each timeframe and checks which cells in which timeframe surpass the set threshold number of speckles in the cell.

It then separate into a new folder the images of the cells that surpass the set threshold number of speckles.

It then copies the images belonging to the identified cells into a new folder containing all the identified cells with that threshold.

Curently, these images then get manually checked by comparing it to the timeframe and separated once more into "correctly identified"and ïncorrectly identified" cells.