#!/bin/bash

mkdir ../Data/1D_Out

# Cluster the list by tanimoto score 0.7
cd .. #PHscan directory

echo "Start"
#rm -r ./Data/l_cluster/l_cluster_0.7
#mkdir -p ./Data/l_cluster/l_cluster_0.7
cd ./Data/l_cluster/l_cluster_0.7
echo l_clustering.py
#time python ../../../Tools/l_clustering.py 0.7
#rm -rf ./not_clustered_sdf
echo select_clustered_sdf.py
#time python ../../../Tools/select_clustered_sdf.py 

# Cluster the list by DBSCAN
cd ../../../Tools
#rm Input.save.npy
echo Clustering_Input_ligand.DBSCAN.v3.yg.py
time python Clustering_Input_ligand.DBSCAN.v3.yg.py y 0.6 2 > ../Data/Table/DBSCAN.txt
        
# Generate keys and make Result_1.dat
cd ..
#mkdir ./Data/Table
cp ./Data/l_cluster/l_cluster_0.7/clustered_sdf.txt ./Data/Table/l_cluster_0.7.txt
sed -i '$d' ./Data/Table/l_cluster_0.7.txt
rm ./Data/Table/Result_1.dat
echo Key_gen.v2.yg.py
time python ./Tools/Key_gen.v2.yg.py 5 ./Data/Table/l_cluster_0.7.txt > ./Data/Table/result_detail_0.7.txt
echo '##' >> ./Result_1.dat 
cat ./Tools/l_cluster_DBSCAN.txt > ./Data/Table/l_cluster_DBSCAN.txt
sed -i '$d' ./Data/Table/l_cluster_DBSCAN.txt
echo Key_gen.v2.yg.py
time python ./Tools/Key_gen.v2.yg.py 5 ./Data/Table/l_cluster_DBSCAN.txt > ./Data/Table/result_detail_DBSCAN.txt
mv ./Result_1.dat ./Data/Table/Result_1.dat
