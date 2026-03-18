macro "Process Z stack image"{
	
	getDimensions(width, height, channels, slices, frames);
	
	og_path = getDirectory("image");
	
	if (channels>1) {
		run("Split Channels");
		for (i = 0; i < channels-1; i++) {	//close the images containing channels that arent the first one(just bcs, no real reason why only the first one)
			close;
		}
	}
	
	im_name = getTitle(); //get whole title of the image

	run("Z Project...", "projection=[Max Intensity] all");	//project all slices to get maxZproj
	selectImage(im_name);	//select OG image	
	close;	//close OG image
	
	print("dir_saveROIs = " + og_path);	//DEBUGGING
	
	saveAs("Tiff", og_path+"/process.tif");
	
	run("Candidate Segmentation");
	
	run("Reset IJ");
}
