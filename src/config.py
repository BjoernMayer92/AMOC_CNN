"""
This is a configuration file for the project, that saves important global variables
"""

from pathlib import Path
import os




# Paths
proj_path = os.path.abspath(Path(__file__).parents[1].resolve())

data_path = os.path.join(proj_path, "data")

data_raw_path = os.path.join(data_path, "raw")
data_pro_path = os.path.join(data_path, "processed")
data_res_path = os.path.join(data_path, "results")
data_ext_path = os.path.join(data_path, "external")

src_path = os.path.join(proj_path, "src")

model_path = os.path.join(proj_path, "models")


# Basin File
basin_file = os.path.join(data_ext_path, "GR15_basin.nc")

if __name__=="__main__":
    print(proj_path)