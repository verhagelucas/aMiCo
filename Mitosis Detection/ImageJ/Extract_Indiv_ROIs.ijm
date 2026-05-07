saveImages = getBoolean("Save ROI images?");
getPlotProfile = getBoolean("Calculate Plot profiles?");
getHaralick = getBoolean("Calculate Haralicks?");

ogImage = getTitle();

numberOfROIs = roiManager("count");

if (saveImages) {
	outDir_images = getDirectory("Choose output directory for the cell images");
}
if (getHaralick) {
	offset = getNumber("Haralick offset d = ", 1);
	label_list = newArray(numberOfROIs);
}
if (getPlotProfile) {
	Table.create("Profile Plots");
}
if (getHaralick || getPlotProfile) {
	outDir_results = getDirectory("Choose output directory for the Harlick results");
}

setBatchMode(true);
for (roiIndex = 0; roiIndex < numberOfROIs; roiIndex++) {
	
	selectImage(ogImage);
	roiManager("select", roiIndex);
	ROIName = getInfo("roi.name");
	save_name = substring(ROIName, 0, 4) + "_" + substring(ROIName, 10, ROIName.length);
	run("Duplicate...", "title="+save_name);
	selectImage(save_name);
	setBackgroundColor(0, 0, 0);
	run("Clear Outside");
	run("Select None");
	
	if (getHaralick) {
		label_list[roiIndex]=save_name;	//store index of the file for later use in python
		// Calculate Haralick features of image
    	run("HaralickFilter ", "image="+save_name+" offset="+offset);
	}

	if (getPlotProfile) {
		getDimensions(width, height, channels, slices, frames);
		makeLine(0, height/2, width, height/2);
		profile = getProfile();
		Array.print(profile);
		Table.setColumn(save_name, profile);
	}

		
	if (saveImages) {
	    saveAs("tif", outDir_images + save_name + ".tif");
	}

	close(save_name);

}

setBatchMode(false);

if (getHaralick) {
	// save Haralick results
	saveAs("Results", outDir_results+"Results_Haralick_d_"+offset+".csv");
	close("Results");
	
	// save ROI_label information
	Array.show("Files list", label_list);
	saveAs("Results", outDir_results+"Files_list.csv");
	close("Files_list.csv");
	
	//Clean up UI
	close("Log");
}

