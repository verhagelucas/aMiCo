//1) Run Candidate segmentation
// run("Candidate Segmentation");

//2) Keep only ROIs of the one cell we want to track
// go through each ROI and decide keep/delete

//3)Crop out the selected ROIs
// Define output directory
outDir = getDirectory("Choose output directory for the cell images");
//select offset for haralick calculations
save_ROIs = getBoolean("Save the individual ROI files?");

// Perform multi-crop to get a stack
roiManager("deselect");
RoiManager.multiCrop(outDir, "show");

// Go through all ROIs & Calculate haralick features
roiManager("List");
numberOfROIs = roiManager("count");
label_list = newArray(numberOfROIs);

for (haralick_offset = 1; haralick_offset <=20; haralick_offset++) {
	
	for (i = 0; i < numberOfROIs; i++) {
	    // Get the name of the ROI from the overlay
	    ROIName = getResultString("Name", i, "Overlay Elements of CROPPED_ROI Manager");
	    save_ROIName = substring(ROIName, 0, 4) + "_" + substring(ROIName, 10, ROIName.length);
	    label_list[i]=save_ROIName;	//store index of the file for later use in python
	    
	    // Select the specific slice in the cropped stack
	    selectWindow("CROPPED_ROI Manager");
	    setSlice(i + 1);
	    
	    // Duplicate the slice with the desired filename
	    run("Duplicate...", "title=" + save_ROIName);
	    
	    // Calculate Haralick features of image
	    run("HaralickFilter ", "image="+save_ROIName+" offset="+haralick_offset);
	    
	    // Save the duplicated image with the ROI name
	    if (save_ROIs) { saveAs("tif", outDir + save_ROIName + ".tif"); }
	
	    
	    // Close the temporary window
	    close();
	}
	
	//Clean up UI

	close("Log");
	
	// save Haralick results
	saveAs("Results", outDir+"Results_Haralick_off_"+haralick_offset+".csv");
	close("Results");
}


close("Overlay Elements of CROPPED_ROI Manager");
close("CROPPED_ROI Manager");
	
// save ROI_label information
Array.show("Files list", label_list);
saveAs("Results", outDir+"Files_list.csv");
close("Files_list.csv");
