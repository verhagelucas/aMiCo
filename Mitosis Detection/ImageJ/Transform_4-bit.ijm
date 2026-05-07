ogImage = getTitle();
//outDir = getDirectory("choose location to store 4-bit image");

width = getWidth();
height = getHeight();
slices = nSlices;

run("8-bit");	//make sure image is 8 bits

for (i = 0; i < slices; i++) {
	setSlice(i+1);
	// Loop through each pixel
	for (y = 0; y < height; y++) {
	    for (x = 0; x < width; x++) {
	    	
	        val = getPixel(x, y); // Get current pixel value (0-255)
	        
	        // Map to 0-15 range by integer division by 16
	        newVal = val / 16;
	        
	        // Set the new pixel value
	        putPixel(x, y, newVal);
	    }
	}

}
setMinAndMax(0, 15);	// make image visible

// Save the resulting "4bit" image
//saveAs("Tiff", outDir+substring(ogImage, 0, ogImage.length-4)+".tif");