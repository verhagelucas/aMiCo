saveImages = getBoolean("Save ROI images?");
getHaralick = getBoolean("Calculate Haralicks?");

ogImage = getTitle();

numberOfROIs = roiManager("count");

if (saveImages) {
	outDir_images = getDirectory("Choose output directory for the cell images");
	max_offset=1;
}

if (getHaralick) {
	max_offset = getNumber("Calculate up to Haralick offset d = ", 5);
	label_list = newArray(numberOfROIs);
	outDir_results = getDirectory("Choose output directory for the Harlick results");
}

if (numberOfROIs>100) {	//if we are calculating the whole timelapse
	file_save_prefix = "Full_";
}else {
	file_save_prefix = "";
}

setBatchMode(true);
for (jj = 1; jj <= max_offset; jj++) {
	offset = jj;
	
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
		
		if (saveImages) {
		    saveAs("tif", outDir_images + save_name + ".tif");
		    close(save_name+".tif");
		}
		else {
			close(save_name);
		}
		
	}
	
	saveImages = false;	//if we want to save images only saved in the first run
	
	if (getHaralick) {
		// save Haralick results
		saveAs("Results", outDir_results+file_save_prefix+"Results_Haralick_d_"+offset+".csv");
		close("Results");
		
		if (!File.exists(outDir_results+file_save_prefix+"Files_list.csv")) {
			// save ROI_label information if not already saved
			Array.show("Files list", label_list);
			saveAs("Results", outDir_results+file_save_prefix+"Full_Files_list.csv");
			close(file_save_prefix+"Files_list.csv");
		}
		
		//Clean up UI
		close("Log");
	}
}
setBatchMode(false);
