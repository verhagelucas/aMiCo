macro "Extract Measurements"{
    title_OG = getTitle();
    dir_save = getDirectory("image");  //Get directory where Results.csv will be saved


    //MEASURE & EXTRACT MEASUREMENTS AS .csv FILE
    selectImage(title_OG);
    // set what will get measured
    run("Set Measurements...", "standard center perimeter bounding kurtosis stack display redirect=None decimal=3");	
    roiManager("Deselect"); // make sure no individiual ROI is selected so all ROIs get measured
    roiManager("Measure");
    saveAs("Results", dir_save + "Results.csv");

    //clean up
    close("Results");
}