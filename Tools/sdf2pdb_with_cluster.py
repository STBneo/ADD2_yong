import os,sys
import multiprocessing
from functools import partial

def pdb(l, pid):
    os.system('babel -isdf ../../Data/PASS/'+pid+'.sdf -opdb '+pid+'.pdb')

def main():
    fr = open('../../Data/l_cluster/l_cluster_0.9/zid_list.txt', 'r')
    lines = fr.readlines()
    pid_ls = []
    for line in lines:
        pid = line.strip()
        pid_ls.append(pid)
    fr.close()

    pool = multiprocessing.Pool(processes=n_cpu)
    m = multiprocessing.Manager()
    l = m.Lock()
    func = partial(pdb, l)
    pool.map(func, pid_ls)
    pool.close()
    pool.join()

if __name__=="__main__":
    main()
