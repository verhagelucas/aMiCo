
#@ int final_size;	// size

dir = getDirectory("Choose a Directory ");
fileslist = getFileList(dir);

print(dir);

setBatchMode(true);
for (i = 0; i < fileslist.length; i++) {
	if (endsWith(fileslist[i], ".tif")){
		open(dir + fileslist[i]);	//open file
		run("Canvas Size...", "width=512 height=512 position=Center zero"); //resize and centre ROI
		//run("Canvas Size...", "width="+ final_size +" height="+ final_size +" position=Center zero");
		selectImage(fileslist[i]);
		run("Save");
		close();
	}
}
setBatchMode(false);
print("Done!")

