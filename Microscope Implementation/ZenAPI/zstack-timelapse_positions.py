# -*- coding: utf-8 -*-

#################################################################
# File        : zenapi_objectivechanger.py
# Author      : SRh
# Institution : Carl Zeiss Microscopy GmbH
#
#
# Copyright(c) 2025 Carl Zeiss AG, Germany. All Rights Reserved.
#
# Permission is granted to use, modify and distribute this code,
# as long as this copyright notice remains part of the code.
#################################################################

from functions_mic_control import *
from functions_imageJ_interact import *


# Get the directory where the current script is located
script_dir = Path(__file__).parent

# Build the path to config.ini relative to the script
config_path = script_dir / "config.ini"

print_info = False
overview_obj = 1
zoomed_obj = 3

#experiment_choice= "Zen_API_Test"
experiment_choice= "Zen_API_Test_Z-stack"
zoomed_exp_choice = "Zen_API_Test_Timelapse"

#select where to store your experiment

root = Tk()
root.withdraw()
selected_folder = filedialog.askdirectory(title="Select folder to store your experiment")

experiment_name = input("Experiment Name:") #TODO: make it so cant insert stuff that will break folder naming
experiment_folder = f"{selected_folder}/{experiment_name}"
os.mkdir(experiment_folder)
timepoints = int(input("Timepoints:"))
#TODO: add a minimum set time between the timepoints where if the scans are done before it they wait

# select positions in zen software >> File >> Tiles >> Export Tile Experiment >>
# >> Save in folder where you'll save your experiment as a .CSV file named "positions"
points = pd.read_csv(f"{selected_folder}/positions.csv",usecols=["X","Y"])
pos_list = points.values.tolist()

#Initialise the JVM environment
os.environ["JAVA_HOME"] =r"C:\Users\Zen-user\.conda\envs\newAPI_env\Library\jre"
# initialise Fiji
ij = imagej.init(r"C:\Fiji", mode = "interactive")



#TODO: consider turning the location results dict into a time dict that tells you when the images were taken
async def check_experiment_api(experiment_name_overview: str, experiment_name_zoomed: str, configfile: str = "config.ini") -> Dict[str, Union[str, Path]]:

    results = {}
    time_array = {}
    timepoint_loops =[]
    overview_times = []
    zoom_times=[]
    analysis_times=[]

    # get the gRPC channel and the metadata
    channel, metadata = initialize_zenapi(configfile)

    #region get microscope services
    # get objective services
    objchanger_service = ObjectiveChangerServiceStub(channel=channel, metadata=metadata)
    # get stage service
    simple_stage_service = StageServiceStub(channel=channel, metadata=metadata)
    # get the experiment service
    exp_service = ExperimentServiceStub(channel=channel, metadata=metadata)
    # get SWAF_service
    swaf_service = ExperimentSwAutofocusServiceStub(channel=channel, metadata=metadata)
    # get focus stage service
    focus_service = FocusServiceStub(channel=channel, metadata=metadata)
    #endregion

    # show output path for images
    save_path = await exp_service.get_image_output_path(ExperimentServiceGetImageOutputPathRequest())
    logger.info("Default saving Location for CZI Images:" + save_path.image_output_path)

    # load experiments by their names without the *.czexp extension
    exp_setup_overview = await exp_service.load(ExperimentServiceLoadRequest(experiment_name=experiment_name_overview))
    logger.info("ExperimentName:" + experiment_name_overview + " Reference Id: " + exp_setup_overview.experiment_id)
    exp_setup_zoomed = await exp_service.load(ExperimentServiceLoadRequest(experiment_name=experiment_name_zoomed))
    logger.info("ExperimentName:" + experiment_name_zoomed + " Reference Id: " + exp_setup_zoomed.experiment_id)


    #load available objectives
    objectives = await objchanger_service.get_objectives(ObjectiveChangerServiceGetObjectivesRequest())


    #region extract available info
    if print_info:
        

        logger.info("----------------------- Available Objectives  -----------------------")

        # check used positions
        used_obj_positions = get_used_objective_positions(objectives)
        logger.info(f"Used objective positions: {used_obj_positions}")

        for obj in objectives.objectives:
            logger.info(f"Objective: {obj.name} - Position: {obj.position}")

        
        #### GET CURRENT INFO

        # get the current objective position and name
        pos_obj = await objchanger_service.get_position(ObjectiveChangerServiceGetPositionRequest())
        current_objective = get_objective_by_position(objectives, pos_obj.value)
        logger.info(f"Current Objective: {current_objective.name} Position: {current_objective.position}")
        obj_initial_position = current_objective.position

        # get the initial stage positions in [m]
        init_posXY = await simple_stage_service.get_position(StageServiceGetPositionRequest())
        logger.info(f"Stage XY Position initial: {np.round(init_posXY.x * 1e6, 2)} - {np.round(init_posXY.y * 1e6, 2)} [micron]")

        #  get Z-Position
        posZ_1 = await focus_service.get_position(StageServiceGetPositionRequest())
        logger.info(f"Z-Drive Position before SWAF [micron]: {posZ_1.value*1e6:.3f}")

    #endregion

    logger.info("----------------------- Begining Time and Position loop -----------------------\n\n")
    
    t=0
    while t < timepoints:   #loop over set timepoints
        

        logger.info(f"-------------------------------- Time point: {t+1} -----------------------------------\n")
        time_folder = f"{experiment_folder}/timepoint_{t+1}"
        os.mkdir(time_folder)   #create folder pertimepoint in which to store images

        for i,pos in enumerate(pos_list):
            tic_pos = time.time()
            logger.info(f"--------------------------- Position: {i} ------------------------------")
            current_x, current_y = pos[0]*1e-6, pos[1]*1e-6

            await stage_over_scan(simple_stage_service, current_x, current_y) #move to current "tile"
            logger.info(f"Stage XY Position: {np.round(current_x * 1e6, 2)} - {np.round(current_y * 1e6, 2)} [micron]\n")

            #autofocus
            # await autofocus(swaf_service, focus_service, exp_setup_overview)  #TODO change to only focus if needed

            #take image
            logger.info("Start Overview Experiment ...")
            exp_path = await take_zstack(exp_service, exp_setup_overview, save_path, time_folder, results, i, zoomed=False)
            logger.info("... Finished Overview Experiment\n")

            tic_analysis = time.time()
            #2) analyse the z_stack
            fiji_segmentation(str(exp_path), str(time_folder), ij)
            # im_width, im_height = fiji_segmentation(exp_path, time_folder, ij)
            im_width, im_height = 5683.2, 3196.8    ## TODO: try and make the new package work with     
            '''im_width, im_height = float(im_size.getOutput("image_width")), float(im_size.getOutput("image_height"))
                                                    ^^^^^^^^^^^^^^^^^
                AttributeError: 'java.util.HashMap' object has no attribute 'getOutput'''

            #3) analyse the results to get cell of interest
            dx, dy = find_largest_centre_dims(exp_path, im_width, im_height)

            analysis_times.append(time.time()-tic_analysis)
            toc_overview = time.time()
            overview_times.append(toc_overview-tic_pos)

            if dx or dy:   #if a dx or dy exist
                logger.info("--Event Identified--\n")

                # determine event position in [m]
                new_posx, new_posy = current_x + dx* 1e-6, current_y + dy* 1e-6

                #zoom into event
                await event_identified(simple_stage_service, objchanger_service, new_posx, new_posy, zoomed_obj)  

                await autofocus(swaf_service, focus_service, exp_setup_zoomed)

                logger.info("Start Timelapse Experiment ...")
                await take_timelapse(exp_service, exp_setup_zoomed, save_path, time_folder, results, i, zoomed=True)
                logger.info("... Finished Timelapse Experiment\n")

                await event_identified(simple_stage_service, objchanger_service, current_x, current_y, overview_obj)  # zoom out to overview
                #TODO MAYBE reduce pos index s.t. the same position gets checked again in case someother cell has started mitosing
                zoom_times.append(time.time()-toc_overview)  

            timepoint_loops.append(time.time()-tic_pos)
        t += 1

    
    
    logger.info("\n\nFinished acquisition\n\n")    

    # close the channel
    channel.close()
    
    time_array["overall_timepoint"] = timepoint_loops    
    time_array["overview_timepoint"] = overview_times    
    time_array["zoomed_timepoints"] = zoom_times 
    time_array["analysis_timepoints"] = analysis_times   


    return results, time_array


if __name__ == "__main__":
    tic_top = time.time()
    # create logger
    logger = set_logging()

    # run the main function
    results, time_array = asyncio.run(check_experiment_api(experiment_name_overview=experiment_choice,experiment_name_zoomed=zoomed_exp_choice, configfile=config_path))

    print(results)
    print(time_array)

    print("avg overview image: ", np.mean(time_array['overview_timepoint']))
    print("avg zoomed images: ", np.mean(time_array['zoomed_timepoints']))
    print("avg image analysis: ", np.mean(time_array['analysis_timepoints']))

    print('total time ', time.time()-tic_top)
    os.kill(os.getpid(), signal.SIGINT) #Makes sure script ends and exits fiji at the end

