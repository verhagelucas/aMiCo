import imagej
from pathlib import Path
import pandas as pd
from ij_macros import macro_process_image, macro_candidate_segmentation, macro_reset_ij
# import os

# os.environ["JAVA_HOME"] =r"C:\Users\Zen-user\.conda\envs\newAPI_env\Library\jre"
# # initialise Fiji
# ij = imagej.init(r"C:\Fiji", mode = "interactive")

def fiji_segmentation_get_outputs(image_path, save_directory, ij_instance):
    '''
    Isolates one channel of the image taken and performs a maxZprojection, 
    this is stored in save_directory as "process.tif".
    It then segments it, and measures the values for the selected ROIs. 
    These measurements and ROIs are stored into save_directory as a 
    "Results.csv" file, and "RoiSet.zip" file respectively.

    Args:
        image_path: path to image being analysed
        save_directory: directory in which the measurements and ROIs will be 
        stored in.
        ij_instance: instance of imagej initiated locally

    Returns:
        im_width: Image width [in μm]
        im_height: Image height [in μm]

    '''
    dataset = ij_instance.io().open(image_path)  # Open the Zstack
    ij_instance.ui().show(dataset)

    args = {
        'path': save_directory,
        'ignore_edges': False,
        'min_sel_size': 0,
    }

    # Process the image to get only 1 channel
    #   Args used: path
    im_size = ij_instance.py.run_macro(macro_process_image, dict(list(args.items())[:1]) )
    im_width, im_height = float(im_size.getOutput("image_width")), float(im_size.getOutput("image_height"))

    # Perform segmentation & save ROIs & measurements
    #   Args used: path, ignore_edges, min_sel_size
    ij_instance.py.run_macro(macro_candidate_segmentation, args)

    # Reset ij_instance roi manager st. it is empty for next image to analyse
    #   Args used: none
    ij_instance.py.run_macro(macro_reset_ij) 

    return im_width, im_height


def fiji_segmentation(image_path, save_directory, ij_instance):
    '''
    Isolates one channel of the image taken and performs a maxZprojection, 
    this is stored in save_directory as "process.tif".
    It then segments it, and measures the values for the selected ROIs. 
    These measurements and ROIs are stored into save_directory as a 
    "Results.csv" file, and "RoiSet.zip" file respectively.

    Args:
        image_path: path to image being analysed [str]
        save_directory: directory in which the measurements and ROIs will be 
        stored in.  [str]
        ij_instance: instance of imagej initiated locally

    Returns:

    '''
    dataset = ij_instance.io().open(image_path)  # Open the Zstack
    ij_instance.ui().show(dataset)

    args = {
        'path': save_directory,
        'ignore_edges': False,
        'min_sel_size': 0,
    }

    # Process the image to get only 1 channel
    #   Args used: path
    ij_instance.py.run_macro(macro_process_image, dict(list(args.items())[:1]) )

    # Perform segmentation & save ROIs & measurements
    #   Args used: path, ignore_edges, min_sel_size
    ij_instance.py.run_macro(macro_candidate_segmentation, args)

    # Reset ij_instance roi manager st. it is empty for next image to analyse
    #   Args used: none
    ij_instance.py.run_macro(macro_reset_ij) 


def find_largest_centre(image_file, im_width, im_height):
    '''
    From the 'Results.csv' file produced by fiji_interact identifies the object with
    the largest perimeter and uses its Centre of Mass (CoM) coordinates to calculate
    the distance between the centre of the image and the largest identified object. 

    Args:
        image_file: path to image being analysed
        im_width: Width of image being analysed [in μm]
        im_height: Height of image being analysed [in μm]

    Returns:
        dx: x distance between current image centre and the centre of the identified 
            object with the largest perimeter [in μm]
        dy: y distance between current image centre and the centre of the identified 
            object with the largest perimeter [in μm]

    '''
    path = Path(image_file)
    directory = path.parent
    #Extract the data from the measurements
    data = pd.read_csv(directory / Path("Results.csv"),     
                    usecols=["XM", "YM", "Perim."])

    max_perim = data.loc[data["Perim."].idxmax()]   #Find the ROI with max perimeter
    com_x, com_y = max_perim["XM"], max_perim["YM"] # Extract coordinates of its CoM
    print(f"CoMx = {com_x}, CoMy = {com_y}")

    dx, dy = (com_x - im_width/2), (com_y - im_height/2)  # Calculate how much stage should move from current pos

    return dx, dy

