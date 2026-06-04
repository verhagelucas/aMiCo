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

from zen_api.lm.acquisition.v1 import (
    ZStackServiceStub,
    ZStackServiceGetZStackInfoRequest,
    ZStackServiceModifyZStackCenterRangeRequest,
    ZStackServiceModifyZStackFirstLastRequest,
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
    FocusServiceStub,
)

#endregion

logger = set_logging()

#region define functions
async def stage_over_scan(stage_service, new_x, new_y):
    '''
    Moves the stage around maintaining the set objective

    Args: 
        stage_service: microscope's stage service
        new_x, new_y: x & y coordinates of the position the microscope 
        will move to
    
    Returns:
        new_posXY: stage position with .x and .y being the new position 
        of the stage (I don't think this is necessary)
    '''
    # Move to new position
    await stage_service.move_to(StageServiceMoveToRequest(x=new_x, y=new_y))
    #extract position
    new_posXY = await stage_service.get_position(StageServiceGetPositionRequest())
    return new_posXY


async def event_identified(stage_service, objective_service, new_x, new_y, new_zoom_pos):
    '''
    Zooms to the determined objective while moving the stage to the x,y position 
    where the event was identified.

    Args:
        stage_service, objective_service: microscope's stage and objectivechanger services
        new_x, new_y: x & y coordinates of the event detected where the microscope stage
        will move to
        new_zoom_pos: the desired objective position index 

    Returns:
        new_posXY: stage position with .x and .y being the new position 
        of the stage (I don't think this is necessary)

    '''
    #change obj
    out = await objective_service.move_to(ObjectiveChangerServiceMoveToRequest(position_index=new_zoom_pos))
    # move to new pos
    # extract position
    new_posXY = await stage_over_scan(stage_service, new_x, new_y)
    return new_posXY


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


async def take_zstack(zstack_service, experiment_service, experiment_setup, center_z, save_path, destination_path, results_dict, pos_index, zoomed):
    '''
    Starts an experiment with the current view of the microscope & stores it 
    as Z-Exp name

    Args:
        zstack_Service: microscope's zstack services
        experiment_service: microscope's experiment services
        experiment_setup: loaded experiment for z-stack moment
        center_z: center of the zstack in μm
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
        dict_key = f"zoomed_Z-exp_path_{pos_index}"
        out_name = f"Pos{pos_index}_Zoomed_Z-Exp"
    else:
        dict_key = f"Z-exp_path_{pos_index}"
        out_name = f"Pos{pos_index}_Z-Exp"
        
    # modify the z-stack to have center at autofocus position with a range of 9
    await zstack_service.modify_z_stack_center_range(
        ZStackServiceModifyZStackCenterRangeRequest(
            experiment_id=experiment_setup.experiment_id,
            center=center_z,
            interval=1 * 1e-6,
            range=9 * 1e-6,
        )
    )

    exp_result = await experiment_service.run_experiment(
        ExperimentServiceRunExperimentRequest(experiment_id=experiment_setup.experiment_id, output_name=out_name)
    )

    exp_status = await experiment_service.get_status(ExperimentServiceGetStatusRequest(experiment_id=experiment_setup.experiment_id))

    logger.info(exp_status)

    shutil.move(str(Path(save_path.image_output_path) / (exp_result.output_name + ".czi")), f"{destination_path}/{out_name}.czi")

    results_dict[dict_key] = Path(destination_path) / (out_name + ".czi")

    return results_dict[dict_key]    # returns the path of the image file


async def autofocus(swaf_service, focus_service, current_exp):
    '''
    Runs software autofocus on current stage position

    Args:
        swaf_service: microscope's software autofocus services
        focus_service: microscope's software stage focus services
        exp_setup: loaded experiment 

    Returns:
        new_focus_position, posZ.value*1e6 = final stage z position in μm

    '''
      # run stored SWAF
    try:
        swaf_response = await swaf_service.find_auto_focus(
            ExperimentSwAutofocusServiceFindAutoFocusRequest(
                experiment_id=current_exp.experiment_id, timeout=60  # in [s]
            )
        )
        new_focus_position = swaf_response.focus_position
        logger.info(f"Z-Drive Position after SWAF: {new_focus_position:.3f}")
        return new_focus_position

    except GRPCError as e:
        logger.error(e.message)
        posZ_1 = await focus_service.get_position(StageServiceGetPositionRequest())
        logger.info(f"Z-Drive Position after SWAF error: {posZ_1.value*1e6:.3f}")
        return posZ_1.value*1e6

#endregion