import matplotlib.pyplot as plt
import pandas as pd

haralick_directory = r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\20251211"
target_label = "0020_0003"  # label of the ROI with the condensed DNA
output_directory = r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\20251211"

features = ["H1","H2", "H3", "H4","H5","H6","H7","H8","H9","H10","H11"]

haralick_df = pd.read_csv(haralick_directory+r"\Results_Haralick.csv", 
                          usecols=features)
files_df = pd.read_csv(haralick_directory+r"\Files_list.csv",
                       header=0,names=["ROI_label"])

whole_df = pd.concat([haralick_df,files_df], axis=1)

# Find index of the target label

try:
    target_idx = whole_df.index[whole_df["ROI_label"] == target_label][0]
except IndexError:
    raise ValueError(f"Label {target_label} not found in ROI_label column")


# Create 3x4 grid of subplots
fig, axes = plt.subplots(3, 4, figsize=(16, 10), sharex=True)
axes = axes.flatten()  # make it 1D for easy indexing

for i, h in enumerate(features):
    ax = axes[i]
    ax.plot(whole_df.index, whole_df[h], marker='o', markersize = 5)
    ax.set_title(h)
    ax.set_ylabel(f"{h} value")

    # Only one tick at target position
    ax.set_xticks([target_idx])
    ax.set_xticklabels([f"DNA condensed\n{target_label}"], rotation=25, ha='right')

    # Vertical line at that timepoint
    ax.axvline(x=target_idx, color='red', linestyle='--', alpha=0.8)

# Hide the unused last subplot (since 3*4=12 and we have 11 features)
#axes[-1].set_visible(False)

fig.suptitle("Haralick Features Over Time", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96])  # leave space for suptitle

plt.savefig(output_directory+r"\Haralick_Features_Over_Time.png", dpi=300, bbox_inches='tight')

plt.show()