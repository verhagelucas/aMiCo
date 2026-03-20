//1) Run Candidate segmentation
// run("Candidate Segmentation");
// close("watershed_stack");
// close("Mask_1");

//2) Keep only ROIs of the one cell we want to track
// go through each ROI and decide keep/delete

//3)Crop out the selected ROIs
//get parent folder
parent_folder = getDirectory("image");
image_name = getTitle();
save_directory = parent_folder+"/Ind_ROIs"+image_name+"/"
//extract all ROIs
roiManager("Deselect");
RoiManager.multiCrop(save_directory, " save tif");

close("*");

//4)Open them up as individual files

// Get a list of all files in the directory
list = getFileList(save_directory);


// Loop through each file in the list
for (i = 0; i < list.length; i++) {
    // Get full file path & open it
    filePath = dir + list[i];
    open(filePath);
}




selectImage("0050-0004.tif");
run("HaralickFilter ", "image=0049-0204.tif offset=1");
selectImage("0049-0204.tif");
selectImage("0050-0004.tif");
run("HaralickFilter ", "image=0050-0004.tif offset=1");
selectImage("0050-0004.tif");
close;
run("Record...");
