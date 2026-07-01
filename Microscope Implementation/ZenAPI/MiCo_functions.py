#region imports 

import asyncio
from pathlib import Path
import os
import signal
import time
from typing import Dict, Union
import numpy as np
import random
import pandas as pd

from tkinter import filedialog
from tkinter import *
import shutil

# from typing import List
from zen_api_utils.misc import set_logging, initialize_zenapi
from zen_api_utils.experiment import show_zstack_info_LM, save_experiment, delete_czifile

from zen_api_utils.objective import (
    get_used_objective_positions,
    get_objective_by_position
)

# import the auto-generated python modules
from zen_api.lm.hardware.v2 import (
    ObjectiveChangerServiceStub,
    ObjectiveChangerServiceGetPositionRequest,
    ObjectiveChangerServiceMoveToRequest,
    ObjectiveChangerServiceGetObjectivesRequest
)

# Import custom stage helper functions
from zen_api_utils.stage import (
    get_stageXY_position_simple,
    move_to_stageXY_position_simple,
    StageXYPosition
)

# import the auto-generated python modules
from zen_api.lm.hardware.v2 import (
    StageServiceStub,
    StageServiceGetPositionRequest,
    StageServiceMoveToRequest,
)

# import the auto-generated python modules  #get the sanp
from zen_api.acquisition.v1beta import (
    ExperimentServiceStub,
    ExperimentServiceLoadRequest,
    ExperimentServiceGetImageOutputPathRequest,
    ExperimentServiceRegisterOnStatusChangedRequest,
    ExperimentServiceStartExperimentRequest,
)

from zen_api.acquisition.v1beta import (
    ExperimentServiceStub,
    ExperimentServiceLoadRequest,
    ExperimentServiceGetImageOutputPathRequest,
    ExperimentServiceGetAvailableExperimentsRequest,
    ExperimentServiceCloneRequest,
    ExperimentServiceSaveRequest,
    ExperimentServiceExportRequest,
    ExperimentServiceImportRequest,
    ExperimentServiceDeleteRequest,
    ExperimentServiceRunSnapRequest,
    ExperimentServiceStartLiveRequest,
    ExperimentServiceStopRequest,
    ExperimentServiceStartContinuousRequest,
    ExperimentServiceRunExperimentRequest,
    ExperimentServiceGetStatusRequest,
)

#for Z-stack
from zen_api.lm.acquisition.v1 import (
    ZStackServiceStub,
    ZStackServiceGetZStackInfoRequest,
    ZStackServiceModifyZStackCenterRangeRequest,
    ZStackServiceModifyZStackFirstLastRequest,
)

#SWAF
from zen_api_utils.experiment import show_swaf_info_LM, save_experiment, run_experiment
from grpclib import GRPCError

from zen_api.lm.acquisition.v1 import (
    ExperimentSwAutofocusServiceStub,
    ExperimentSwAutofocusServiceGetAutofocusParametersRequest,
    ExperimentSwAutofocusServiceSetAutofocusParametersRequest,
    ExperimentSwAutofocusServiceFindAutoFocusRequest,
    AutofocusMode,
    AutofocusContrastMeasure,
    AutofocusSampling,
)

# import the auto-generated python modules
from zen_api.lm.hardware.v2 import (
    StageServiceGetPositionRequest,
    FocusServiceMoveToRequest,
    FocusServiceStub,
)

#endregion

logger = set_logging()

#region define functions
async def stage_move(stage_service, focus_service, new_x, new_y, new_z):
    '''
    Moves the stage around maintaining the set objective

    Args: 
        stage_service: microscope's stage service
        stage_service: microscope's focus service
        new_x, new_y, new_z: x, y & z coordinates in µm of the position the 
        microscope will move to in m
    
    Returns:
        new_posXY.x: x stage position of the stage in m (I don't think this is necessary)
        new_posXY.y: y stage position of the stage in m(I don't think this is necessary)
        new_posZ.value: z stage position of the stage in m(I don't think this is necessary)
    '''
    
    # Move to new position
    await stage_service.move_to(StageServiceMoveToRequest(x=new_x, y=new_y))
    await focus_service.move_to(FocusServiceMoveToRequest(value=new_z))
    #extract position
    new_posXY = await stage_service.get_position(StageServiceGetPositionRequest())
    new_posZ = await focus_service.get_position(StageServiceGetPositionRequest())
    return new_posXY.x, new_posXY.y, new_posZ.value


async def change_FOV(stage_service, focus_service, objective_service, new_x, new_y, new_z, new_zoom_pos):
    '''
    Zooms to the determined objective while moving the stage to the x,y,z position specified
    (where the event was identified).

    Args:
        stage_service, focus_service, objective_service: microscope's stage and objective changer services
        new_x, new_y, new_z: x, y & z coordinates in m of the position the microscope stage
        will move to
        new_zoom_pos: the desired objective position index 

    Returns:
        new_posX: x stage position of the stage in m (I don't think this is necessary)
        new_posY: y stage position of the stage in m(I don't think this is necessary)
        new_posZ.value: z stage position of the stage in m(I don't think this is necessary)
    '''
    #change objective
    out = await objective_service.move_to(ObjectiveChangerServiceMoveToRequest(position_index=new_zoom_pos))

    # move to new position using previous function
    new_posX, new_posY, new_posZ = await stage_move(stage_service, focus_service, new_x, new_y, new_z)

    return new_posX, new_posY , new_posZ


async def take_snap(experiment_service, experiment_setup, save_path, destination_path, results_dict, pos_index, zoomed):
    '''
    Takes a snap experiment image of the current view of the microscope

    Args:
        experiment_service: microscope's experiment services
        experiment_setup: loaded experiment 
        save_path: default path where Zen saves images
        destination_path: path where the snap will be stored in
        results_dict: dictionary where the snaps and their paths are all stored together
        pos_index: position index of the area being snapped
        zoomed: boolean representing whether the current snap is zoomed in or an overview snap

    Returns:
        # dictionary_key: dictionary key to identify the path (but not rly needed)

    '''
    # wait until snap is finished
    snap = await experiment_service.run_snap(ExperimentServiceRunSnapRequest(experiment_id=experiment_setup.experiment_id))
    #append it to the list of experiments
    if zoomed:
        dict_key = f"zoomed_snap_path_{pos_index}"
        out_name = f"Pos{pos_index}_Zoomed_Snap"
    else:
        dict_key = f"snap_path_{pos_index}"
        out_name = f"Pos{pos_index}_Snap"
        

    shutil.move(str(Path(save_path.image_output_path) / (snap.output_name + ".czi")), f"{destination_path}/{out_name}.czi")

    results_dict[dict_key] = Path(destination_path) / (out_name + ".czi")
    #         return dict_key #TODO see if needed


async def take_timelapse(experiment_service, zoomed_experiment_setup, save_path, destination_path, results_dict, pos_index, zoomed):
    '''
    Starts an experiment with the current view of the microscope & stores it 
    as TL-Exp name

    Args:
        experiment_service: microscope's experiment services
        experiment_setup: loaded experiment for timelapse moment
        save_path: default path where Zen saves images
        destination_path: path where the snap will be stored in
        results_dict: dictionary where the snaps and their paths are all stored together
        pos_index: position index of the area being snapped
        zoomed: boolean representing whether the current snap is zoomed in or an overview snap

    Returns:
        results_dict[dict_key]: path of where the image file has been stored

    '''
    # execute experiment
    logger.info("Starting Experiment Execution ...")
    if zoomed:
        dict_key = f"zoomed_tl-exp_path_{pos_index}"
        out_name = f"Pos{pos_index}_Zoomed_TL-Exp"
    else:
        dict_key = f"tl-exp_path_{pos_index}"
        out_name = f"Pos{pos_index}_TL-Exp"
        

    exp_result = await experiment_service.run_experiment(
        ExperimentServiceRunExperimentRequest(experiment_id=zoomed_experiment_setup.experiment_id, output_name=out_name)
    )

    exp_status = await experiment_service.get_status(ExperimentServiceGetStatusRequest(experiment_id=zoomed_experiment_setup.experiment_id))

    logger.info(exp_status)

    shutil.move(str(Path(save_path.image_output_path) / (exp_result.output_name + ".czi")), f"{destination_path}/{out_name}.czi")

    results_dict[dict_key] = Path(destination_path) / (out_name + ".czi")

    return results_dict[dict_key]    # returns the path of the image file


async def take_zstack_exp(experiment_service, zstack_service, experiment_setup, centre_z, save_path, destination_path, results_dict, pos_index, zoomed, zstack_interval=2*1e-6, zstack_range=8*1e-6, show_info=False):
    '''
    Starts a Zstack experiment centered around specified z slice with the current view of the 
    microscope & stores it as Z-Exp name

    Args:
        experiment_service, zstack_service: microscope's experiment and zstack services
        experiment_setup: loaded z-stack experiment settings file
        centre_z: centre of the z-stack in m
        save_path: default path where Zen saves images
        destination_path: path where the snap will be stored in
        results_dict: dictionary where the snaps and their paths are all stored together
        pos_index: position index of the area being snapped
        zoomed: boolean representing whether the current snap is zoomed in or an overview snap

        Optional:
        zstack_interval: interval between zslices in m
        zstack_range: range covered by zstack in m
        show_info: shows Z-stack information

    Returns:
        results_dict[dict_key]: path of where the image file has been stored

    '''

    
    if zoomed:
        dict_key = f"zoomed_Z-exp_path_{pos_index}"
        out_name = f"Pos{pos_index}_Zoomed_Z-Exp"
    else:
        dict_key = f"Z-exp_path_{pos_index}"
        out_name = f"Pos{pos_index}_Z-Exp"


    # modify the z-stack to have centre at autofocus position with a range of 9
    await zstack_service.modify_z_stack_center_range(
        ZStackServiceModifyZStackCenterRangeRequest(
            experiment_id = experiment_setup.experiment_id,
            center = centre_z,
            interval = zstack_interval,
            range = zstack_range,
        )
    )
    
    # delete already existing CZI files with same name in temp storage to prevent isues
    delete_czifile(Path(save_path.image_output_path), out_name)

    if show_info:
        # get the information about the mdoified stack
        zstack_info = await zstack_service.get_z_stack_info(
            ZStackServiceGetZStackInfoRequest(experiment_id=experiment_setup.experiment_id)
        )

        # show z-stack info
        show_zstack_info_LM(zstack_info)

    # execute experiment
    logger.info("Starting Experiment Execution ...")

    #run the modified zstack experiment
    exp_result = await experiment_service.run_experiment(
        ExperimentServiceRunExperimentRequest(experiment_id=experiment_setup.experiment_id, output_name=out_name)
    )

    exp_status = await experiment_service.get_status(ExperimentServiceGetStatusRequest(experiment_id=experiment_setup.experiment_id))

    logger.info(exp_status)

    #move the file from the default save path to our experiment's directory
    shutil.move(str(Path(save_path.image_output_path) / (exp_result.output_name + ".czi")), f"{destination_path}/{out_name}.czi")

    results_dict[dict_key] = Path(destination_path) / (out_name + ".czi")

    return results_dict[dict_key]    # returns the path of the image file


async def autofocus(swaf_service, focus_service, experiment_setup, zoomed, overview_focus=0, ref_channel="FITC", show_info=False):
    '''
    Runs software autofocus on current stage position

    Args:
        swaf_service: microscope's software autofocus services
        focus_service: microscope's software stage focus services
        experiment_setup: experiment to be ran 
        zoomed: boolean representing whether the current experiment is zoomed in or an overview

    Returns:
        new_focus_position or posZ.value = final stage z position in m

    '''
    # modify the SWAF's search range depending on whether its a zoomed in position (requires more range and time), 
    # or if it's an overview image where we already have an estimate of the focus position




    if zoomed:
        await swaf_service.set_autofocus_parameters(
            ExperimentSwAutofocusServiceSetAutofocusParametersRequest(
                experiment_id=experiment_setup.experiment_id,   # we are changing the zoomed experiment's settings here
                autofocus_mode=AutofocusMode.AUTO,
                search_strategy="Smart",
                autofocus_sampling=AutofocusSampling.MEDIUM,
                # offset=0.5 * 1e-6,  # in [m]
                use_acquisition_roi=True,  # Full frame will be used and not the Focus Region
                reference_channel_name=ref_channel,
                # relative_range_is_automatic=False, # if false it is still "relative" but one needs tp provide a search range
                relative_search_range=123 * 1e-6,  # --> cannot be used when range is auto
                # lower_limit=-50 * 1e-6,  # --> cannot be used when range is auto
                # upper_limit=50 * 1e-6,  # --> cannot be used when range is auto
            )
        )
      # run stored SWAF
    try:
        swaf_response = await swaf_service.find_auto_focus(
            ExperimentSwAutofocusServiceFindAutoFocusRequest(
                experiment_id=experiment_setup.experiment_id, timeout=60  # in [s]
            )
        )
        new_focus_position = swaf_response.focus_position

        if show_info:
            # get the information about the SWAF parameters
            swaf_info = await swaf_service.get_autofocus_parameters(
                ExperimentSwAutofocusServiceGetAutofocusParametersRequest(experiment_id=experiment_setup.experiment_id)
            )
            # show the SWAF parameters
            show_swaf_info_LM(swaf_info)

        logger.info(f"Z-Drive Position after SWAF: {new_focus_position:.3f}")
        return new_focus_position*1e-6

    except GRPCError as e:
        logger.error(e.message)
        posZ_1 = await focus_service.get_position(StageServiceGetPositionRequest())

        if show_info:
            # get the information about the SWAF parameters
            swaf_info = await swaf_service.get_autofocus_parameters(
                ExperimentSwAutofocusServiceGetAutofocusParametersRequest(experiment_id=experiment_setup.experiment_id)
            )
            # show the SWAF parameters
            show_swaf_info_LM(swaf_info)

        logger.info(f"Z-Drive Position after SWAF error: {posZ_1.value*1e6:.3f}")
        return posZ_1.value



#endregion