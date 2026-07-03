macro "Image Pre-processing"{
	title_OG = getTitle();
	og_path = getDirectory("image");

	keep = 1; // channel kept (indexed starting at 1)
	getDimensions(width, height, channels, slices, frames);
	
	//extract channel of interest
	if (channels>1) {
		run("Split Channels");

		selectImage("C"+keep+"-"+title_OG);

		close("\\Others");	//Close all but selected channel of interest
	}
	
	im_name = getTitle(); //get whole title of the image

	run("Z Project...", "projection=[Max Intensity] all");	//project all slices to get maxZproj
	selectImage(im_name);	//select OG image	
	close;	//close OG image
	
	saveAs("Tiff", og_path+"/process.tif");	// save singl-channel image for later use

}
