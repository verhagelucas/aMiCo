import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from target_dict import targets_20251128_Pos1, targets_20260416_Pos7

haralick_directory = "C:\\Users\\elsam\\Documents\\MEP\\Data\\Haralick_Plots\\4bit\\20260416_Pos7\\"
output_directory = "C:\\Users\\elsam\\Documents\\MEP\\Data\\Haralick_Plots\\4bit\\20260416_Pos7\\Results"
#allcells_directory = "c:\\Users\\Student\\OneDrive-Maz\\OneDrive - Erasmus University Rotterdam\\MEP\\Maria\\Haralick_plots\\FollowROIs\\20251128\\Pos1\\AllCells\\gaussian-blur"

targets_dict = targets_20260416_Pos7

features = ["H1","H2", "H3", "H4","H5","H6","H7","H8","H9","H10","H11"]
offsets = [1, 2, 3, 4, 5]
# cells = ["Cell1", "Cell2", "Cell3", "Cell4", "Cell5", "Cell6", "Cell7"]
cells = ["Cell7"]

output_directory = "C:\\Users\\elsam\\Documents\\MEP\\Data\\Haralick_Plots\\4bit\\20260416_Pos7\\"+cells[0]+"\\Results"

parts = haralick_directory.rsplit("\\", 3)


def plot_haralick(df, title, save_path, show = True, save = True):
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

    if save: plt.savefig(save_path, dpi=300, bbox_inches='tight')

    if show: plt.show()

    plt.close()


print(f"Looking at {cells}, with preprocessing: {parts[-3]}")


whole_dfs = []

for offset in offsets:

    for cellnumber in cells:
        target_label = targets_dict[cellnumber]
        cell_directory = haralick_directory+cellnumber
        haralick_df = pd.read_csv(cell_directory+r"\Results_Haralick_d_"+str(offset)+"_4bit.csv", 
                                usecols=features)
        files_df = pd.read_csv(cell_directory+r"\Files_list.csv",
                        header=0,names=["ROI_label"])
        
        whole_df = pd.concat([haralick_df,files_df], axis=1)    # df containing the measurements of the cell of interest

        whole_dfs.append(whole_df)
        # Find index of the target label

        try:
            target_idx = whole_df.index[whole_df["ROI_label"] == target_label][0]
        except IndexError:
            raise ValueError(f"Label {target_label} not found in ROI_label column")

    # Plot the features
    plot_haralick(df= whole_dfs, title="Normalised 4-bit Transform\nHaralick Features Over Time\nd_"+str(offset)+"", save_path=output_directory+r"\Haralick_Features_Over_Time_d_"+str(offset)+".png", show=True, save=False)

print("Done!")