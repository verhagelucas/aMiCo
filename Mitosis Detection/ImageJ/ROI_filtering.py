import pandas as pd
import numpy as np
from tkinter import filedialog
import os
import shutil, glob
import re
import zipfile

filter_choice = "Kurt"
min_threshold = 0.2
max_threshold = 0.4


file_path = filedialog.askopenfilename( #select excel file to be analysed
    title="Select a results file to analyse",
    filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
)
directory = os.path.dirname(file_path)  #extract directory path

data = pd.read_csv(file_path)

zip_file_path = filedialog.askopenfilename( #select zip file to be extracted
    title="Select ROI zipped folder to extract",
    filetypes=(("Zip Folder", "*.zip"), ("All files", "*.*"))
)

#extract zipped ROIs into folder called RoiSet
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(f"{directory}/RoiSet/")

filtered_ROIs_dir = f"{directory}/filtered_cells_{filter_choice}{min_threshold}-{max_threshold}"
os.mkdir(filtered_ROIs_dir)     #make dir to store filtered ROIs


filtered_ROIs_path = f"{directory}/filtered_cells_{filter_choice}{min_threshold}-{max_threshold}.csv"  #create new csv file to store the detected cells in


#region data manipulation

filtered_data = data[data[filter_choice]>min_threshold] # filter data that is greater than the selected threshold
filtered_data = filtered_data[filtered_data[filter_choice]<max_threshold]

selected_ROIs = filtered_data["Label"].tolist()
print(selected_ROIs)

filtered_data.to_csv(filtered_ROIs_path)

for roi in selected_ROIs:

    #clean out label name to get the ROI name
    roi_name = roi.replace("C1-Position001-dividing_cells.tif:","")
    roi_name = re.sub(r":\d+","",roi_name)

    #copy the selected files to the new folder
    for image in glob.glob(f"{directory}/RoiSet/{roi_name}.*"):
        shutil.copy(image,filtered_ROIs_dir)


# zip it up into a folder to import all ROIs at once
shutil.make_archive(f'{directory}/FilteredRois', 'zip', filtered_ROIs_dir)

#delete unzipped folder
shutil.rmtree(f"{directory}/RoiSet/")