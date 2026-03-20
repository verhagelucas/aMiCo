// Get a list of all files in the directory
close("*");
dir = "C:/Users/Student/OneDrive-Maz/OneDrive - Erasmus University Rotterdam/MEP/Maria/confocal/20251128/maxZprojStacks/Ind_ROIs_C1Pos001Zoomed/";
names_list = getFileList(dir);
indexes = newArray(names_list.length);

// Loop through each file in the list
for (i = 0; i < names_list.length; i++) {
    // Get full file path & open it
    filePath = dir + names_list[i];
    // Check if item= tiff
    if (endsWith(names_list[i], ".tif")) {
        open(filePath);
        
        //build index array
    	indexes[i]=i;
    }
    

}
Array.show("Files list", indexes, names_list);
//saveAs("Results", dir+"Files_list.csv");
//close("Files_list.csv");

for (i = 0; i < names_list.length; i++) {
	if (endsWith(names_list[i], ".tif")) {
		run("HaralickFilter ", "image="+names_list[i]+" offset=1");
	}
}
close("Log");

//saveAs("Results", dir+"Haralick_Results.csv");
