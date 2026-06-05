import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

##IJ actions 

#1) perform candidate segmentation

# for each cell:
    #2) extract cell rois & clear outside

    #3) transform to 4bit image

    #4) calculate haralick feature

# 5) Store the results into csv 
# 6) Also store the measurement results into csv to get the coordinates where we move
# 6) OPTION2: Make imagej macro that giving it the name of the roi = ouutputs coordinates (cant do that nvm ijm outputs dont work in the version we have)

allcells_directory = "c:\\Users\\Student\\OneDrive-Maz\\OneDrive - Erasmus University Rotterdam\\MEP\\Maria\\Haralick_plots\\FollowROIs\\20251128\\Pos1\\AllCells\\4-bit"

features = ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "H11"]   # features we care about
offset = 5

haralick_df = pd.read_csv(allcells_directory+r"\Full_Results_Haralick_d_"+str(offset)+".csv", 
                            usecols=features)
files_df = pd.read_csv(allcells_directory+r"\Full_Files_list.csv",
                        header=0,names=["ROI_label"])

whole_df = pd.concat([haralick_df,files_df], axis=1)    # df containing the measurements of the cell of interest

last_frame = whole_df.iloc[-1, -1][:4]    # get the last frame 
accepted_ROIs = pd.DataFrame(columns=features+['ROI_label'])


for frame in range(int(last_frame)):
    prefix = f"{frame+1:04d}"   # extract slice label
        
    # Get the means of all the haralicks in that slice
    frame_haralicks = whole_df[whole_df["ROI_label"].str.startswith(prefix, na=False)][features +["ROI_label"]]


    mean = frame_haralicks[features].mean() # mean of the current frame

    frame_haralicks[features] = frame_haralicks[features] - mean

    accepted_mask = frame_haralicks[(frame_haralicks["H1"]>=-1) & (frame_haralicks["H1"]<= 1) &
                                    (frame_haralicks["H2"]>=0) &
                                    (frame_haralicks["H3"]>=-1) & (frame_haralicks["H3"]<= 1) &
                                    (frame_haralicks["H5"]<=-0.1) & 
                                    (frame_haralicks["H8"]>=0) & 
                                    (frame_haralicks["H9"]>=-1.5) & (frame_haralicks["H9"]<= 1.5) &
                                     (frame_haralicks["H11"]>=0) ]
    accepted_ROIs = pd.concat([accepted_ROIs, accepted_mask])

accepted_ROIs.to_csv('c:\\Users\\Student\\Desktop\\temp\\accepted_ROIs.csv', index=False)
# for i in range(len(accepted_ROIs)):
#     if len(accepted_ROIs[i]):
#         print(f"\nframe {i+1}")
#         print(accepted_ROIs[i])