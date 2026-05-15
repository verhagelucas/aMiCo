import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from target_dict import targets_20251128_Pos1, targets_20260416_Pos7

haralick_directory = "c:\\Users\\Student\\OneDrive-Maz\\OneDrive - Erasmus University Rotterdam\\MEP\\Maria\\Haralick_plots\\FollowROIs\\20251128\\Pos1\\Cell5\\gaussian-blur"
output_directory = "c:\\Users\\Student\\OneDrive-Maz\\OneDrive - Erasmus University Rotterdam\\MEP\\Maria\\Haralick_plots\\FollowROIs\\20251128\\Pos1\\Cell5\\gaussian-blur"
allcells_directory = "c:\\Users\\Student\\OneDrive-Maz\\OneDrive - Erasmus University Rotterdam\\MEP\\Maria\\Haralick_plots\\FollowROIs\\20251128\\Pos1\\AllCells\\gaussian-blur"

targets_dict = targets_20251128_Pos1

features = ["H1","H2", "H3", "H4","H5","H6","H7","H8","H9","H10","H11"]
offsets = [1, 2, 3, 4, 5]

parts = haralick_directory.rsplit("\\", 2)
target_label = targets_dict[parts[-2]]

def plot_multiple_haralicks(dfs, title, save_path, show = True, save = True):
    # Create 3x4 grid of subplots

    for df in dfs:
        plt.plot(df.index, df[features], label= features)
    axes = axes.flatten()  # make it 1D for easy indexing

    for i, h in enumerate(features):
        ax = axes[i]
        for id, d in enumerate(df):
            ax.plot(d.index, d[h], marker='o', markersize = 5, label=f"cell {id}")
        ax.set_title(h)
        ax.set_ylabel(f"{h} value")

        # Only one tick at target position
        ax.set_xticks([target_idx])
        ax.set_xticklabels([f"DNA condensed\n{target_label}"], rotation=25, ha='right')

        # Vertical line at that timepoint
        ax.axvline(x=target_idx, color='red', linestyle='--', alpha=0.8)

    # Hide the unused last subplot (since 3*4=12 and we have 11 features)
    axes[-1].set_visible(False)

    plt.title(title, fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # leave space for suptitle

    if save: plt.savefig(save_path, dpi=300, bbox_inches='tight')

    if show: plt.show()

    plt.close()


print(f"Looking at {parts[-2]}, with preprocessing: {parts[-1]}")

for offset in offsets:

    haralick_df = pd.read_csv(haralick_directory+r"\Results_Haralick_d_"+str(offset)+".csv", 
                            usecols=features)
    files_df = pd.read_csv(haralick_directory+r"\Files_list.csv",
                        header=0,names=["ROI_label"])

    whole_df = pd.concat([haralick_df,files_df], axis=1)    # df containing the measurements of the cell of interest

    # Find index of the target label

    try:
        target_idx = whole_df.index[whole_df["ROI_label"] == target_label][0]
    except IndexError:
        raise ValueError(f"Label {target_label} not found in ROI_label column")


    #normalise between 0&1
    norm_df = whole_df.copy()
    scaler = MinMaxScaler()
    norm_df[features] = scaler.fit_transform(norm_df[features])


    # Correct for haralick using average haralick at frame
    full_haralick_df = pd.read_csv(allcells_directory+r"\Full_Results_Haralick_d_"+str(offset)+".csv", 
                                usecols=features)
    full_files_df = pd.read_csv(allcells_directory+r"\Full_Files_list.csv",
                                header=0,names=["ROI_label"])

    full_whole_df = pd.concat([full_haralick_df,full_files_df], axis=1)

    #look at difference between value and mean
    last_slice = whole_df["ROI_label"].index[-1]    # get the last frame we are interested in (avoid unnecessary calculations)

    # Calculate avg for each frame
    adjusted_dfs = []  # List to collect adjusted values
    running_dfs = []  # create a storage array that keeps track of the current haralick average

    running_mean_den = np.zeros(len(features))  # create a storage array that keeps track of the current haralick average denominator
    running_mean_num = 0  # create a storage array that keeps track of the current haralick average numerator
    

    for slice in whole_df["ROI_label"]:
        prefix = slice[:4]  #extract slice label
        
        # Get the means of all the haralicks in that slice
        slice_haralicks = full_whole_df[full_whole_df["ROI_label"].str.startswith(prefix, na=False)][features]

        # update running average values
        running_mean_den += slice_haralicks.sum().values
        running_mean_num += slice_haralicks.index[-1]

        running_mean = running_mean_den / running_mean_num

        means = slice_haralicks.mean().values # mean of the current frame
        
        # GEt the haralicks of the ROIs we are interested in
        relevant_ROIs = whole_df[whole_df["ROI_label"].str.startswith(prefix, na=False)][features]
        
        # Look at how far the individual interest haralick is from the mean
        adjusted_slice = relevant_ROIs - means
        running_slice = relevant_ROIs - running_mean
        
        adjusted_dfs.append(adjusted_slice)
        running_dfs.append(running_slice)

    adjusted_df, running_df = pd.concat(adjusted_dfs), pd.concat(running_dfs)   # make into df
    adjusted_df, running_df = pd.concat([adjusted_df,files_df], axis=1), pd.concat([running_df,files_df], axis=1)   # add ROI_labels column




    # Plot the features
    plot_haralick(df= [whole_df], title="Raw\nHaralick Features Over Time\nd_"+str(offset)+"", save_path=output_directory+r"\Haralick_Features_Over_Time_d_"+str(offset)+".png", show=False)
    plot_haralick(df= [norm_df], title="Normalised\nHaralick Features Over Time\nd_"+str(offset)+"", save_path=output_directory+r"\Normalised_Haralick_Features_Over_Time_d_"+str(offset)+".png", show=False)
    plot_haralick(df= [adjusted_df], title="Adjusted\nHaralick Features Over Time\nd_"+str(offset)+"", save_path=output_directory+r"\Adjusted_Haralick_Features_Over_Time_d_"+str(offset)+".png", show=False)
    plot_haralick(df= [running_df], title="Adjusted Running Avg\nHaralick Features Over Time\nd_"+str(offset)+"", save_path=output_directory+r"\Running-mean_Haralick_Features_Over_Time_d_"+str(offset)+".png", show=False)

print("Done!")