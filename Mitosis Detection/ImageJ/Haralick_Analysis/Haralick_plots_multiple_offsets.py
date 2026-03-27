import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

directory = Path(r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\20260129\haralick_offsets")
haralick_files = list(directory.rglob("Results_Haralick_off_*.csv"))
names_file = Path(r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\20260129\Files_list.csv")

target_label = "0020_0003"  # label of the ROI with the condensed DNA

features = ["H1","H2", "H3", "H4","H5","H6","H7","H8","H9","H10","H11"]

whole_dfs = []
#target_idxs = []

files_df = pd.read_csv(names_file, header=0,names=["ROI_label"])    ##outside for loop because only need once

for i, file in enumerate(haralick_files):
    haralick_df = pd.read_csv(file, usecols=features)
    

    whole_df = pd.concat([haralick_df,files_df], axis=1)
    whole_dfs.append(whole_df)

## get index of target label only once because it's the same for all dataframes
try:
    target_idx = whole_df.index[whole_df["ROI_label"] == target_label][0]
except IndexError:
    raise ValueError(f"Label {target_label} not found in ROI_label column")


# Extract target rows and build target_df
target_point_df = []
for i, df in enumerate(whole_dfs):
    target_row = df[df["ROI_label"]==target_label].copy() 
    target_row['haralick_d'] = i+1
    target_point_df.append(target_row)

target_df = pd.concat(target_point_df, ignore_index=True)
print(target_df)
del target_df["ROI_label"]
    

# Create 3x4 grid of subplots
fig, axes = plt.subplots(3, 4, figsize=(16, 10), sharex=True)
axes = axes.flatten()  # make it 1D for easy indexing

for i, h in enumerate(features):
    ax = axes[i]
    ax.plot(target_df.index+1, target_df[h], marker='o', markersize = 5)
    ax.set_title(h)
    ax.set_ylabel(f"{h} value")

# Hide the unused last subplot (since 3*4=12 and we have 11 features)
#axes[-1].set_visible(False)

fig.suptitle("Haralick Features Across different offsets", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96])  # leave space for suptitle

plt.savefig(directory / Path(r"Haralick_Features_Over_Offset.png"), dpi=300, bbox_inches='tight')

plt.show()