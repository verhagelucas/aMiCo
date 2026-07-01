ogImage = getTitle();

numberOfROIs = roiManager("count");
normalised_4bit = false;
global_4bit = false;
gaussian = false;

//max_offset = getNumber("Calculate up to Haralick offset d = ", 5);
starting_offset = 1
max_offset = 10;	//TODO: make into @int input
label_list = newArray(numberOfROIs);
outDir_results = getDirectory("Choose output directory for the Harlick results");	//TODO: make into @string input


for (roiIndex = 0; roiIndex < numberOfROIs; roiIndex++) {
	//go through the ROIs and extract the cells into individual images
	// (this has to happen outside of batch mode to open the image files
		
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
}
//take out all indiv cells


setBatchMode(true);
for (offset = starting_offset; offset <= max_offset; offset+=9) {
	//loop over the diff haralick distances to calculate
		
	for (i = 0; i < lengthOf(label_list); i++) {

		save_name = label_list[i];
		//Transform cell into normalised 4-bit image the first time haralick is calculated
		if (offset==starting_offset) {
			selectImage(save_name);
			if (normalised_4bit){
				run("Normalised Transform 4-bit");
				postfix="_n4bit";
			}
			else if(global_4bit){
				run("Transform 4-bit");
				postfix="_4bit";
			}
			else if (gaussian) {
				postfix="_gauss";
			}
			else {
				postfix="_normal";
			}
			
		}

		// Calculate Haralick features of transformed image
    	run("HaralickFilter ", "image="+save_name+" offset="+offset);
		
	}
	
	saveImages = false;	//if we want to save images only saved in the first run
	

	
	// save Haralick results
	saveAs("Results", outDir_results+"Results_Haralick_d_"+offset+postfix+".csv");
	close("Results");
	
	if (!File.exists(outDir_results+"Files_list.csv")) {
		// save ROI_label information if not already saved
		Array.show("Files list", label_list);
		saveAs("Results", outDir_results+"Files_list.csv");
		close("Files_list.csv");
	}
	
	//Clean up UI
	close("Log");
}
///REMOVE IN SCRIPTING MACRO
run("Select None");
roiManager("delete");

setBatchMode(false);
selectImage(ogImage);
close("\\Others");	//Close all images

