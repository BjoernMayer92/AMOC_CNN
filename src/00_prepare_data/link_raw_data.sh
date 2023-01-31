#!/bin/bash

mkdir -p /work/uo1075/u301101/Doktorarbeit/CNN/data/raw/GrandEnsemble
cp -rsv /work/uo1075/u301101/Doktorarbeit/Data/GrandEnsemble/hist /work/uo1075/u301101/Doktorarbeit/CNN/data/raw/GrandEnsemble

ln -s /pool/data/MPIOM/GR15/GR15_basin.nc /work/uo1075/u301101/Doktorarbeit/CNN/data/external/
