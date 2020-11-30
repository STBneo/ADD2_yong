import os,sys
import multiprocessing
from functools import partial

def sdf_2d(l, pid):
    R = sys.argv[1]
    os.system('cp ../../Data/l_cluster/l_cluster_0.9_'+R+'/sdf/'+pid+'.sdf '+R+'/SDF_2D')

def sdf_3d(l, pid):
    R = sys.argv[1]
    os.system('obgen '+R+'/SDF_2D/'+pid+'.sdf -ff UFF > '+R+'/SDF_3D/'+pid+'.sdf')

def pdb_3d(l, pid):
    R = sys.argv[1]
    os.system('babel -isdf '+R+'/SDF_3D/'+pid+'.sdf -opdb '+R+'/'+pid+'.pdb')

def main():
    R = sys.argv[1]
    os.system('mkdir -p '+R+'/SDF_2D '+R+'/SDF_3D')

    fr = open('../../Data/l_cluster/l_cluster_0.9_'+R+'/chembl_list.txt', 'r')
    lines = fr.readlines()
    pid_ls = []
    for line in lines:
        pid = line.strip()
        pid_ls.append(pid)

    pool = multiprocessing.Pool(processes=23)
    m = multiprocessing.Manager()
    l = m.Lock()
    func = partial(sdf_2d, l)
    pool.map(func, pid_ls)
    pool.close()
    pool.join()

    pool = multiprocessing.Pool(processes=23)
    m = multiprocessing.Manager()
    l = m.Lock()
    func = partial(sdf_3d, l)
    pool.map(func, pid_ls)
    pool.close()
    pool.join()

    pool = multiprocessing.Pool(processes=23)
    m = multiprocessing.Manager()
    l = m.Lock()
    func = partial(pdb_3d, l)
    pool.map(func, pid_ls)
    pool.close()
    pool.join()

if __name__=="__main__":
    main()
