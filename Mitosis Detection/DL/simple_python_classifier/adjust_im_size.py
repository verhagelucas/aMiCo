macro_pad_image = """
#@ String path
#@ int new_size

// run("Bio-Formats Importer", "open=[" + path + "] autoscale color_mode=Colorized rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT");
run("Select path", "inputfile=[" + path + "]");
selectImage(1);

run("Canvas Size...", "width="+ new_size +" height="+ new_size +" position=Center zero"); // resize images to common size
saveAs("Tiff", path);

"""

