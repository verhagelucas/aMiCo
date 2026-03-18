macro "Segment Cells Own" {
//set parameters
ignore_edges = true;
min_sel_size = 0;

// Select directory in which to save ROIs
//dir_saveROIs = getDir("Select directory to save ROI list");
dir_saveROIs = getDirectory("image");

//Image pre-processing

title_OG = getTitle();
print("Title " + title_OG)	//debug
run("Duplicate...", "duplicate");
rename("Duplicated");


run("Gaussian Blur...", "sigma=4 stack");
run("Make Binary", "calculate black create");
rename("Mask_1");

close("Duplicated");
selectImage("Mask_1");
run("Fill Holes", "stack");
run("Duplicate...", "duplicate");
rename("Mask_2");

list_names = newArray(); //List to store names of the individual watershed files created
number_slices = nSlices


//watershed each frame and store name in list_names
for (i = 1; i <= number_slices; i++) {
	selectImage("Mask_2");
    setSlice(i);
	run("Distance Transform Watershed", "distances=[Borgefors (3,4)] output=[16 bits] normalize dynamic=1 connectivity=4");
	run("glasbey_on_dark");
	new_name = getTitle() + i;
	rename(new_name);
	list_names = Array.concat(list_names, getTitle());

}

close("Mask_2");

// make sure list_names are latest open in order & active
for (i = 0; i < list_names.length; i++) {
	showProgress(i, list_names.length+1);	//show progress bar
    selectWindow(list_names[i]);
}

// make a stack from all open images whose titles contain the word watershed (latest opened ones)
run("Images to Stack", "name=watershed_stack title=watershed use");
showProgress(1, 1);//clear progress bar

//get the ROIs from the watershed
run("Label image to composite ROIs", "rm=[RoiManager[size=2285, visible=true]]");

//REMOVE THE EDGE ROIs
if (ignore_edges) {
		
	nROIs = roiManager("count");
	width = getWidth();
	height = getHeight();
	
	
	for (roiIndex = 0; roiIndex < nROIs; roiIndex++) {	//loop over each ROI
		
	    roiManager("select", roiIndex);
	    
	    getBoundingRect(xMin, yMin, sel_width, sel_height);	// get ROI bounds
	    
	    // check border pixels against ROI bounds
	    if (xMin == 0 || xMin + sel_width == width || 
	    yMin == 0 || yMin + sel_height == height) { //if it's at the borders
	    	
	    	run("Clear", "slice");  // delete content in that ROI
	        roiManager("Delete");	//delete ROI as well
	        roiIndex --;	//check the new ROI that's taken the old one's place
	        nROIs = roiManager("count");	//set the new amount of ROIs for te loop
	        continue;
	    }
	    
	    if ( (sel_width <= min_sel_size) || (sel_height <= min_sel_size)){	//remove dots smaller than 
	    	run("Clear", "slice");  // delete content in that ROI
	        roiManager("Delete");	//delete ROI as well
	        roiIndex --;	//check the new ROI that's taken the old one's place
	        nROIs = roiManager("count");	//set the new amount of ROIs for te loop
	        continue;
	    }
	}
}
selectImage(title_OG);	//debugging
dir_saveROIs = getInfo("image.directory");	//debugging
print("dir_saveROIs = " + dir_saveROIs);	//DEBUGGING

roiManager("Save", dir_saveROIs + "_RoiSet.zip");


//measure and extract kurtosis measurements (along with the slide of them)
selectImage(title_OG);
run("Set Measurements...", "standard center perimeter bounding kurtosis stack display redirect=None decimal=3");	// set what will get measured
roiManager("Deselect");
roiManager("Measure");
saveAs("Results", dir_saveROIs + "_Results.csv");

}

//
//n = nResults;
//kurtosis_values = newArray(n);
//slide_numbers = newArray(n);
//for (i = 0; i < n; i++) {
//    kurtosis_values[i] = getResult("Kurt", i);
//    slide_numbers[i] = getResult("Slice", i);
//}
//





//Array.print(slide_numbers);
//Array.print(kurtosis_values);

//Array.show("Kurtosis", slide_numbers, kurtosis_values);

//Plot.create ("Kurtosis", "slice", "kurtosis");
//Plot.setLimits (0, 15, 0, 60);
//Plot.setFrameSize (300, 200);
//Plot.setBackgroundColor ("lightgray");
//Plot.setColor ("blue", "red");
//Plot.setLineWidth (2);
//Plot.add ("triangle", kurtosis_values, slide_numbers);
//Plot.setColor ("red", "red");
//Plot.setLineWidth (1);
//Plot.add ("line", data)
//Plot.show ();