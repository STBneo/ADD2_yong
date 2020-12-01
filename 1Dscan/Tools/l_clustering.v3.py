import os, sys
import pandas as pd
import multiprocessing
from functools import partial

def make_sdf(score, l, pid):
    #print(score)
    if score == str(0.7):
        #copy sdf files
        fr = open('../../Input/'+pid+'.sdf', 'r')
        lines = fr.readlines()
        fw = open('./sdf/'+pid+'.sdf', 'w')
        for n, line in enumerate(lines):
            if n == 0: fw.write(pid+'\n')
            elif n > 0: fw.write(line)
            #elif 0 < n < len(lines)-1 : fw.write(line)
            #elif n == len(lines)-1 : fw.write('\n$$$$\n')
        fw.close()
        fr.close()
        #os.system('cp ../Data/Input/'+pid+'.sdf ./sdf')

    elif score == str(0.9):
        #copy sdf files
        os.system('cp ../../PASS/'+pid+'.sdf ./sdf')

def make_total_sdf(pid_ls):
    print('Make total.sdf')
    for pid in pid_ls:
        os.system('cat ./sdf/'+pid+'.sdf >> total.sdf')
        fr = open('./sdf/'+pid+'.sdf', 'r')
        al = fr.read()
        if '$$$$' not in al:
            os.system('echo "\$$\$$" >> total.sdf')
        fr.close()

def make_smi(pid_ls):
    print('Make smi files')
    os.system('mkdir smi')
    for pid in pid_ls:
        #print('babel -isdf ./sdf/'+pid+'.sdf -osmi ./smi/'+pid+'.smi')
        os.system('babel -isdf ./sdf/'+pid+'.sdf -osmi ./smi/'+pid+'.smi')
        
def make_total_fs():
    print('Make total.fs')
    os.system('babel total.sdf -ofs')

def make_result(pid_ls, score):
    print('Make result')
    os.system('mkdir result')
    #fw = open('ligand_'+score+'_result.txt', 'w')
    fw = open('result.txt', 'w')
    for pid in pid_ls:
        fw.writelines(pid+' '+pid+'\n')
        os.system('obabel ./total.fs -S ./smi/'+pid+'.smi -ofpt -at'+score+' > ./result/'+pid+'_result.txt')
        with open('./result/'+pid+'_result.txt', 'r') as fr: 
            lines = fr.readlines()
        for line in lines:
                if 'Tanimoto from' in line:
                    tanimoto = line.strip()
                    #print(tanimoto.split(' '))
                    B = tanimoto.split(' ')[0].replace('>','').replace('.pdb','')
                    A = tanimoto.split(' ')[5].replace('.pdb','')
                    #print(A+' '+B)
                    fw.writelines(A+' '+B+'\n')
                else: pass
    fw.close()

def result_to_number(pid_ls, score):
    pid_dic = {}
    for n, pid in enumerate(pid_ls):
        pid_dic[pid] = n+1 
    #print(pid_dic)

    #with open('ligand_'+score+'_result.txt', 'r') as fr: 
    with open('result.txt', 'r') as fr: 
        lines = fr.readlines()

    g1 = []
    g2 = []
    for line in lines:
        line = line.rstrip()
        #print(line)
        A = line.split(' ')[0]
        B = line.split(' ')[1]
        #print(A)
        #print(B)
        g1.append(pid_dic[A])
        g2.append(pid_dic[B])

    data = {'G1':g1,
            'G2':g2}
    df = pd.DataFrame(data)
    #print(pid_dic[A], pid_dic[B])
    #print(df)
    df = df.sort_values(['G1','G2'], ascending=[True,True])
    df = df.to_string(index=False, header=False)
    #print(df)
    #fw = open('ligand_'+score+'_number_result.sort.txt', 'w')
    fw = open('result_num.txt', 'w')
    fw.writelines(df)

def run_icliq(score):
    print('Run icliq')
    #os.system('cat ligand_'+score+'_number_result.sort.txt | uniq > ligand_'+score+'_number_result.sort.uniq.txt')
    os.system('cat result_num.txt | uniq > result_num_uniq.txt')
    os.system('gcc ../../../Tools/clustering_example/icliq.v2.c')
    #os.system('./a.out ligand_'+score+'_number_result.sort.uniq.txt xxx > ligand.'+score+'.clustered.out.txt')
    os.system('./a.out result_num_uniq.txt xxx > icliq_out.txt')

def parsing_clustered(pid_ls, score):
    pid_dic = {}

    for n, pid in enumerate(pid_ls):
        pid_dic[n+1] = pid 
    #print(pid_dic)

    #with open('ligand.'+score+'.clustered.out.txt', 'r') as f:
    with open('icliq_out.txt', 'r') as f:
        lines = f.readlines()

    #fw = open('ligand.'+score+'.chembl.clustered.out.txt', 'w')
    fw = open('icliq_out_pars.txt', 'w')
    total_nmem = 0

    for n, line in enumerate(lines):
        if n == 0: continue

        else:
            #print(line)
            gid = line[0:8].strip()
            nmem = line[9:17].strip()
            total_nmem += int(nmem)
            #mem = line[18:-1].strip()
            mem_ls = line[18:-1].strip().split(' ')
            new_mem_ls = []
            for mem in mem_ls:
                mem = int(mem)
                #print(mem)
                #print(pid_dic[mem])
                new_mem_ls.append(pid_dic[mem])
            new_mem_ls = str(new_mem_ls).replace('[','').replace(']','').replace(', ', '\t').replace("'",'')
            fw.write(gid+'\t'+nmem+'\t'+new_mem_ls+'\n')
            
            if n == len(lines)-1:
                if total_nmem != len(pid_ls):
                    fw.write(str(int(gid)+1)+'\t'+str(int(nmem))+'\t'+pid_ls[-1]+'\n')
                    fw.write('# Total chembl count : '+str(int(total_nmem)+1))
    fw.close()

def make_chembl_list(score):
    if score == str(0.9):
        #fr = open('ligand.0.9.chembl.clustered.out.txt', 'r')
        fr = open('icliq_out_pars.txt', 'r')
        #fw = open('chembl_list.txt', 'w')
        fw = open('zid_list.txt', 'w')
        lines = fr.readlines()
        #print(lines)
        for line in lines:
            if '#' not in line:
                cid = line.split('\t')[2]
                fw.write(cid.strip()+'\n')
        fr.close()
        fw.close()

def main():
    score = sys.argv[1]

    pid_ls = []
    if score == str(0.7):
        f = os.listdir('../../Input')
        for ff in f:
            pid = ff.split('.')[0]
            pid_ls.append(pid) 

    elif score == str(0.9):
        sdf_ls = os.listdir('../../PASS')
        for sdf in sdf_ls:
            pid = sdf[:-4]
            pid_ls.append(pid)
    #print(pid_ls)

    print('Make sdf files')
    os.system('mkdir sdf')
    if os.path.isfile('total.sdf'):
        os.system('rm total.sdf')
    n_cpu = multiprocessing.cpu_count()-1
    pool = multiprocessing.Pool(processes=n_cpu)
    m = multiprocessing.Manager()
    l = m.Lock()
    func = partial(make_sdf, score, l)
    pool.map(func, pid_ls)
    pool.close()
    pool.join() 

    make_total_sdf(pid_ls)
    make_smi(pid_ls)
    make_total_fs()
    make_result(pid_ls, score)
    result_to_number(pid_ls, score)
    run_icliq(score)
    parsing_clustered(pid_ls, score)
    make_chembl_list(score)

if __name__ == '__main__':
    main()
