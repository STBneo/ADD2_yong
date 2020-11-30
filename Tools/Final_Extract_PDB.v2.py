import os, sys

y_n = sys.argv[1]

if y_n == 'Y' or y_n == 'y':
    print('Clustering')
    os.chdir('../Data')
    os.system('rm -r ./l_cluster/l_cluster_0.9')
    os.system('mkdir ./l_cluster/l_cluster_0.9')
    os.chdir('./l_cluster/l_cluster_0.9')
    os.system('python ../../../Tools/l_clustering.v3.py 0.9')

    print('Convert sdf2pdb')
    os.chdir('../../../Data')
    os.system('rm -r ./Dic_Lib_Output_PDB')
    os.system('mkdir Dic_Lib_Output_PDB')
    os.chdir('./Dic_Lib_Output_PDB')
    os.system('python ../../Tools/sdf2pdb_with_cluster.py')

elif y_n == 'N' or y_n == 'n':
    print('Convert sdf2pdb')
    os.system('rm -r ../Data/Dic_Lib_Output_PDB')
    os.system('mkdir ../Data/Dic_Lib_Output_PDB')
    os.system('python sdf2pdb_without_cluster.py')
