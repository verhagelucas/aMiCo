import matplotlib.pyplot as plt
import pandas as pd


haralick_directory1 = r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\20251128"
target_label1 = "0030_0008"  # label of the ROI with the condensed DNA

haralick_directory2 = r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\20251203"
target_label2 = "0025_0004"  # label of the ROI with the condensed DNA

haralick_directory3 = r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\20260129"
target_label3 = "0020_0003"  # label of the ROI with the condensed DNA

output_directory = r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\Joint"

features = ["H1","H2", "H3", "H4","H5","H6","H7","H8","H9","H10","H11"]

haralick_df1 = pd.read_csv(haralick_directory1+r"\Results_Haralick.csv", usecols=features)
haralick_df2 = pd.read_csv(haralick_directory2+r"\Results_Haralick.csv", usecols=features)
haralick_df3 = pd.read_csv(haralick_directory3+r"\Results_Haralick.csv", usecols=features)

files_df1 = pd.read_csv(haralick_directory1+r"\Files_list.csv", header=0, names=["ROI_label"])
files_df2 = pd.read_csv(haralick_directory2+r"\Files_list.csv", header=0, names=["ROI_label"])
files_df3 = pd.read_csv(haralick_directory3+r"\Files_list.csv", header=0, names=["ROI_label"])

whole_df1 = pd.concat([haralick_df1,files_df1], axis=1)
whole_df2 = pd.concat([haralick_df2,files_df2], axis=1)
whole_df3 = pd.concat([haralick_df3,files_df3], axis=1)

# Find index of the target label

try:
    target_idx1 = whole_df1.index[whole_df1["ROI_label"] == target_label1][0]
except IndexError:
    raise ValueError(f"Label {target_label1} not found in ROI_label column")

try:
    target_idx2 = whole_df2.index[whole_df2["ROI_label"] == target_label2][0]
except IndexError:
    raise ValueError(f"Label {target_label2} not found in ROI_label column")

try:
    target_idx3 = whole_df3.index[whole_df3["ROI_label"] == target_label3][0]
except IndexError:
    raise ValueError(f"Label {target_label3} not found in ROI_label column")


# Create 3x4 grid of subplots
fig, axes = plt.subplots(3, 4, figsize=(16, 10), sharex=True)
axes = axes.flatten()  # make it 1D for easy indexing

for i, h in enumerate(features):
    ax = axes[i]
    l1, = ax.plot(whole_df1.index, whole_df1[h], color="C0", marker='o', markersize = 5, label="20251128")
    l2, = ax.plot(whole_df2.index, whole_df2[h], color="C1", marker='o', markersize = 5, label="20251203")
    l3, = ax.plot(whole_df3.index, whole_df3[h], color="C2", marker='o', markersize = 5, label="20260129")
    ax.set_title(h)
    ax.set_ylabel(f"{h} value")

    # three ticks, one per target index
    ax.set_xticks([target_idx1, target_idx2, target_idx3])
    ax.set_xticklabels(
        [f"{target_label1}",
         f"{target_label2}",
         f"{target_label3}"],
        rotation=25, ha='right'
    )

    # Vertical line at that timepoint
    ax.axvline(x=target_idx1, color="C0", linestyle='--', alpha=0.8)
    ax.axvline(x=target_idx2, color="C1", linestyle='--', alpha=0.8)
    ax.axvline(x=target_idx3, color="C2", linestyle='--', alpha=0.8)

# Hide the unused last subplot (since 3*4=12 and we have 11 features)
#axes[-1].set_visible(False)

fig.suptitle("Haralick Features Over Time", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96])  # leave space for suptitle


# Single figure legend with your dates (C0=20251128, etc.)
fig.legend(
    handles=[l1, l2, l3],  # from first subplot lines
    labels=["20251128", "20251203", "20260129"],
    loc="upper right",
    bbox_to_anchor=(0.98, 0.98)
)

plt.savefig(output_directory+r"\Haralick_Features_Over_Time.png", dpi=300, bbox_inches='tight')

plt.show()

##################

# import matplotlib.pyplot as plt
# import pandas as pd

# haralick_directories = [r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\20251128", r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\20251203", r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\20260129"]
# target_labels = ["0030_0008", "0025_0004", "0020_0003"]

# output_directory = r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\Joint"

# features = ["H1","H2", "H3", "H4","H5","H6","H7","H8","H9","H10","H11"]


# whole_dfs=[]
# target_idx=[]

# for i, path in haralick_directories:
#     haralick_df = pd.read_csv(path+r"\Results_Haralick.csv", usecols=features)
#     files_df = pd.read_csv(path+r"\Files_list.csv", header=0, names=["ROI_label"])
#     whole_df = pd.concat([haralick_df,files_df], axis=1)
#     whole_dfs.append(whole_df)

#     # Find index of the target label
#     try:
#         target_idx.append(whole_df.index[whole_df["ROI_label"] == target_labels[i]][0])
#     except IndexError:
#         raise ValueError(f"Label {target_labels[i]} not found in ROI_label column")






# # Create 3x4 grid of subplots
# fig, axes = plt.subplots(3, 4, figsize=(16, 10), sharex=True)
# axes = axes.flatten()  # make it 1D for easy indexing

# lines = [l1,l2,l3]
# for i, h in enumerate(features):
#     ax = axes[i]
#     for j, df in whole_dfs:
#         lines[j], = ax.plot(df.index, df[h], color="C0", marker='o', markersize = 5)
        
#     ax.set_title(h)
#     ax.set_ylabel(f"{h} value")

#     # three ticks, one per target index
#     ax.set_xticks([target_idx1, target_idx2, target_idx3])
#     ax.set_xticklabels(
#         [f"{target_label1}",
#          f"{target_label2}",
#          f"{target_label3}"],
#         rotation=25, ha='right'
#     )

#     # Vertical line at that timepoint
#     ax.axvline(x=target_idx1, color="C0", linestyle='--', alpha=0.8)
#     ax.axvline(x=target_idx2, color="C1", linestyle='--', alpha=0.8)
#     ax.axvline(x=target_idx3, color="C2", linestyle='--', alpha=0.8)

# # Hide the unused last subplot (since 3*4=12 and we have 11 features)
# #axes[-1].set_visible(False)

# fig.suptitle("Haralick Features Over Time", fontsize=16)
# plt.tight_layout(rect=[0, 0, 1, 0.96])  # leave space for suptitle


# # Single figure legend with your dates (C0=20251128, etc.)
# fig.legend(
#     handles=[l1, l2, l3],  # from first subplot lines
#     labels=["20251128", "20251203", "20260129"],
#     loc="upper right",
#     bbox_to_anchor=(0.98, 0.98)
# )

# plt.savefig(output_directory+r"\Haralick_Features_Over_Time.png", dpi=300, bbox_inches='tight')

# plt.show()