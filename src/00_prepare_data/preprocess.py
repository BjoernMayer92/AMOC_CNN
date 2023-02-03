"This scripts converts the raw data into in situ density"

import xarray as xr
import os
from cdo import Cdo

#!/usr/bin/env python
# coding: utf-8

# # 1 Import Packages

# In[73]:

from prefect.deployments import Deployment
from prefect.deployments import run_deployment
from prefect import get_run_logger

import xarray as xr
import sys, os
from pathlib import Path
import glob
from cdo import Cdo
import matplotlib.pyplot as plt
import numpy as np
import logging

from prefect import Flow, task, flow

cdo = Cdo()


import src.config as config
import src.utils as utils





@task
def gen_filename_list(filename_dict):
    if filename_dict["experiment_family"]=="GrandEnsemble":
        path = os.path.join(config.data_raw_path, filename_dict["experiment_family"], filename_dict["experiment"], filename_dict["realization"])
        logger = get_run_logger()
        logger.info("Reading Files from path: {} ".format(path))
        filename_template = "_".join([filename_dict["realization"],filename_dict["experiment"],"mpiom", "data", "3d", "mm"])+"*.nc"
        logger.info("Searching for files with the template: {} ".format(filename_template))

        filename_list = glob.glob(os.path.join(path, filename_template))
        logger.info("Reading Files from path: {} ".format(filename_list))
        return filename_list

@task
def cal_merge_time(file_list:list, inp_file_dict:dict): 
    out_file, out_file_dict = utils.add_processing_step(inp_file_dict = inp_file_dict, processing_str ="mergetime", init_path = config.data_pro_path, init_filestem = "", filetype ="nc")

    cdo.mergetime(input = " ".join(file_list), output= out_file)
    return out_file, out_file_dict

@task
def cal_density(inp_file, inp_file_dict):

    out_file, out_file_dict = utils.add_processing_step(inp_file_dict, processing_str = "rho", init_path=config.data_pro_path, init_filestem="",filetype="nc")
    
    cdo.setname("rho", input= "-rhopot -adisit {}".format(inp_file), output= out_file)

    return out_file, out_file_dict

@task
def cal_remap(inp_file, inp_file_dict):
    out_file, out_file_dict = utils.add_processing_step(inp_file_dict, processing_str="remap", init_path= config.data_pro_path, init_filestem="", filetype="nc")

    cdo.remapbil("r360x180", input=inp_file, output=out_file)

    return out_file, out_file_dict

@task
def cal_mask_and_crop(inp_file, inp_file_dict, mask_file, lon_min, lon_max, lat_min, lat_max):
    out_file, out_file_dict = utils.add_processing_step(inp_file_dict, processing_str="masked", init_path = config.data_pro_path, init_filestem="", filetype="nc")
    data_lonlatbox_file = cdo.sellonlatbox("{},{},{},{}".format(lon_min, lon_max, lat_min, lat_max),input = inp_file)
    mask_lonlatbox_file = cdo.sellonlatbox("{},{},{},{}".format(lon_min, lon_max, lat_min, lat_max),input = mask_file)
    cdo.mul(input = " ".join([data_lonlatbox_file,mask_lonlatbox_file]), output=out_file)

    return out_file, out_file_dict

@task
def cal_yearly_means(inp_file, inp_file_dict):
    
    out_file, out_file_dict = utils.add_processing_step(inp_file_dict, processing_str = "ym", init_path=config.data_pro_path, init_filestem="",filetype="nc")

    cdo.yearmonmean(input= inp_file, output= out_file)

    return out_file, out_file_dict

@flow
def run_realization(filename_dict, mask_file, lon_min, lon_max, lat_min, lat_max):

    filename_list = gen_filename_list(filename_dict)
    merge_file, merge_dict = cal_merge_time(filename_list, filename_dict)
    merge_rho_file, merge_rho_dict = cal_density(merge_file, merge_dict)
    merge_rho_remap_file, merge_rho_remap_file_dict = cal_remap(merge_rho_file, merge_rho_dict)
    merge_rho_remap_masked_file, merge_rho_remap_masked_file_dict = cal_mask_and_crop(merge_rho_remap_file, merge_rho_remap_file_dict, mask_file = mask_file, lon_min = lon_min, lon_max= lon_max, lat_min=lat_min, lat_max=lat_max)
    merge_rho_remap_masked_ym_file, merge_rho_remap_masked_ym_file_dict = cal_yearly_means(merge_rho_remap_masked_file, merge_rho_remap_masked_file_dict)


@flow 
def run_GrandEnsemble():
    mask_filename = "_".join(["mask", "atlantic", "r360x180"])+".nc"
    mask_file = os.path.join(config.data_pro_path, "basin", "r360x180",mask_filename)

    lat_min = -30
    lat_max = 90

    lon_min=250
    lon_max= 10

    experiment_family = "GrandEnsemble"
    experiment = "hist"

    filename_dict_list = []

    realization_subflows = []
    for i, realization_id in enumerate(np.arange(1,2)):
        realization = "lkm" + str(realization_id).zfill(4)
        

        filename_dict = {}
        filename_dict["experiment_family"] = experiment_family
        filename_dict["experiment"] = experiment
        filename_dict["realization"] = realization

        realization_subflows.append(run_realization(filename_dict, mask_file, lon_min, lon_max, lat_min, lat_max))
        filename_dict_list.append(filename_dict)



def create_deployment():
    mask_filename = "_".join(["mask", "atlantic", "r360x180"])+".nc"
    mask_file = os.path.join(config.data_pro_path, "basin", "r360x180",mask_filename)

    lat_min = -30
    lat_max = 90

    lon_min=250
    lon_max= 10

    experiment_family = "GrandEnsemble"
    experiment = "hist"

    filename_dict_list = []

    for i, realization_id in enumerate(np.arange(1,5)):
        realization = "lkm" + str(realization_id).zfill(4)
        

        filename_dict = {}
        filename_dict["experiment_family"] = experiment_family
        filename_dict["experiment"] = experiment
        filename_dict["realization"] = realization

        filename_dict_list.append(filename_dict)


    for filename_dict in filename_dict_list:
        deployment = Deployment.build_from_flow(
            flow=run_realization,
            name=filename_dict["realization"],
            parameters = {
                "filename_dict" : filename_dict,
                "mask_file" : mask_file,
                "lon_min" : lon_min,
                "lon_max" : lon_max,
                "lat_min" : lat_min,
                "lat_max" : lat_max
            }
        )
        deployment.apply()

create_deployment()

