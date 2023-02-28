import os
import papermill as pm
import numpy as np
import datetime

kfold_index_list = np.arange(0,6+1)
lev_index_list = [0,23]

datetime_string = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
out_dir = "./linear_models/{}".format(datetime_string)

if not os.path.exists(out_dir):
    os.makedirs(out_dir)
    
jupyter_filestem = "linear_model"
for lev_index in lev_index_list:
    for kfold_index in kfold_index_list:
        inp_filename = jupyter_filestem+".ipynb"
        out_filename = "_".join([jupyter_filestem,"lev", str(lev_index), "kfold", str(kfold_index)])+".ipynb"

        pm.execute_notebook(inp_filename, os.path.join(out_dir, out_filename), parameters = {"lev_index": str(lev_index), "kfold_index":str(kfold_index), "datetime_string":datetime_string})
        
