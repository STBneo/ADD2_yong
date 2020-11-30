#!/bin/bash

# Clustering by tanimoto score 0.7
echo 'Clustering by tanimoto score 0.7'
cd ..
rm -r ./Data/l_cluster/l_cluster_0.7
mkdir -p ./Data/l_cluster/l_cluster_0.7
cd ./Data/l_cluster/l_cluster_0.7
python ../../../Tools/l_clustering.v3.py 0.7
rm -rf ./not_clustered_sdf
python ../../../Tools/select_clustered_sdf.v2.py 

# Clustering by DBSCAN
echo 'Clustering by DBSCAN'
cd ../../../Tools
rm Input.save.npy
python Clustering_Input_ligand.DBSCAN.v3.yg.py y 0.6 2 > ../Data/Table/DBSCAN.txt
        
# Generate keys and make Result_1.dat
echo 'Generate keys and make Result_1.dat'
cd ..
rm -r ./Data/1D_Out
mkdir ./Data/1D_Out
cp ./Data/l_cluster/l_cluster_0.7/clustered_sdf.txt ./Data/Table/l_cluster_0.7.txt
sed -i '$d' ./Data/Table/l_cluster_0.7.txt
rm ./Data/Table/Result_1.dat
python ./Tools/Key_gen.v2.yg.py 5 ./Data/Table/l_cluster_0.7.txt > ./Data/Table/result_detail_0.7.txt
echo '##' >> ./Result_1.dat
cat ./Tools/l_cluster_DBSCAN.txt > ./Data/Table/l_cluster_DBSCAN.txt
sed -i '$d' ./Data/Table/l_cluster_DBSCAN.txt
python ./Tools/Key_gen.v2.yg.py 5 ./Data/Table/l_cluster_DBSCAN.txt > ./Data/Table/result_detail_DBSCAN.txt
mv ./Result_1.dat ./Data/Table/Result_1.dat
