import os,sys
import multiprocessing
from functools import partial
import glob

def pdb(l, sdf):
    pid = sdf[:-4]
    os.system('babel -isdf ../Data/PASS/'+sdf+' -opdb ../Data/Dic_Lib_Output_PDB/'+pid+'.pdb')

def main():
    sdf_ls = os.listdir('../Data/PASS/')

    print('Convert')
    n_cpu = multiprocessing.cpu_count()-1
    pool = multiprocessing.Pool(processes=n_cpu)
    m = multiprocessing.Manager()
    l = m.Lock()
    func = partial(pdb, l)
    pool.map(func, sdf_ls)
    pool.close()
    pool.join()

if __name__=="__main__":
    main()
