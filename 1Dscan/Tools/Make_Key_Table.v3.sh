#!/bin/bash

# Clustering by tanimoto score 0.7
echo 'Clustering upper 0.7 by DBSCAN'
rm Input.save1.npy
python Clustering_Input_ligand.DBSCAN.v5.yg.py y 0.3 0 > ../Data/Table/DBSCAN1.txt
mv ./l_cluster_DBSCAN1.txt ../Data/Table/l_cluster_DBSCAN1.txt
sed -i '$d' ../Data/Table/l_cluster_DBSCAN1.txt
python select_clustered_sdf.v3.py
sed -i '$d' ../Data/Table/l_cluster_DBSCAN1.txt

# Clustering by DBSCAN
echo 'Clustering under 0.7 by DBSCAN'
rm Input.save2.npy
python Clustering_Input_ligand.DBSCAN.v5.yg.py y 0.6 2 > ../Data/Table/DBSCAN2.txt
mv ./l_cluster_DBSCAN2.txt ../Data/Table/l_cluster_DBSCAN2.txt
sed -i '$d' ../Data/Table/l_cluster_DBSCAN2.txt
        
# Generate keys and make Result_1.dat
echo 'Generate keys and make Result_1.dat'
cd ..
rm -r ./Data/1D_Out
mkdir ./Data/1D_Out
rm ./Data/Table/Result_1.dat
python ./Tools/Key_gen.v3.yg.py 5 ./Data/Table/l_cluster_DBSCAN1.txt > ./Data/Table/result_detail_DBSCAN1.txt
echo '##' >> ./Result_1.dat
python ./Tools/Key_gen.v3.yg.py 5 ./Data/Table/l_cluster_DBSCAN2.txt > ./Data/Table/result_detail_DBSCAN2.txt
mv ./Result_1.dat ./Data/Table/Result_1.dat
