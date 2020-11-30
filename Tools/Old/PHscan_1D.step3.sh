#!/bin/bash

#set -euxo pipefail

# Make chembl_list.?R.txt
cd ..
rm -r ./Data/l_cluster/l_cluster_0.9_$1
mkdir -p ./Data/l_cluster/l_cluster_0.9

cd ./Data/l_cluster/l_cluster_0.9
echo make_chembl_list0.9.py
python ../../../Tools/make_chembl_list0.9.py $1
cat chembl_list.$1.txt | sort | uniq > chembl_list.$1.uniq.txt

# Cluster the list by tanimoto score 0.9
echo l_clustering.py 0.9
time python ../../../Tools/l_clustering.py 0.9 $1

cd ../../..
mv ./Data/l_cluster/l_cluster_0.9 ./Data/l_cluster/l_cluster_0.9_$1
