import matplotlib.pyplot as plt
import pandas as pd

haralick_df = pd.read_csv(r"c:\Users\Student\OneDrive-Maz\OneDrive - Erasmus University Rotterdam\MEP\Maria\confocal\20251128\maxZprojStacks\Ind_ROIs_C1Pos001Zoomed\Haralick_Results.csv", 
                          usecols=["H1","H2", "H3", "H4","H5","H6","H7","H8","H9","H10","H11"])
files_df = pd.read_csv(r"c:\Users\Student\OneDrive-Maz\OneDrive - Erasmus University Rotterdam\MEP\Maria\confocal\20251128\maxZprojStacks\Ind_ROIs_C1Pos001Zoomed\Files_list_0.csv",
                       usecols=["names_list"])

print(haralick_df.head(5))
print(files_df.head(5))

whole_df = pd.concat([haralick_df,files_df], axis=1)
h1 = haralick_df["H1"]


plt.figure(figsize=(10, 6))
plt.plot(haralick_df.index, haralick_df['H1'], marker='o', label="H1")
plt.plot(haralick_df.index, haralick_df['H2'], marker='o', label="H2")
plt.plot(haralick_df.index, haralick_df['H3'], marker='o', label="H3")
plt.plot(haralick_df.index, haralick_df['H4'], marker='o', label="H4")
plt.xlabel('timepoint')
plt.ylabel('Feature values')
plt.title('Feature values across times')
plt.legend()
#plt.savefig(r'C:\Users\Student\Desktop\MmM\Code\Microscope_Control\Microscope Implementation\Test_Data\AAA.png', dpi=300, bbox_inches='tight')
#plt.xticks(haralick_df.index, files_df, rotation=45, ha='right')
#plt.tight_layout()
plt.show()