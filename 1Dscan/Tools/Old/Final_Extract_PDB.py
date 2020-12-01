import os, sys

R_ls = os.listdir('../Data/Dic_Lib_Output_SDF/')
R_ls = sorted(R_ls)
#R_ls = ['1R','2R','3R','4R','5R','6R','7R','8R']
#R_ls = ['1R']
os.chdir('../Data')
os.system('rm -r ../Data/Dic_Lib_Output_PDB')
os.system('mkdir ../Data/Dic_Lib_Output_PDB')
for R in R_ls:
    os.system('rm -r ./l_cluster/l_cluster_0.9_'+R)
    os.system('mkdir -p ./l_cluster/l_cluster_0.9')
    os.chdir('./l_cluster/l_cluster_0.9')

    os.system('python ../../../Tools/make_zinc_list_0.9.py '+R)
    os.system('cat zid_list_'+R+'.txt | sort | uniq > zid_list_'+R+'_uniq.txt')

    os.system('python ../../../Tools/l_clustering.v2.py 0.9 '+R)

    os.chdir('../../..')
    os.system('mv ./Data/l_cluster/l_cluster_0.9 ./Data/l_cluster/l_cluster_0.9_'+R)

    os.chdir('./Data/Dic_Lib_Output_PDB')
    os.system('rm -rf '+R)
    os.system('python ../../Tools/sdf2pdb.m.v2.py '+R)

    os.chdir('..')
