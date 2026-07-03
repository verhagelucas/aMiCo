macro "Extract Haralick Measurements"{
	ogImage = getTitle();

	numberOfROIs = roiManager("count");
	normalised_4bit = false;
	gaussian = false;


	starting_offset = 1
	max_offset = 10;	//TODO: make into @int input
	label_list = newArray(numberOfROIs);
	outDir_results = getDirectory("image");	//TODO: make into @string input


	//go through the ROIs and extract the cells into individual images
	// setBatchMode(true);
	for (roiIndex = 0; roiIndex < numberOfROIs; roiIndex++) {
		// (this has to happen outside of batch mode to open the image files)

			//find the cell in the overall image
			selectImage(ogImage);
			roiManager("select", roiIndex);
			ROIName = getInfo("roi.name");
			save_name = substring(ROIName, 0, 4) + "_" + substring(ROIName, 10, ROIName.length);

			//extract the cell to its own image
			run("Duplicate...", "title="+save_name);
			selectImage(save_name);
			setBackgroundColor(0, 0, 0);
			run("Clear Outside");
			run("Select None");

			label_list[roiIndex]=save_name;	//store file name for later use in haralick calculation and python

			//Pre-process image if needed
			selectImage(save_name);
			if (normalised_4bit){
				run("Normalised 8to4bit Transform");
				postfix="_n4bit";
			}
			else if (gaussian) {
				run("Gaussian Blur...", "sigma=2 stack");
				postfix="_gauss";
			}
			else {
				postfix="_normal";
			}
				
	}
	// setBatchMode("exit and display");



	//Measure Haralick using boundary offsets of the extracted individual cells
	setBatchMode(true);
	for (offset = starting_offset; offset <= max_offset; offset+=(max_offset-starting_offset)) {
			
		for (i = 0; i < lengthOf(label_list); i++) {	//go through all segmented nuclei

			save_name = label_list[i];
			// Calculate Haralick features of the nuclear image
			run("HaralickFilter ", "image="+save_name+" offset="+offset);
			
		}
		
		// save Haralick results
		saveAs("Results", outDir_results+"Results_Haralick_d_"+offset+postfix+".csv");
		close("Results");
		
		// save ROI_label name list only on the first run
		if (offset == starting_offset) {
			Array.show("Files list", label_list);
			saveAs("Results", outDir_results+"Files_list.csv");
			close("Files_list.csv");
		}
		
		//Clean up UI
		close("Log");
	}

	setBatchMode(false);
	selectImage(ogImage);
	close("\\Others");	//Close all non-OG images

}