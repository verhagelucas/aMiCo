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
experiments = ["20251128", "20251203", "20260129"]

output_directory = r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\Joint\haralick_offsets"

features = ["H2","H9"]


for offset in range(20):
    #create a place to store the whole dataframes
    all_whole_dfs = {d: [] for d in experiments}
    all_target_idxs = {d: [] for d in experiments}


    # extract data from the haralick values and calculate the condensation measure
    for i, path in enumerate(haralick_directories):
        haralick_df = pd.read_csv(path + f"\\Results_Haralick_off_{offset+1}.csv", usecols=features)
        files_df = pd.read_csv(path + r"\Files_list.csv", header=0, names=["ROI_label"])

        whole_df = pd.concat([haralick_df, files_df], axis=1)

        whole_df["condensation"] = whole_df["H2"]/whole_df["H9"]    # calculate condensation measure


        all_whole_dfs[experiments[i]].append(whole_df)
        all_target_idxs[experiments[i]].append(whole_df.index[whole_df["ROI_label"] == target_labels[i]][0])

    # define plotting function
    line_handles = [None] * len(haralick_directories)   #initialise line_handles for legend

    def plot_values(experiment):

                # extract the target index and the H features of the current experiment
                target_idx = all_target_idxs[experiment][0]
                whole_df_1 = all_whole_dfs[experiment][0]

                ref_x = 0  # align target labels to x=0

                aligned_x = whole_df_1.index - target_idx + ref_x # generate shifted x axis
                
                plt.plot(aligned_x, whole_df_1["condensation"], label= experiment)  # plot the experiments values
    \

                    # ax.set_xticks([ref_x])  # mark the frame to be identified
                    # ax.set_xticklabels(["target frame"])  # label the frame


    for experiment in experiments:
        plot_values(experiment)

    plt.title(f"H2/H9\nd={offset+1}")
    plt.legend()
    plt.axvline(x=0, color="black", linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
    # plt.savefig(output_directory+f"\\{d1}\\{d1}-{d2}.png", dpi=300, bbox_inches='tight')
