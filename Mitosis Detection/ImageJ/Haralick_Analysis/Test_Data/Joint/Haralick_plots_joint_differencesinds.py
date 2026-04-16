'''
Plots each H feature difference between d=d1, and d=d2 (9-1)
'''
import matplotlib.pyplot as plt
import pandas as pd
import os

haralick_directories = [r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\20251128\haralick_offsets", 
                       r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\20251203\haralick_offsets", 
                       r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\20260129\haralick_offsets"]
target_labels = ["0030_0008", "0025_0004", "0020_0003"]
legend_labels = ["20251128", "20251203", "20260129"]

output_directory = r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\Joint\haralick_offsets"

features = ["H1","H2", "H3", "H4","H5","H6","H7","H8","H9","H10","H11"]
ds = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

for d1 in ds[:10]:
    os.makedirs(output_directory+f"\\{d1}")
    for d2 in ds:

        if d2==d1:
            continue

        # Pre-load data
        all_whole_dfs = {d: [] for d in [d1, d2]}
        all_target_idxs = {d: [] for d in [d1, d2]}


        for d in [d1, d2]:
            for i, path in enumerate(haralick_directories):
                haralick_df = pd.read_csv(path + f"\\Results_Haralick_off_{d}.csv", usecols=features)
                files_df = pd.read_csv(path + r"\Files_list.csv", header=0, names=["ROI_label"])

                whole_df = pd.concat([haralick_df, files_df], axis=1)

                all_whole_dfs[d].append(whole_df)
                all_target_idxs[d].append(whole_df.index[whole_df["ROI_label"] == target_labels[i]][0])


        # Figure 
        fig, axes = plt.subplots(3, 4, figsize=(16, 11))
        axes = axes.flatten()
        #fig.subplots_adjust(left=0.05, right=0.88, bottom=0.05, top=0.92)  # Make space for buttons


        line_handles = [None] * len(haralick_directories)   #initialise line_handles for legend

        def plot_offset(offset_label_1, offset_label_2):
            global line_handles


            target_idx = all_target_idxs[offset_label_1]
            whole_df_1 = all_whole_dfs[offset_label_1]
            whole_df_2 = all_whole_dfs[offset_label_2]

            ref_x = 0  # align target labels to x=0

            #reset plots
            for ax in axes:
                ax.clear()

            for i, h in enumerate(features):
                ax = axes[i]

                for j, df in enumerate(whole_df_1):
                    aligned_x = df.index - target_idx[j] + ref_x
                    df_2 = whole_df_2[j]

                    line, = ax.plot(aligned_x, df[h]-df_2[h], color=f"C{j}", marker='o', markersize=5)
                    if i == 0:
                        line_handles[j] = line  #only stored line handles 

                ax.axvline(x=ref_x, color="black", linestyle='--', alpha=0.5)

                ax.set_title(h) 
                ax.set_ylabel(f"{h} value")
                ax.set_xticks([ref_x])  # mark the frame to be identified
                ax.set_xticklabels(["target frame"])  # label the frame

            axes[-1].set_visible(False) # hide H12
            fig.suptitle(f"Haralick Features Over Time\nOffset = {offset_label_1} - Offset = {offset_label_2}", fontsize=16)
            fig.legend(handles=line_handles, labels=legend_labels, loc="upper left", bbox_to_anchor=(0.02, 0.98))


        # Initial plot FIXED
        plot_offset(d1,d2) 

        plt.tight_layout()
        plt.savefig(output_directory+f"\\{d1}\\{d1}-{d2}.png", dpi=300, bbox_inches='tight')
