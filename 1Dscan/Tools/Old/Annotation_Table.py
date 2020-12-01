import os, sys
import multiprocessing

R_ls = ['1R','2R','3R','4R','5R','6R','7R','8R']
#R_ls = ['1R','2R','3R']
#R_ls = ['1R']

os.chdir('../Data')
os.system('rm -r Annotation')
os.system('mkdir Annotation')
os.chdir('./Annotation')

os.system('cp ../../Tools/FAFDrugs2/example/faf2.param .')
os.system('cp ../../Tools/FAFDrugs2/example/groups.param .')
os.system('cp ../../Tools/FAFDrugs2/example/results.table.id .')

def func(sdf):
    os.system('python ../../Tools/FAFDrugs2/bin/FAFDrugs2.py faf2.param '+sdf)

sdf_ls = []
for R in R_ls:
    os.system('cp ../Dic_Lib_Output_PDB/'+R+'/SDF/* .')
    sdf_ls = sdf_ls + os.listdir('../Dic_Lib_Output_PDB/'+R+'/SDF/')

pool = multiprocessing.Pool(processes=23)
pool.map(func, sdf_ls)
pool.close()
pool.join()

os.system('cat ZINC*/*_results.table >> results.table.id')
os.system('rm -r ZINC*')
