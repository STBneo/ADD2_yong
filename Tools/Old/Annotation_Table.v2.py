import os, sys
import multiprocessing
from datetime import datetime

os.chdir('../Data')
os.system('rm -r Annotation')
os.system('mkdir Annotation')
os.chdir('./Annotation')

def FAF2(sdf):
    os.system('python ../../Tools/FAFDrugs2/bin/FAFDrugs2.py faf2.param '+sdf)
    #os.system('rm '+sdf)

def make_table(sdf):
    zid = sdf.split('.')[0]
    os.system('cat '+zid+'/'+zid+'_results.table >> results.table.id')
    #os.system('rm -r '+zid+'*')
    os.system('rm -r '+zid)

R_ls = os.listdir('../Dic_Lib_Output_PDB/')
for R in R_ls:
    os.system('cp -r ../Dic_Lib_Output_PDB/'+R+'/SDF .')
    os.system('mv SDF/* .')
    os.system('rm -r SDF')
    
sdf_ls = os.listdir('.')

os.system('cp ../../Tools/FAFDrugs2/example/faf2.param .')
os.system('cp ../../Tools/FAFDrugs2/example/groups.param .')
os.system('cp ../../Tools/FAFDrugs2/example/results.table.id .')

def print_date_time():
    now = datetime.now()
    w=datetime.now()
    dt_string=now.strftime("%d/%m/%Y %H:%M:%S")
    print 'Date and Time: ',dt_string

print('FAF2 annotation')
n_cpu = multiprocessing.cpu_count()-1
pool = multiprocessing.Pool(processes=n_cpu)
pool.map(FAF2, sdf_ls)
pool.close()
pool.join()

print('make FAF annotation table')
pool = multiprocessing.Pool(processes=n_cpu)
pool.map(make_table, sdf_ls)
pool.close()
pool.join()

print_date_time()
