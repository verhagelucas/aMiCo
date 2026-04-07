
# #################################
#
# Inputs: * CellProfiler .csv with speckle information (Output of Speckle_Detector.cppipe)
#         * Images of cells with the speckles grouped in folders per time frame
#
# Output: * New folders containing all the cell images that have a speckle count 
#         above the specified thresholds
#
# #################################

import pandas as pd
import numpy as np
from tkinter import filedialog
import os
import shutil, glob

speckle_thresholds = [100, 150, 200, 210, 220, 230, 240, 250, 300, 450]


### define the common files (csv & images)
file_path = filedialog.askopenfilename( #select excel file to be analysed
    title="Select a csv file to analyse",
    filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
)
directory = os.path.dirname(file_path)  #extract directory path

img_src_dir = filedialog.askdirectory(  # select folder from which the images will be copied from
    title="Select the folder containing the images"
)  

data = pd.read_csv(file_path)
#extract general info from data
n_images = data.iloc[-1, 0]                             # total n of images = last image number
parent_nuclei = np.sort(data["Parent_Nuclei"].unique()) # get list of all the nuclei that had specks in them
n_specks = np.copy(parent_nuclei)                       # create temp array to keep track of specks belonging to each nucleus


for speckle_threshold in speckle_thresholds:

    #create new folder with threshold to store the detected cells in
    dir_detected_cells = f"{directory}/detected_cells_{speckle_threshold}"  
    os.mkdir(dir_detected_cells) 


    #region data filtering
    n_specks_all_img = np.zeros((n_images, n_specks.size))  # create 2D array to keep track of n of specks per image frame: row = image frame, column = nucleus number

    # count n of specks belonging to each parent nuclei per image frame
    for i in range(n_images):     
        im_i = data[data["ImageNumber"] ==  i+1]    # extract the rows belonging to that image frame

        for ind,j in enumerate(parent_nuclei):
            n_specks[ind] = len(im_i[im_i["Parent_Nuclei"]==j]) # store the amount of specks that belong to each nuclei

        n_specks_all_img[i,:] = n_specks    # store in permanent array

    speck_count = pd.DataFrame(n_specks_all_img, columns=parent_nuclei) #make df of the counts array

    count_dict = dict(list(speck_count.groupby(speck_count.index))) # group our df by index and create a dict with lists of df's as values

    #endregion

    #region separate identified cells

    for t_frame, counts in count_dict.items():       # t_frame= row index, counts = df row w t_frame's counts       
        check = counts.columns[(counts > speckle_threshold).any()]  #see which counts are above the established threshold
        if len(check) > 0: 
            for cell_num in check.tolist():     # go over each identified cell (check) & transfer from old location to newly made directory
                for image in glob.glob(f"{img_src_dir}/*{t_frame+1}/*_{cell_num}.*"):   # t_fram+1 bcs CP starts counting at 1, not 0
                    shutil.copy(image,dir_detected_cells)
    #endregion

    print("Done!")