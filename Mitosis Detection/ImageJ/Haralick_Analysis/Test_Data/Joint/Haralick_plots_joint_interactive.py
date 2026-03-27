import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.widgets import Slider
import os

haralick_directories = [r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\20251128\haralick_offsets", 
                       r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\20251203\haralick_offsets", 
                       r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\20260129\haralick_offsets"]
target_labels = ["0030_0008", "0025_0004", "0020_0003"]
legend_labels = ["20251128", "20251203", "20260129"]

output_directory = r"Mitosis Detection\ImageJ\Haralick_Analysis\Test_Data\Joint\haralick_offsets"
os.makedirs(output_directory, exist_ok=True)

features = ["H1","H2", "H3", "H4","H5","H6","H7","H8","H9","H10","H11"]

# Pre-load ALL data for offsets 1-20
all_whole_dfs = {d: [] for d in range(1, 21)}
all_target_idxs = {d: [] for d in range(1, 21)}

for d in range(1, 21):
    for i, path in enumerate(haralick_directories):
        haralick_df = pd.read_csv(path + f"\\Results_Haralick_off_{d}.csv", usecols=features)
        files_df = pd.read_csv(path + r"\Files_list.csv", header=0, names=["ROI_label"])
        whole_df = pd.concat([haralick_df, files_df], axis=1)
        all_whole_dfs[d].append(whole_df)
        
        try:
            all_target_idxs[d].append(whole_df.index[whole_df["ROI_label"] == target_labels[i]][0])
        except IndexError:
            raise ValueError(f"Label {target_labels[i]} not found in ROI_label column for offset {d}")

# Create figure with 3x4 subplots + slider space
fig, axes = plt.subplots(3, 4, figsize=(16, 12))
axes = axes.flatten()
fig.subplots_adjust(bottom=0.15)  # Space for slider

# Initial plot for offset=1
current_offset = 1
target_idx = all_target_idxs[current_offset]
line_handles = [None] * len(haralick_directories)

def plot_offset(offset_val):
    global current_offset
    current_offset = int(offset_val)
    target_idx = all_target_idxs[current_offset]
    whole_dfs = all_whole_dfs[current_offset]
    
    # Clear all subplots
    for ax in axes:
        ax.clear()
    
    # Plot features
    for i, h in enumerate(features):
        ax = axes[i]
        for j, df in enumerate(whole_dfs):
            line, = ax.plot(df.index, df[h], color=f"C{j}", marker='o', markersize=5)
            if i == 0:
                line_handles[j] = line
            ax.axvline(x=target_idx[j], color=f"C{j}", linestyle='--', alpha=0.8)
        
        ax.set_title(h)
        ax.set_ylabel(f"{h} value")
        ax.set_xticks(target_idx)
        ax.set_xticklabels(target_labels, rotation=25, ha='right')
    
    # Hide unused subplot
    axes[-1].set_visible(False)
    
    # Update title and legend
    fig.suptitle(f"Haralick Features Over Time\nOffset = {current_offset}", fontsize=16)
    fig.legend(handles=line_handles, labels=legend_labels, loc="upper right", bbox_to_anchor=(0.98, 0.98))
    
    fig.canvas.draw_idle()

# Initial plot
plot_offset(1)

# Add slider
ax_slider = fig.add_axes([0.2, 0.02, 0.6, 0.03])
slider = Slider(ax_slider, 'Offset', 1, 20, valinit=1, valstep=1, valfmt='%d')

# Connect slider
slider.on_changed(plot_offset)

plt.tight_layout(rect=[0, 0.08, 1, 0.96])

# Save interactive plot (optional static snapshot)
plt.savefig(output_directory + "\\Haralick_Features_Over_Time_interactive.png", dpi=300, bbox_inches='tight')
plt.show()