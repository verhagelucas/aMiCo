import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# haralick_directory = r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\20251211"
# target_label = "0020_0003"  # label of the ROI with the condensed DNA
# output_directory = r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\20251211"
haralick_directory = r"c:\Users\Student\OneDrive-Maz\OneDrive - Erasmus University Rotterdam\MEP\Maria\Haralick_plots\FollowROIs\20251128\Pos1\Cell1\normal_images"
output_directory = r"c:\Users\Student\OneDrive-Maz\OneDrive - Erasmus University Rotterdam\MEP\Maria\Haralick_plots\FollowROIs\20251128\Pos1\Cell1\normal_images"
target_label = "0030_0007"

features = ["H1","H2", "H3", "H4","H5","H6","H7","H8","H9","H10","H11"]

haralick_df = pd.read_csv(haralick_directory+r"\Results_Haralick_d_1.csv", 
                          usecols=features)
files_df = pd.read_csv(haralick_directory+r"\Files_list.csv",
                       header=0,names=["ROI_label"])

whole_df = pd.concat([haralick_df,files_df], axis=1)

# Find index of the target label

try:
    target_idx = whole_df.index[whole_df["ROI_label"] == target_label][0]
except IndexError:
    raise ValueError(f"Label {target_label} not found in ROI_label column")

def plot_haralick(df, title, save_path):
    # Create 3x4 grid of subplots
    fig, axes = plt.subplots(3, 4, figsize=(16, 10), sharex=True)
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

    fig.suptitle(title, fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # leave space for suptitle

    plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.show()


#normalise between 0&1
norm_df = whole_df.copy()
scaler = MinMaxScaler()
norm_df[features] = scaler.fit_transform(norm_df[features])


# Correct for haralick using average haralick at frame
allcells_directory = r"c:\Users\Student\OneDrive-Maz\OneDrive - Erasmus University Rotterdam\MEP\Maria\Haralick_plots\FollowROIs\20251128\Pos1\AllCells"
full_haralick_df = pd.read_csv(allcells_directory+r"\Full_Results_Haralick_d_1.csv", 
                               usecols=features)
full_files_df = pd.read_csv(allcells_directory+r"\Full_Files_list.csv",
                            header=0,names=["ROI_label"])

full_whole_df = pd.concat([full_haralick_df,full_files_df], axis=1)

#look at difference between value and mean
last_slice = whole_df["ROI_label"].index[-1]    # get the last frame we are interested in (avoid unnecessary calculations)

# Calculate avg for each frame
adjusted_dfs = []  # List to collect adjusted values

for slice in range(1, last_slice+1):
    prefix = f"{slice:04d}"
    
    # Get the means of all the haralicks in that slice
    slice_haralicks = full_whole_df[full_whole_df["ROI_label"].str.startswith(prefix, na=False)][features]
    means = slice_haralicks.mean().values 
    
    # GEt the haralicks of the ROIs we are interested in
    relevant_ROIs = whole_df[whole_df["ROI_label"].str.startswith(prefix, na=False)][features]
    
    # Look at how far the individual interest haralick is from the mean
    adjusted_slice = relevant_ROIs - means
    
    adjusted_dfs.append(adjusted_slice)

adjusted_df = pd.concat(adjusted_dfs)   # make into df
adjusted_df = pd.concat([adjusted_df,files_df], axis=1)

# plot_haralick(df= [whole_df], title= "Haralick Features Over Time\nd_1", save_path=output_directory+r"\Haralick_Features_Over_Time_d_1.png")
# plot_haralick(df= [norm_df], title= "Normalised Haralick Features Over Time\nd_1", save_path=output_directory+r"\Normalised_Haralick_Features_Over_Time_d_1.png")
# plot_haralick(df= [adjusted_df], title= "Adjusted Haralick Features Over Time\nd_1", save_path=output_directory+r"\Adjusted_Haralick_Features_Over_Time_d_1.png")