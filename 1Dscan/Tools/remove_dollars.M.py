import sys,os
import glob
import multiprocessing

f_ls = glob.glob('../Data/Annotation/*.sdf')

def func(f):
    os.system('sed -i "$ d" '+f)

n_cpu = multiprocessing.cpu_count()-1
pool = multiprocessing.Pool(processes=n_cpu)
pool.map(func, f_ls)
pool.close()
pool.join()
