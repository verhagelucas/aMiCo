import matplotlib.pyplot as plt
import pandas as pd

haralick_directories = [r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\20251128\haralick_offsets", 
                        r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\20251203\haralick_offsets", 
                        r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\20260129\haralick_offsets"]
target_labels = ["0030_0008", "0025_0004", "0020_0003"]
legend_labels = ["20251128", "20251203", "20260129"]

output_directory = r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\Joint\haralick_offsets"


features = ["H1","H2", "H3", "H4","H5","H6","H7","H8","H9","H10","H11"]

for d in range(1,21):
    whole_dfs=[]
    target_idx=[]

    # initialise the dataframes
    for i, path in enumerate(haralick_directories):
        haralick_df = pd.read_csv(path+f"\\Results_Haralick_off_{d}.csv", usecols=features)
        files_df = pd.read_csv(path+r"\Files_list.csv", header=0, names=["ROI_label"])
        whole_df = pd.concat([haralick_df,files_df], axis=1)
        whole_dfs.append(whole_df)

        # Find index of the target label
        try:
            target_idx.append(whole_df.index[whole_df["ROI_label"] == target_labels[i]][0])
        except IndexError:
            raise ValueError(f"Label {target_labels[i]} not found in ROI_label column")






    # Create 3x4 grid of subplots
    fig, axes = plt.subplots(3, 4, figsize=(16, 10), sharex=True)
    axes = axes.flatten()  # make it 1D for easy indexing

    line_handles = [None] * len(whole_dfs)  # initialise line_handles used for legend

    # loop over all features and plot all experiments feature values for each
    for i, h in enumerate(features):
        ax = axes[i]

        for j, df in enumerate(whole_dfs):
            line, = ax.plot(df.index, df[h], color=f"C{j}", marker='o', markersize = 5)

            # save line handle only in case of the first graph
            if i == 0: 
                line_handles[j] = line

            # Vertical line at DNA division timepoint
            ax.axvline(x=target_idx[j], color=f"C{j}", linestyle='--', alpha=0.8)
            
        ax.set_title(h)
        ax.set_ylabel(f"{h} value")

        # three ticks, one per target index
        ax.set_xticks(target_idx)
        ax.set_xticklabels( target_labels, rotation=25, ha='right'    )


    # Hide the unused last subplot (since 3*4=12 and we have 11 features)
    #axes[-1].set_visible(False)

    fig.suptitle(f"Haralick Features Over Time\nOffset = {d}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # leave space for suptitle


    # Single figure legend with your dates (C0=20251128, etc.)
    fig.legend(
        handles=line_handles,  # from first subplot lines
        labels=legend_labels,
        loc="upper right",
        bbox_to_anchor=(0.98, 0.98)
    )

    plt.savefig(output_directory+f"\\Haralick_Features_Over_Time_off_{d}.png", dpi=300, bbox_inches='tight')

    # plt.show()