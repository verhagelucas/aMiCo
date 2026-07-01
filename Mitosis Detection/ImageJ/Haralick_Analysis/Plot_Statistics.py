import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from target_dict import targets_20251128_Pos1, targets_20260416_Pos7

cells = ["Cell1", "Cell2", "Cell3", "Cell4", "Cell5", "Cell6", "Cell7", "Cell8", "Cell9", "Cell10", "Cell11", "Cell12", "Cell13"]
cells = ["Cell1"]
date = "20251128"
pos = "Pos1"
targets_dict = targets_20251128_Pos1

features = ["StdDev", "Skew", "Kurt"]
ref_x = 0  # all red lines will align here

fig, ax = plt.subplots(figsize=(10, 5))

full_csv_path = f"c:\\Users\\elsam\\Downloads\\MEP\\Confocal Images\\{date}\\{pos}\\AllCells\\M_Results\\Results.csv"
full_files_path = f"c:\\Users\\elsam\\Downloads\\MEP\\Confocal Images\\{date}\\{pos}\\AllCells\\H_Results\\Files_list.csv"


#Calculate Difference from Average
full_stats_df = pd.read_csv(full_csv_path, usecols=features)
full_files_df = pd.read_csv(full_files_path, header=0,names=["ROI_label"])

full_whole_df = pd.concat([full_stats_df,full_files_df], axis=1)

#look at difference between value and mean
last_slice = df["ROI_label"].index[-1]    # get the last frame we are interested in (avoid unnecessary calculations)

# Calculate avg for each frame
adjusted_dfs = []  # List to collect adjusted values
running_dfs = []  # create a storage array that keeps track of the current haralick average

running_mean_den = np.zeros(len(features))  # create a storage array that keeps track of the current stats average denominator
running_mean_num = 0  # create a storage array that keeps track of the current stats average numerator


for slice in df["ROI_label"]:
    prefix = slice[:4]  #extract slice label
    
    # Get the means of all the stats in that slice
    slice_stats = full_whole_df[full_whole_df["ROI_label"].str.startswith(prefix, na=False)][features]

    # update running average values
    running_mean_den += slice_stats.sum().values
    running_mean_num += slice_stats.index[-1]

    running_mean = running_mean_den / running_mean_num

    means = slice_stats.mean().values # mean of the current frame
    
    # GEt the stats of the ROIs we are interested in
    relevant_ROIs = df[df["ROI_label"].str.startswith(prefix, na=False)][features]
    
    # Look at how far the individual interest stat is from the mean
    adjusted_slice = relevant_ROIs - means
    running_slice = relevant_ROIs - running_mean
    
    adjusted_dfs.append(adjusted_slice)
    running_dfs.append(running_slice)

adjusted_df, running_df = pd.concat(adjusted_dfs), pd.concat(running_dfs)   # make into df
adjusted_df, running_df = pd.concat([adjusted_df,files_df], axis=1), pd.concat([running_df,files_df], axis=1)   # add ROI_labels column


for cell in cells:
    csv_path = f"c:\\Users\\elsam\\Downloads\\MEP\\Confocal Images\\{date}\\{pos}\\{cell}\\M_Results\\Results.csv"

    files_path = f"c:\\Users\\elsam\\Downloads\\MEP\\Confocal Images\\{date}\\{pos}\\{cell}\\H_Results\\Files_list.csv"

    target_label = targets_dict[cell]

    stats_df = pd.read_csv(csv_path, usecols=features)
    files_df = pd.read_csv(files_path, header=0, names=["ROI_label"])
    df = pd.concat([stats_df, files_df], axis=1)

    matches = df.index[df["ROI_label"] == target_label]
    print(df.head(10))
    if len(matches) == 0:
        raise ValueError(f"No row found where ROI_label == {target_label!r}")

    target_idx = matches[0]



    #Plot normal std
    x = df.index - target_idx + ref_x
    ax.plot(x, df["StdDev"], marker="o", label=f"{cell[:4]} {cell[4:]}")

    # #Plot adjusted df
    # x= adjusted_df.index - target_idx + ref_x
    # ax.plot(x, adjusted_df["StdDev"], marker="o", label=f"Adjusted {cell[:4]} {cell[4:]}")

    # #Plot adjusted df using the running average
    # x= running_df.index - target_idx + ref_x
    # ax.plot(x, running_df["StdDev"], marker="o", label=f"Running {cell[:4]} {cell[4:]}")




ax.axvline(
    x=ref_x,
    color="red",
    linestyle="--",
    label="prophase frame"
)

ax.set_xlabel("Frame index aligned to prophase")
ax.set_ylabel("Standard Deviation")
ax.set_title("Standard Deviation over time frames")

ax.legend()
plt.tight_layout()
plt.show()