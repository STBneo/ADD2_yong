#!/bin/bash

#set -euxo pipefail

# Convert sdf to pdb files
cd ..
cd ./Data/Dic_Lib_Output_PDB
rm -rf $1
echo sdf2pdb.m.py
time python ../../Tools/sdf2pdb.m.py $1
cd ..
