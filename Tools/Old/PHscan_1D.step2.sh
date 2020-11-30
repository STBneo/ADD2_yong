#!/bin/bash

#set -euxo pipefail

# Make chembl_list.?R.txt
cd ..
rm -r ./Data/l_cluster/l_cluster_0.9_$1
mkdir -p ./Data/l_cluster/l_cluster_0.9

cd ./Data/l_cluster/l_cluster_0.9
python ../../../Tools/make_zinc_list_0.9.py $1
cat zid_list_$1.txt | sort | uniq > zid_list_$1_uniq.txt

# Cluster the list by tanimoto score 0.9
python ../../../Tools/l_clustering.py 0.9 $1

cd ../../..
mv ./Data/l_cluster/l_cluster_0.9 ./Data/l_cluster/l_cluster_0.9_$1

# Convert sdf to pdb file
cd ./Data/Dic_Lib_Output_PDB
rm -rf $1
python ../../Tools/sdf2pdb.m.py $1
cd ..
