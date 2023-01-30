"""
This is a configuration file for the project, that saves important global variables
"""

from pathlib import Path
import os




# Paths
proj_path = os.path.abspath(Path(__file__).parent.resolve())

data_path = os.path.join(proj_path, "data")

data_raw_path = os.path.join(data_path, "raw")
data_pro_path = os.path.join(data_path, "processed")
data_res_path = os.path.join(data_path, "results")

src_path = os.path.join(proj_path, "src")



