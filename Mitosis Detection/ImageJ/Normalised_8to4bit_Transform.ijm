macro "Normalised 8 to 4-bit Transform"{
	ogImage = getTitle();
	//outDir = getDirectory("choose location to store 4-bit image");

	width = getWidth();
	height = getHeight();
	slices = nSlices;

	run("8-bit");	//make sure image is 8 bits

	setBatchMode(true);
	for (i = 0; i < slices; i++) {	// in case image is a stack
		setSlice(i+1);
		getStatistics(area, mean, min, max, std, histogram);	// get the maximum value
		
		// Loop through each pixel
		for (y = 0; y < height; y++) {
			for (x = 0; x < width; x++) {
				
				val = getPixel(x, y); // Get current pixel value (0-255)
				
				// Map to normalised 0-15 range
				scaledVal = val * 15 / max;
				
				// Bin to the correct intensity
				newVal = Math.ceil(scaledVal);
				
				// Set the new pixel value
				putPixel(x, y, newVal);
			}
		}
		
	}
	setMinAndMax(0, 15);	// make image visible
	setBatchMode(false);


	// Save the resulting "4bit" image
	//saveAs("Tiff", outDir+substring(ogImage, 0, ogImage.length-4)+".tif");
}