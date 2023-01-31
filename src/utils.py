from typing import Union
import os

def gen_relative_path_and_filestem(processing_dict: dict) -> Union[str,str]:
    """This function creates a relative path and filestem given a specific dictionary for the variable.

    Args:
        processing_dict (dict): Dictionary containing the processing information

    Returns:
        Union[str,str]: path and filestem for the file.
    """
    path = "" 
    for i, key in enumerate(processing_dict):
        value = processing_dict[key]
        path = os.path.join(path, value)
        filestem= value if i==0  else "_".join([filestem,value])

    return path, filestem



def gen_absolute_path_and_filename(filename_dict: dict, init_path:str, init_filestem:str, filetype: str="nc") -> Union[str,str]:
    """This function creates an absolute path and filename given a processing dictionary for the variable, the initial path and the initial filestem 
    as well as an filetype"

    Args:
        filename_dict (dict): Dictionary containing the processing information.
        init_path (str): Initial path of the file.
        init_filestem (str): Initial filestem of the file. 
        filetype (str, optional): _description_. Defaults to "nc".

    Returns:
        Union[str,str]: absolute path and filename
    """
    relative_path, relative_filestem = gen_relative_path_and_filestem(filename_dict)

    absolute_path = os.path.join(init_path, relative_path)
    
    if init_filestem=="":
        absolute_filestem = relative_filestem
    else:
        absolute_filestem = "_".join([init_filestem,relative_filestem])
    
    absolute_filename = ".".join([absolute_filestem, filetype]) 

    
    return absolute_path, absolute_filename


def add_processing_step(inp_file_dict: dict, processing_str: str, init_path: str, init_filestem: str, filetype:str) ->Union[str,dict]:
    """This functions adds a processing step to the file dictionary creates the new output path for the file and returns the filename and path for the output file

    Args:
        inp_file_dict (dict): Input file dictionary. 
        processing_str (str): String that describes the processing step and is appended to the already existing processing string
        init_path (str): String of the init path that is added to the relative path created from the inp_file_dict
        init_filestem (str): String of the filestem that is prepended to the relative filesteam created from the inp_file_dict
        filetype (str): String describing the filetype

    Returns:
        Union[str,dict]: output file and dictionary
    """

    
    out_file_dict = inp_file_dict.copy()
    if "processing" not in inp_file_dict.keys():
        out_file_dict["processing"] = processing_str
    else:
        out_file_dict["processing"] = "_".join([out_file_dict["processing"], processing_str])

    path, filename = gen_absolute_path_and_filename(out_file_dict, init_path = init_path, init_filestem = init_filestem, filetype=filetype)
    os.makedirs(path, exist_ok=True)
    out_file = os.path.join(path, filename)

    return out_file, out_file_dict