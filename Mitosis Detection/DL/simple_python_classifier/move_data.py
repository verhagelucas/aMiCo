import os, shutil
import pandas as pd
import random 

#region extract images
root_dir = r"c:\\Users\\Student\\OneDrive-Maz\\OneDrive - Erasmus University Rotterdam\\MEP\\Maria\\Haralick Analysis\\Included"
true_dir = r"C:\\Users\\Student\\Desktop\\MmM\\Code\\Microscope_Control\\Mitosis Detection\\DL\\data-mitosis\\all\\1"
false_dir = r"C:\\Users\\Student\\Desktop\\MmM\\Code\\Microscope_Control\\Mitosis Detection\\DL\\data-mitosis\\all\\0"
labels = pd.read_csv(r"C:\\Users\\Student\\Desktop\\MmM\\Code\\Microscope_Control\\Mitosis Detection\\DL\\Labelled1.csv", usecols=["Experiment", "Folder", "Target"])

position_paths = set(list(zip(labels["Experiment"], labels["Folder"])))

correct_counter = 0
for path in position_paths:

    current_dir = f"{root_dir}\\{path[0]}\\{path[1]}"
    files = os.listdir(current_dir) #get file list of all images in the experiment's postion
    targets = list(labels[(labels["Experiment"] == path[0]) & (labels["Folder"] == path[1])]["Target"]) # extract taget labels

    for file in files:
        if file[-3:] == "csv" or file[-3:] == "zip":
            continue    # if file is not an image: ignore it and move on

        if file[:-4] in targets:    # if name of file without extension in target list
            correct_counter += 1
            shutil.copy(f"{current_dir}\\{file}", true_dir) # copy file to the true folder
        else:
            shutil.copy(f"{current_dir}\\{file}", false_dir)


if labels["Target"].dropna().shape[0] == correct_counter:
    print("all targets correctly passed")

#endregion

#region divide dataset
all_dir = r"C:\\Users\\Student\\Desktop\\MmM\\Code\\Microscope_Control\\Mitosis Detection\\DL\\data-mitosis\\all"
train_dir = r"C:\\Users\\Student\\Desktop\\MmM\\Code\\Microscope_Control\\Mitosis Detection\\DL\\data-mitosis\\train"
val_dir = r"C:\\Users\\Student\\Desktop\\MmM\\Code\\Microscope_Control\\Mitosis Detection\\DL\\data-mitosis\\val"

for file in os.listdir(f"{all_dir}\\0"):
    if random.random()>0.3:
        shutil.copy(f"{all_dir}\\0\\{file}", f"{train_dir}\\0")
    else:
        shutil.copy(f"{all_dir}\\0\\{file}", f"{val_dir}\\0")

for file in os.listdir(f"{all_dir}\\1"):
    if random.random()>0.3:
        shutil.copy(f"{all_dir}\\1\\{file}", f"{train_dir}\\1")
    else:
        shutil.copy(f"{all_dir}\\1\\{file}", f"{val_dir}\\1")
#endregion