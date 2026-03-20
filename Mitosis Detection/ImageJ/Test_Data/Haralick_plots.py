import matplotlib.pyplot as plt
import pandas as pd

haralick_df = pd.read_csv(r".\Haralick_Results.csv", 
                          usecols=["H1","H2", "H3", "H4","H5","H6","H7","H8","H9","H10","H11"])
files_df = pd.read_csv(r".\Files_list_0.csv",
                       usecols=["names_list"])

print(haralick_df.head(5))
print(files_df.head(5))

whole_df = pd.concat([haralick_df,files_df], axis=1)

def plot_feature(df, feature_name):
    '''
    df: haralick df
    feature_name: string
    '''
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df[feature_name], marker='o')
    plt.xlabel("timepoint")
    plt.ylabel(f" {feature_name} values")
    plt.title(f"{feature_name} value over time")
    plt.show()





plot_feature(haralick_df, "H1")
plot_feature(haralick_df, "H2")
plot_feature(haralick_df, "H3")
plot_feature(haralick_df, "H7")

#plt.savefig(r'C:\Users\Student\Desktop\MmM\Code\Microscope_Control\Microscope Implementation\Test_Data\AAA.png', dpi=300, bbox_inches='tight')
#plt.xticks(haralick_df.index, files_df, rotation=45, ha='right')
#plt.tight_layout()