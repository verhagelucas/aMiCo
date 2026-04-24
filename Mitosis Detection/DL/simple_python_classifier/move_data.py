import os, shutil
import pandas as pd
import random 

# os.environ["JAVA_HOME"]=r"c:\Users\Student\miniforge3\envs\newAPI_env\Library\jre"
# ij = imagej.init(r"c:\Users\Student\Documents\Fiji\Fiji.app", mode = "interactive")

# #region extract images
# root_dir = r"c:\\Users\\Student\\OneDrive-Maz\\OneDrive - Erasmus University Rotterdam\\MEP\\Maria\\Haralick Analysis\\Included"
# true_dir = r"C:\\Users\\Student\\Desktop\\MmM\\Code\\Microscope_Control\\Mitosis Detection\\DL\\data-mitosis\\all_topleft\\1"
# false_dir = r"C:\\Users\\Student\\Desktop\\MmM\\Code\\Microscope_Control\\Mitosis Detection\\DL\\data-mitosis\\all_topleft\\0"
# labels = pd.read_csv(r"C:\\Users\\Student\\Desktop\\MmM\\Code\\Microscope_Control\\Mitosis Detection\\DL\\Labelled1.csv")

# position_paths = set(list(zip(labels["Experiment"], labels["Folder"])))

# correct_counter = 0
# path_counter = 0
# for path in position_paths:
#     print("currently at: ", path, f"{path_counter+1} out of  {len(position_paths)}")
#     current_dir = f"{root_dir}\\{path[0]}\\{path[1]}"
#     files = os.listdir(current_dir) #get file list of all images in the experiment's postion
#     previous  = list((labels[(labels["Experiment"] == path[0]) & (labels["Folder"] == path[1])]["Previous"]).dropna())
#     targets = list((labels[(labels["Experiment"] == path[0]) & (labels["Folder"] == path[1])]["Target"]).dropna()) # extract taget labels
#     laters  = list((labels[(labels["Experiment"] == path[0]) & (labels["Folder"] == path[1])]["Later"]).dropna())
#     ignore = list((labels[(labels["Experiment"] == path[0]) & (labels["Folder"] == path[1])]["Ignore"]).dropna()) # extract labels to ignore
#     frame_ignore = list((labels[(labels["Experiment"] == path[0]) & (labels["Folder"] == path[1])]["Frame_Ignore"]).dropna())  #select the frames for each experiment that must be ignored
#     print(frame_ignore)
#     for file in files:
#         if file[-3:] == "csv" or file[-3:] == "zip":
#             continue    # if file is not an image: ignore it and move on

        
#         if file[:-4] in ignore:
#             continue
#         elif int(file[:4]) in frame_ignore:
#             continue
#         elif (file[:-4] in previous) or (file[:-4] in targets) or (file[:-4] in laters):    # if name of file without extension in target list
#             correct_counter += 1
#             shutil.copy(f"{current_dir}\\{file}", f"{true_dir}\\{path[0]}_{path[1]}_{file}") # copy file to the true folder"
#         # elif file[:-4] in laters:    # if name of file without extension in target list
#         #     correct_counter += 1
#         #     shutil.copy(f"{current_dir}\\{file}", f"{true_dir}\\{path[0]}_{path[1]}_{file}") # copy file to the true folder"
#         else:
#             shutil.copy(f"{current_dir}\\{file}", f"{false_dir}\\{path[0]}_{path[1]}_{file}")
#     path_counter += 1

# if labels["Target"].dropna().shape[0] == correct_counter:
#     print("all targets correctly passed")
# print("DONE")

# #endregion


# #region divide dataset
# all_dir = r"C:\\Users\\Student\\Desktop\\MmM\\Code\\Microscope_Control\\Mitosis Detection\\DL\\data-mitosis\\all_topleft"
# train_dir = r"C:\\Users\\Student\\Desktop\\MmM\\Code\\Microscope_Control\\Mitosis Detection\\DL\\data-mitosis\\train_topleft"
# val_dir = r"C:\\Users\\Student\\Desktop\\MmM\\Code\\Microscope_Control\\Mitosis Detection\\DL\\data-mitosis\\val_topleft"

# for file in os.listdir(f"{all_dir}\\0"):
#     if random.random()>0.3:
#         shutil.copy(f"{all_dir}\\0\\{file}", f"{train_dir}\\0")
#     else:
#         shutil.copy(f"{all_dir}\\0\\{file}", f"{val_dir}\\0")

# for file in os.listdir(f"{all_dir}\\1"):
#     if random.random()>0.3:
#         shutil.copy(f"{all_dir}\\1\\{file}", f"{train_dir}\\1")
#     else:
#         shutil.copy(f"{all_dir}\\1\\{file}", f"{val_dir}\\1")

# print("DONE")
# #endregion



#region make 50/50 split

train_dir = r"C:\\Users\\Student\\Desktop\\MmM\\Code\\Microscope_Control\\Mitosis Detection\\DL\\data-mitosis\\train_topleft"

class1, class0 = os.listdir(f"{train_dir}\\1"), os.listdir(f"{train_dir}\\0")
len0_og = len(class0)

for i in range(len0_og-len(class1)):
    #randomly select a random image to be popped out
    idx = random.randint(0,len(class0)-1)
    os.remove(f"{train_dir}\\0\\{class0[idx]}") # delete file
    class0.pop(idx) # remove from list

print("DONE")
#endregion