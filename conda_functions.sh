#!/bin/bash

source activate CNN

if [ $1 = "export" ]
then
    conda env export > environment.yml
elif [ $1 = "install_kernel" ] 
then
    python -m ipykernel install --user --name CNN
fi

