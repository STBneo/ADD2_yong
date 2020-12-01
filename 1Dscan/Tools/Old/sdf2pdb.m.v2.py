import os,sys
import multiprocessing
from functools import partial

def sdf(l, pid):
    R = sys.argv[1]
    os.system('cp ../../Data/l_cluster/l_cluster_0.9_'+R+'/sdf/'+pid+'.sdf '+R+'/SDF')
    '''
    sdf = pid+'.sdf'
    line = subprocess.check_output(['tail', '-1', sdf])
    if '$$$$' not in line:
        os.system('echo "\$\$\$\$" >> '+sdf)
    '''

def pdb(l, pid):
    R = sys.argv[1]
    os.system('babel -isdf '+R+'/SDF/'+pid+'.sdf -opdb '+R+'/'+pid+'.pdb')

def main():
    R = sys.argv[1]
    os.system('mkdir -p '+R+'/SDF')

    fr = open('../../Data/l_cluster/l_cluster_0.9_'+R+'/zid_list.txt', 'r')
    lines = fr.readlines()
    pid_ls = []
    for line in lines:
        pid = line.strip()
        pid_ls.append(pid)

    n_cpu = multiprocessing.cpu_count()-1
    pool = multiprocessing.Pool(processes=n_cpu)
    m = multiprocessing.Manager()
    l = m.Lock()
    func = partial(sdf, l)
    pool.map(func, pid_ls)
    pool.close()
    pool.join()

    pool = multiprocessing.Pool(processes=n_cpu)
    m = multiprocessing.Manager()
    l = m.Lock()
    func = partial(pdb, l)
    pool.map(func, pid_ls)
    pool.close()
    pool.join()

if __name__=="__main__":
    main()
