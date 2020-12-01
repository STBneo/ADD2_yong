import os, sys
import multiprocessing
from datetime import datetime

os.chdir('../Data')
os.system('rm -r Annotation')
os.system('mkdir Annotation')
os.chdir('./Annotation')

def copy(sdf):
    os.system('cp -r '+sdf_path+sdf+' .')

def FAF2(sdf):
    os.system('python ../../Tools/FAFDrugs2/bin/FAFDrugs2.py faf2.param '+sdf)
    #os.system('rm '+sdf)

def make_table(sdf):
    zid = sdf.split('.')[0]
    os.system('cat '+zid+'/'+zid+'_results.table >> results.table.id')
    #os.system('rm -r '+zid+'*')
    os.system('rm -r '+zid)

sdf_path = '../FDA/PASS/'
print('Copy')
sdf_ls = os.listdir(sdf_path)
n_cpu = multiprocessing.cpu_count()-1
pool = multiprocessing.Pool(processes=n_cpu)
pool.map(copy, sdf_ls)
pool.close()
pool.join()
#sys.exit(1)
    
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
