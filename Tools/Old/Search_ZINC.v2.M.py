from os import walk
import sys, os
import string
from time import time
from shutil import copy
import shutil
import json
import numpy as np
#from pyRMSD.utils.proteinReading import Reader
#from pyRMSD.matrixHandler import MatrixHandler
#import pyRMSD.RMSDCalculator
import subprocess
import commands
from Bio import pairwise2
from Bio.Seq import Seq
from Bio.SubsMat import MatrixInfo as matlist
#import multiprocessing
#from functools import partial
from multiprocessing import Process, Manager
import shutil
import pickle
import itertools
import marshal
from itertools import repeat
import glob

# Usage: python Search_ZINC.py test.file (comma seperated!!)

def Run_search():

    time1=time()

    arg='rm -r ../Data/Dic_Lib_Output_SDF/*'
    os.system(arg)

    i_path='../Data/Dic_Lib_Input'
    i_files=glob.glob(i_path+'/*csv')
    #print i_files

    for afile in i_files:
        print afile
        total_input,f_count=Search_ZINC(afile)
        print 'Total input ligand is:',total_input
        print 'Total found ligand is:',f_count

    time2=time()
    print '\n\n     ===== Summary =====\n'
    print 'Processing time: '+str(time2-time1)+'\n'

    return 


def preps_input(lines):
    
    #file_bin=[[] for i in repeat(None, n)]
    file_bin=[[] for i in repeat(None, 21)]

    for line in lines:
        token=line.split(',')
        c_id=int(token[0][5:8])
        file_bin[c_id].append(token[0])

    return file_bin


def read_dic_files(file_list):
  
    ln_file_list=len(file_list)
    Dic_bin=[[] for i in repeat(None,ln_file_list)]

    #print ln_file_list
    #print Dic_bin

    r_count=0
    for a_file in file_list:
        print 'reading.....',a_file
        #print os.stat(a_file).st_size
        if(os.stat(a_file).st_size!=0):
            with open(a_file,'rb') as fp:
                Dic=marshal.load(fp)
                Dic_bin[r_count].append(Dic)
                #print Dic_bin
                #sys.exit(1)
        r_count+=1
        
    return Dic_bin


def Search_ZINC(afile):

    b_path='../Data/Dic_Lib_Output_SDF'

    token=afile.split('.')
    #print token[-2]
    t_path=os.path.join(b_path,token[-2])
    #print t_path
    
    if(os.path.isdir(t_path)):
        pass
        #print 'Yes'
    else:
        #print 'No'
        os.mkdir(t_path)
    #sys.exit(1)

    t_files=afile
    fp_for_in=open(t_files,'r')
    lines=fp_for_in.readlines()
    total_input=len(lines)
    fp_for_in.close()
    
    file_bin=preps_input(lines)
    #print file_bin

    f_count=0

    for index_cid in range(0,20):
        print 'Searching for cid:',index_cid
        file_list=[]
        for(path, dir, files) in os.walk('../Data/Dic_Lib'):
            dic_files = [fi for fi in files if fi.endswith('.dic')]
            t_file=str(index_cid)+'.dic'
            if t_file in dic_files:
                path_file=os.path.join(path,t_file)
                #print path_file
                file_list.append(path_file)
        file_list.sort()

        # Read dictionary files
        # Dic_bin=read_dic_files(file_list)

        SDFs=file_bin[index_cid]

        if len(SDFs)>0:    
            # Read dictionary files
            #Dic_bin=read_dic_files(file_list)
            #print file_list
            Dic={}

            for dic_file in file_list:
                if(os.stat(dic_file).st_size!=0):
                    print 'reading...',dic_file
                    with open(dic_file,'rb') as fp:
                        Dic=marshal.load(fp)
                        fp.close()
                        for a_sdf in SDFs:
                            #print type(Dic)
                            if a_sdf in Dic:
                                f_count+=1
                                #print 'find....',a_sdf
                                sdf_str=Dic[a_sdf]
                                fp_for_out=open(t_path+'/'+a_sdf+'.sdf','w')
                                fp_for_out.write(sdf_str)
                                fp_for_out.close()

            
    return total_input,f_count


############################################################


def Read_lib():

    tmp_list=[]
    sdf_path='./re_dic_test'

    files=os.listdir(sdf_path)
    #print files

    for f in files:
        #print f
        path_file=os.path.join(sdf_path,f)
        if not os.path.exists(sdf_path):
            pass
        else:
	    exists=os.path.isfile(path_file) 
	    if exists:
                with open(path_file,'rb') as fp:
                    Dic=marshal.load(fp)
                    tmp_list.append(Dic)
	    else:
                print 'There is no Dic marshal file'
    
    return tmp_list


def P_make_SDF_lib():

    '''
    # mulitprocessing part using pool and map
    pool = multiprocessing.Pool(processes=int(sys.argv[2]))
    #passing pararmeter like this and need 2 steps
    #func=partial(sub_make_complex,base_path)
    func=partial(sub_enva_analysis,fun_type,base_path,mylist)
    #map have only iteratable value
    fail_pdb=pool.map(func,to_be_process)
    fail_pids.append(fail_pdb)
    pool.close()
    pool.join()
    '''

    # remove the existing library file
    '''
    exists=os.path.isfile('./bin/ligand.lib.json')
    if exists:
        os.remove('./bin/ligand.lib.json')
    else:
        pass
    '''
    # start time
    time1=time()

    print '\nStarting making SDF_DIC files for searching file\n'
    # dictionary example a key:ADD, value: pdb_id1, pdb_id2,...,pdb_idn
    #lib_dic_a={}
    # dictionary example a key:pdb_id value:feaure{index}, feature{index}
    sdf_dic_f={}
    dic_count={}
    # later for efficency split input file into 1000?

    fp_for_in=open(sys.argv[1],'r')
    token=sys.argv[1].split('.')

    dump_count=0
    pass_count=0
    in_count=0
    dup_count=0
    line_count=0
    tmp_str=''


    while(True):
        line=fp_for_in.readline()
        line_count+=1
        if line=='':
            break

        if(line.startswith('ZINC')):
            key=line.strip()
        if line!='$$$$\n':
            tmp_str=tmp_str+line
        if line=='$$$$\n':
            in_count+=1
            tmp_str=tmp_str+line
            if key not in sdf_dic_f:
                pass_count+=1
                sdf_dic_f[key]=tmp_str
                tmp_str=''
            else:
                dup_count+=1
                print key,' is duplicated'

    fp_for_in.close()

    #print sdf_dic_f
    #print sdf_dic_f.keys()

    ouf=open('./'+token[0]+'.dic','wb')
    marshal.dump(sdf_dic_f,ouf)

    time2=time()
    #print '\nTotal ',dump_count,' ligands are processed!'
    print 'Total ',in_count,' ligands are inputed!'
    print 'Total ',pass_count,' ligands are passed!'
    print 'Total ',dup_count,' ligands are duplicted!'
    print '\nFinishing making dictionary files for searching file!!!!'
    print '\nProcessing time: '+str(time2-time1)+'\n'
    return

    #key_list=lib_dic_f.keys()
    #for akey in key_list:
        #print akey

    '''
    with open('./1D_lib_A.ADP.json','w') as fp:
	json.dump(lib_dic_a,fp)

    with open('./1D_lib_F.ADP.json','w') as fp:
	json.dump(lib_dic_f,fp)
    '''
    '''
    with open('./1D_lib_A.ADP.pickle','wb') as fp:
	pickle.dump(lib_dic_a,fp,protocol=pickle.HIGHEST_PROTOCOL)

    with open('./1D_lib_F.ADP.pickle','wb') as fp:
	pickle.dump(lib_dic_f,fp,protocol=pickle.HIGHEST_PROTOCOL)
    '''
    
    #ouf=open('./Data/Lib/1D_lib_A_M.dat','wb')
    #marshal.dump(lib_dic_a,ouf)
    #ouf.close()
    #print lib_dic_f
    ouf=open('./Data/Lib/1D_lib_F.ADP_m.dat','wb')
    marshal.dump(lib_dic_f,ouf)
    ouf.close()

    time2=time()
    print '\nTotal ',dump_count,' ligands are processed!'
    print 'Total ',in_count,' ligands are inputed!'
    print 'Total ',pass_count,' ligands are passed!'
    print 'Total ',dup_count,' ligands are duplicted!'
    print 'Finishing making Library files for 1D_scan!!!!'
    print '\nProcessing time: '+str(time2-time1)+'\n'
    
def make_head_sdf():

    base_path=os.getcwd()
    #print base_path
    #sys.exit(1)
    #t_path=sys.argv[1]
    #os.chdir(t_path)
    #work_path=os.getcwd()
    #print work_path
    files=filter(os.path.isfile, os.listdir(os.getcwd()))
    sdf_files = [fi for fi in files if fi.endswith('.sdf')]
    Z_sdf_files = [fi for fi in sdf_files if fi.startswith('Z')]
    #print len(sdf_files)

    for a_sdf in Z_sdf_files:
        #print a_sdf[:-4]
        Z_str=a_sdf[:-4]+'\n'
        fp_for_in=open(a_sdf,'r')
        head=fp_for_in.readline()
        lines=fp_for_in.readlines()
        fp_for_in.close()
        for line in lines:
            Z_str=Z_str+line

        #print Z_str
        fp_for_out=open(a_sdf,'w')
        fp_for_out.write(Z_str)
        #sys.exit(1)


def key_pattern():

    time1=time()

    item=['A','D','P']

    for n in range(4,7):
        
        print 'Starting making...',str(n),'lib'
        #candidate=list(map(''.join,itertools.product(item,repeat=n)))
        fp =open(sys.argv[1])
        dic_count={}
        dic_id={}

        dump_count=0
        while(1):
            line=fp.readline()
            if(line==''):
                break
            if 'dump' in line:
                dump_count+=1
                zid=line.split('\t')[0]
                zf=fp.readline().strip()
                ln_zf=len(zf)
                #print zf,ln_zf,
                #print zf,ln_zf
                if(int(n)<=ln_zf):
                    #print ln_zf
                    for s_i in range(0,ln_zf-n+1):
                        #print zf[s_i:s_i+n],
                        zkey=zf[s_i:s_i+n]
                        if not zkey in dic_count:
                            dic_id[zkey]=[zid]
                            dic_count[zkey]=1
                        else:
                            dic_id[zkey].append(zid)
                            dic_count[zkey]+=1
                    #print 
                else:
                    pass
                    #print
                #return

        fp.close()

        keys=dic_id.keys()
        for akey in keys:
            tmp_list=dic_id[akey]
            tmp2_list=list(set(tmp_list))
            dic_id[akey]=tmp2_list


        print 'Ending making ',str(n),'lib'
        ouf=open('./Data/Lib/1D_key_lib_'+str(n)+'_m.dat','wb')
        marshal.dump(dic_id,ouf)

    time2=time()

    print '\nTotal ',dump_count,' ligands are processed!'
    print 'Finishing making Key dictionary files for 1D_scan'
    print '\n\nProcessing time: '+str(time2-time1)+'\n\n'

def make_sdf_lib():

    base_path=os.getcwd()
    
    if not os.path.exists('./data/sdf_lib'):
        os.mkdir('./data/sdf_lib')

    #'''
    print '\nCopying the sdf files......\n'
    for(path, dir, files) in os.walk("./data/input"):
        #print path,dir,files
        #print path    
        sdf_files = [fi for fi in files if fi.endswith('.sdf')]
        if (len(sdf_files)!=0):
            #print sdf_files
            arg=path+'/'+sdf_files[0]
            #print arg
            os.system('cp '+arg+ ' ./data/sdf_lib')

            # example: subporcess.call
            # import subprocess
            # cmd = "git --version"
            # returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
            # print('returned value:', returned_value)
	    # zp = subprocess.call(['7z', 'a', '-p=swshin', '-y', z_name] + [a_file_loc])
    #'''
    print '\nMaking sdf library.....'
    os.chdir('./data/sdf_lib')
    #print os.getcwd()
    make_head_sdf()
    os.system('babel *.sdf -osmi -m')
    os.system('cat *.sdf > ligand.lib.sdf')
    os.system('babel ligand.lib.sdf -ofs')
    os.chdir(base_path)


def sub_processing(lib_dic_a,lib_dic_f,lines):

    tmp_dic={}

    #print lines
    l_count=0
    for ele in lines:
        print ele
        #sys.exit(1)

        # Check read_dump.py format
        # ---------------------------------------------
        if(ele[0]=='' or ele[1]=='' or ele[2]=='' or ele[3]==''):
            print ele
            print 'One or more lines are empty'
            print ele[1]
            print ele[2]
            print 'Pass the '+ele[0][:6]
            continue
            #sys.exit(1)

        if(len(ele[1])<=2):
            print 'the length of feature must be more than 3'
            print ele[1]
            print 'Pass the '+ele[0][:6]
            continue
        # ---------------------------------------------


        #print 'Porcessing.......PDB_id: '+ele
        token1=ele[0].split('\t')
        token3=ele[2].split(' ')
        token4=ele[3].split('\t')
        ln_ADP=len(ele[1])
        l_index=0
        end_of_ADP=ln_ADP-3
        while(l_index<=end_of_ADP):
            tmp_index=[]
            #print token1[0] # PDB id
            #print ele[1]    # feature list: 'ADPPDDDA'
            #print ele[1][l_index:l_index+3]  # 3features example: 'ADP'
            #print token3[l_index],token3[l_index+1],token3[l_index+2] # 3 indexes 

            # 3 Indexs
            tmp_index.append(int(token3[l_index]))
            tmp_index.append(int(token3[l_index+1]))
            tmp_index.append(int(token3[l_index+2]))


            # Making both Dictionary
            # For lib_dic_f
            '''
            if ele[1][l_index:l_index+3] in tmp_dic: #ele[1][l_index:l_index+3] 3 feature: ADP
                #d_value=[]
                #d_value.append(tmp_index)
                tmp_dic[ele[1][l_index:l_index+3]].append(tuple(tmp_index))
            else:
                d_value=[]
                d_value.append(tuple(tmp_index))
                tmp_dic[ele[1][l_index:l_index+3]]=d_value
            '''

            # For lib_dic_a
            if ele[1][l_index:l_index+3] in lib_dic_a: #ele[1][l_index:l_index+3] 3 feature: ADP
                d_value=[]
                # For removing redundancy in dic value_list
                '''
                d_value=lib_dic_a[ele[1][l_index:l_index+3]]
                print d_value
                pdb_set=set(d_value)
                if token1[0] in pdb_set:
                    pass
                else:
                    lib_dic_a[ele[1][l_index:l_index+3]].append(token1[0])
                '''
                # Allow redundancy
                lib_dic_a[ele[1][l_index:l_index+3]].append(token1[0])

            else:
                d_value=[]
                d_value.append(token1[0])
                lib_dic_a[ele[1][l_index:l_index+3]]=d_value


            # must be in last loop
            l_index+=1

        tmp_dic['f']=ele[1]
        # casting the chacter in int at once
        # tmp_dic['i']=map(int,token3)
        # tmp_dic['c']=token4
        #print tmp_dic
        lib_dic_f[token1[0]]=tmp_dic
        tmp_dic={}

    return lib_dic_a,lib_dic_f
    #return lib_dic_f

def P_make_lib():

    '''
    # mulitprocessing part using pool and map
    pool = multiprocessing.Pool(processes=int(sys.argv[2]))
    #passing pararmeter like this and need 2 steps
    #func=partial(sub_make_complex,base_path)
    func=partial(sub_enva_analysis,fun_type,base_path,mylist)
    #map have only iteratable value
    fail_pdb=pool.map(func,to_be_process)
    fail_pids.append(fail_pdb)
    pool.close()
    pool.join()
    '''

    # remove the existing library file
    '''
    exists=os.path.isfile('./bin/ligand.lib.json')
    if exists:
        os.remove('./bin/ligand.lib.json')
    else:
        pass
    '''
    # start time
    time1=time()

    print '\nStarting making Library files for 1DScan'
    # dictionary example a key:ADD, value: pdb_id1, pdb_id2,...,pdb_idn
    #lib_dic_a={}
    # dictionary example a key:pdb_id value:feaure{index}, feature{index}
    lib_dic_f={}
    dic_count={}
    # later for efficency split input file into 1000?

    fp_for_in=open(sys.argv[1],'r')

    dump_count=0
    pass_count=0
    in_count=0
    dup_count=0
    while(1):
        line=fp_for_in.readline()
        if line=='':
            break
        if 'dump' in line:
            dump_count+=1
            zid=line.split('\t')[0]
            zf=fp_for_in.readline().strip()
            if len(zf)>=4:
                if not zid in lib_dic_f:
                    lib_dic_f[zid]=zf
                    #dic_count[zid]=1
                    in_count+=1
                else:
                    print 'Something worng!'
                    print 'Two same key!'
                    print zid
                    dup_count+=1
                    #return
                    #lib_dic[zkey].append(zid)
                    #dic_count[zkey]+=1
            else:
                pass_count+=1
    fp_for_in.close()

    #key_list=lib_dic_f.keys()
    #for akey in key_list:
        #print akey

    '''
    with open('./1D_lib_A.ADP.json','w') as fp:
	json.dump(lib_dic_a,fp)

    with open('./1D_lib_F.ADP.json','w') as fp:
	json.dump(lib_dic_f,fp)
    '''
    '''
    with open('./1D_lib_A.ADP.pickle','wb') as fp:
	pickle.dump(lib_dic_a,fp,protocol=pickle.HIGHEST_PROTOCOL)

    with open('./1D_lib_F.ADP.pickle','wb') as fp:
	pickle.dump(lib_dic_f,fp,protocol=pickle.HIGHEST_PROTOCOL)
    '''
    
    #ouf=open('./Data/Lib/1D_lib_A_M.dat','wb')
    #marshal.dump(lib_dic_a,ouf)
    #ouf.close()
    #print lib_dic_f
    ouf=open('./Data/Lib/1D_lib_F.ADP_m.dat','wb')
    marshal.dump(lib_dic_f,ouf)
    ouf.close()

    time2=time()
    print '\nTotal ',dump_count,' ligands are processed!'
    print 'Total ',in_count,' ligands are inputed!'
    print 'Total ',pass_count,' ligands are passed!'
    print 'Total ',dup_count,' ligands are duplicted!'
    print 'Finishing making Library files for 1D_scan!!!!'
    print '\nProcessing time: '+str(time2-time1)+'\n'

def select_sample_random():

    # make ligand folder
    l_base='./Select_PDB_Ligand'
    if not os.path.exists(l_base):
        os.makedirs(l_base)
    else:
        arg='rm '+l_base+'/*.pdb'
        #print arg
        os.system(arg)
        #shutil.rmtree(l_base)

    # make receptor folder
    r_base='./Select_PDB_Receptor'
    if not os.path.exists(r_base):
        os.makedirs(r_base)
    else:
        arg='rm '+r_base+'/*.pdb'
        #print arg
        os.system(arg)
        #shutil.rmtree(r_base)

    i_base='./Select_PDB'
    if not os.path.exists(i_base):
        os.makedirs(i_base)
    else:
        arg='rm '+i_base+'/*.pdb'
        #print arg
        os.system(arg)
        #shutil.rmtree(i_base)

    target_list=[]
    cluster_list=[]
    fail_pdb=[]
    num_cluster=0

    fp_for_in=open(sys.argv[1],'r')
    head=fp_for_in.readline()
    lines=fp_for_in.readlines()
    ln_lines=len(lines)
    fp_for_in.close()
    #print ln_lines
    #sys.exit(1)

    tmp_pdb=[]
    fp_for_in2=open(sys.argv[2],'r')
    lines2=fp_for_in2.readlines()
    ln_lines2=len(lines)
    fp_for_in2.close()
    
    for line in lines2:
        fail_pdb.append(line.strip())
    #print fail_pdb
    
    l_count=0
    c_set=[]
    for i in range(0,ln_lines-1):
        token1=lines[i].split(',')
        token2=lines[i+1].split(',')
        if(token1[0]!=token2[0]):
            num_cluster+=1
            cluster_list.append(c_set)
            c_set=[]
        else:
            #print token1[1]
            c_set.append(token1[1])

    #print num_cluster
    #print cluster_list
    #sys.exit(1)

    t_count=0
    s_count=0
    for c in cluster_list:
        t_count+=1
        #print str(t_count)+':'+c[0]
        #print c
        f_count=0
        for sub_c in c:
            #print sub_c
            tmp_pdb=sub_c+'.pdb'
            #print tmp_pdb    
            #print fail_pdb
            #sys.exit(1)
            
            if sub_c in fail_pdb:
                print tmp_pdb+' is in fail list'
                break
            else:
                #sys.exit(1)    
                target_list.append(c[0])
                #print tmp_pdb

	        # check pdb_file_format 
	        exists=os.path.isfile(tmp_pdb) 
	        if exists:
                    HETATM_flag=0
                    atom_count=0
                    fp_for_pdbin=open(tmp_pdb)
                    lines=fp_for_pdbin.readlines()
                    fp_for_pdbin.close()

                    # 2 pass processing
                    receptor_str=''
                    ligand_str=''
                    atom_flag=0
                    hatom_flag=0
                    for line in lines:
                        # processing 'ATOM'
                        if(line.startswith('ATOM')):
                            atom_count+=1
                            receptor_str=receptor_str+line
                            atom_flag=1
                            # max atom count:8000
                            if(atom_count>=8000):
                                break
                        # for write the receptor
                        if(atom_flag==1 and not line.startswith('ATOM')):
                            receptor=receptor_str+'TER\n'+'END\n'
                            fp_for_out=open(r_base+'/'+sub_c+'_r.pdb','w')
                            fp_for_out.write(receptor)
                            fp_for_out.close()

                        # processing 'HETATM'
                        if(line.startswith('HETATM')):
                            HETATM_flag=1
                            '''
                            arg='cp '+tmp_pdb+' ./Select_PDB'
                            os.system(arg)
                            s_count+=1
                            f_count+=1
                            '''
			    if(line[12:17].strip()!='H'):
                                hatom_flag=1
                                ligand_str=ligand_str+line

			if(line.startswith('CONECT') or line.startswith('MASTER') ):
                            ligand_str=ligand_str+line

                        if(hatom_flag==1 and not line.startswith('HETATM') and not line.startswith('CONECT') and not line.startswith('MASTER')):
                            ligand=ligand_str+'TER\n'+'END\n'
                            fp_for_out=open(l_base+'/'+sub_c+'_l.pdb','w')
                            fp_for_out.write(ligand)
                            fp_for_out.close()
                            arg='cp '+tmp_pdb+' ./Select_PDB'
                            os.system(arg)
                            s_count+=1
                            f_count+=1

                    if HETATM_flag and f_count==2:
                        f_count=0
                        break
	        else:
		    break
    print len(target_list)
    print s_count
    #print fail_pdb
    #print target_list

def parsing_enva(*farg):

	p_dic = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K','ILE': 'I', 'PRO': 'P','THR': 'T', 'PHE': 'F', 'ASN': 'N', 'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R','TRP': 'W', 'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}

	type=01
	
	if(len(farg)==1):
		pdb_name=farg[0]
		type=1
	if(len(farg)==2):
		pdb_name=farg[0]
		t_pdb_p=farg[1]
		type=2

	fp_for_in=open(pdb_name,'r')
	head=fp_for_in.readline()
	lines=fp_for_in.readlines()
	fp_for_in.close()
	#print pdb_name
	
	m_pdb_f=[0]*9
	m_pdb_p=[]
	m_pdb_a=[]
	m_pdb_seq=''

	# M = np.empty((0,9),float)
	M = np.empty((0,8),float)

	#print pdb_name
	#sys.exit(1)

	c_count=0
	for line in lines:
		if(not line.startswith('END')):
			line=line.strip()
			token=line.split()
			if(token[29]!='---'):
				c_count+=1
				#print token
				#print line
				m_pdb_p.append(token[5])
				m_pdb_a.append(p_dic[token[3][-3:]])
				m_pdb_seq+=p_dic[token[3][-3:]]
				m_pdb_f[0]=m_pdb_f[0]+int(token[10]) # B-turn-1,else-0 **
				m_pdb_f[1]=m_pdb_f[1]+int(token[11]) # Acc
				m_pdb_f[2]=m_pdb_f[2]+int(token[12]) # Pol
				m_pdb_f[3]=m_pdb_f[3]+int(token[13]) # Phi **
				m_pdb_f[4]=m_pdb_f[4]+int(token[14]) # Psi
				m_pdb_f[5]=m_pdb_f[5]+int(token[15]) # Dep(0:surface,10:out)
				m_pdb_f[6]=m_pdb_f[6]+int(token[16]) # HF(0-10)
				m_pdb_f[7]=m_pdb_f[7]+int(token[21]) # Ac(water accessible) **
				m_pdb_f[8]=m_pdb_f[8]+int(token[22]) # Polarity **
				#print m_pdb_f
				#sys.exit(1)

				#tmp_a=np.array([[float(token[10]),float(token[11]),\
                                #float(token[12]),float(token[13]),float(token[14]),float(token[15]),float(token[16]),float(token[21]),float(token[22])]])
				# remove B-turn
				if(len(farg)==1):
					tmp_a=np.array([[float(token[11]),float(token[12]),\
                                        float(token[13]),float(token[14]),float(token[15]),float(token[16]),float(token[21]),float(token[22])]])
					M=np.vstack((M,tmp_a))
					#print token[11],token[12],token[13],token[14],token[15],token[16],token[21],token[22]
				if(len(farg)==2):
					if(token[5] in t_pdb_p):
						#print t_pdb_p
						#print token
						#print 'Find'
						#print token[5]
						tmp_a=np.array([[float(token[11]),float(token[12]),\
                                                float(token[13]),float(token[14]),float(token[15]),float(token[16]),float(token[21]),float(token[22])]])
						#print token
						#print token[11],token[12],token[13],token[14],token[15],token[16],token[21],token[22]
						M=np.vstack((M,tmp_a))
						#sys.exit(1)
					else:
						#print 'No'
						pass
					#sys.exit(1)
				#M=np.vstack((M,tmp_a))

        if(c_count==0):
            print pdb_name
            arg='enva_error'
            return arg
	#print m_pdb_f
	#if(type==2):
		#sys.exit(1)
	m_pdb_f[0]=float(m_pdb_f[0])/c_count
	m_pdb_f[1]=float(m_pdb_f[1])/c_count
	m_pdb_f[2]=float(m_pdb_f[2])/c_count
	m_pdb_f[3]=float(m_pdb_f[3])/c_count
	m_pdb_f[4]=float(m_pdb_f[4])/c_count
	m_pdb_f[5]=float(m_pdb_f[5])/c_count
	m_pdb_f[6]=float(m_pdb_f[6])/c_count
	m_pdb_f[7]=float(m_pdb_f[7])/c_count
	m_pdb_f[8]=float(m_pdb_f[8])/c_count
	#print m_pdb_f
	#sys.exit(1)
	#print m_pdb_f
	#print m_pdb_p
	#print m_pdb_a
	#print m_pdb_seq

	#Normalize M
	if(sys.argv[1]=='3'):
		#print 'Hi'
		#print M
		Max_M=M.max(axis=0)
		#print Max_M
		Min_M=M.min(axis=0)
		#print Min_M
		#for index in range(0,9):
		for index in range(0,8):
			#print index
			M[:,index]=(M[:,index]-Min_M[index])/(Max_M[index]-Min_M[index])
		#print M
		M_avg=np.average(M,axis=0)
		#print M_avg
		#print m_pdb_p
		#sys.exit(1)

        # return the sequence
	if(sys.argv[1]=='1'):
		return m_pdb_seq
        # return the feature
	if(sys.argv[1]=='2'):
		return m_pdb_f
        # return normalized value and total average
	if(sys.argv[1]=='3'):
		return M_avg, m_pdb_p


def enva_analysis():

    start=time()

    cpu_num=multiprocessing.cpu_count()
    if(len(sys.argv)!=3):
        print '\nUsage: program_name input_parameter num_of_cpu!!\n'
        return

    if(int(sys.argv[2])>cpu_num):
        print 'The number of cpu should be less than '+str(cpu_num)+'\n'
        return
    
    # for data commnuication
    mylist = Manager().list()
    base_path=os.getcwd()
    tar_dir=[]
    to_be_process=[]
    fail_pids=[]
    fun_type=sys.argv[1]

    fp_for_in=open('log.enva.analysis.txt','r')
    passed_id=fp_for_in.readlines()
    fp_for_in.close()

    listOfFiles=filter(os.path.isdir, os.listdir(os.getcwd()))
    listOfFiles.sort(reverse = True)

    #sys.exit(1)
    num_of_pid=len(listOfFiles)
    for d in listOfFiles:
        token=d.split('.')
        if(len(token)>=2):
            tar_dir.append(d)
    print len(tar_dir)
    print tar_dir
    #sys.exit(1)

    print '\n'
    for td in tar_dir:
        td_tmp=td
        td=td+'\n'
        if td not in passed_id:
            to_be_process.append(td_tmp)
        else:
            print td_tmp+': is already processed!\n'

    print to_be_process
    #sys.exit(1)

    # mulitprocessing part using pool and map
    pool = multiprocessing.Pool(processes=int(sys.argv[2]))
    #passing pararmeter like this and need 2 steps
    #func=partial(sub_make_complex,base_path)
    func=partial(sub_enva_analysis,fun_type,base_path,mylist)
    #map have only iteratable value
    fail_pdb=pool.map(func,to_be_process)
    fail_pids.append(fail_pdb)
    pool.close()
    pool.join()

    #print mylist

    fp_for_in=open('log.enva.analysis.txt','a')
    for l in mylist:
        fp_for_in.write(l+'\n')
    fp_for_in.close()
   
    end=time()
    t_s=end-start
    t_m=t_s/60
    t_d=t_m/24
    print 'Execution Time: day:'+str(t_d)+' min.:'+str(t_m)+' second: '+str(t_s)

    print 'failed_pid lists: '
    print fail_pids

    return


def sub_enva_analysis(fun_type,base_path,mylist,target_dir):


        #print fun_type,base_path,mylist,target_dir
        #return
        proc = os.getpid()

        t_path=base_path+'/'+target_dir
        #Binding PDB file and comformers
        os.chdir(t_path)
        listOfFiles= filter(os.path.isfile, os.listdir(os.getcwd()))
        enva_files = [fi for fi in listOfFiles if fi.endswith('.env')]
        enva_files.sort(reverse = True)
        #print enva_files


        # select original Complex
        listOfFiles= filter(os.path.isfile, os.listdir(os.getcwd()))
        files = [fi for fi in listOfFiles if fi.endswith('.pdb')]
        files.sort(reverse = True)

        pdb_orig=''
        fmin=1000
        for f in files:
            f_size=len(f)
            if f_size<fmin:
                fmin=f_size
                pdb_orig=f

        if(len(pdb_orig[:-4])!=5):
            print pdb_orig
            print 'check original pdb! there are no original PDB file!'
            return pdb_orig[:5]

        chain_id=pdb_orig[4:-4]
        print pdb_orig,chain_id

	# ENVA code
	arg2='../SP2.enva_ub -e '+pdb_orig+' '+chain_id
	print arg2
	os.system(arg2)
        #return 


        '''
	id_dic={}

	fp_for_pdb_list=open(sys.argv[1],'r')
	lines=fp_for_pdb_list.readlines()
	fp_for_pdb_list.close()

	for line in lines:
		line=line.strip()
		token=line.split('\t')
		if(len(token)==2):
			id_dic[token[0]]=token[1]
		if(len(token)==1):
			pass
	#print id_dic
        '''

	token_in=sys.argv[1].split('_')
	m_pdb=token_in[0]+'pdb.env'
        m_pdb=pdb_orig+'.env'
        #print m_pdb
        #return
       
        #print sys.argv[1],sys.argv[2]
        #return


	if(sys.argv[1]=='1' or sys.argv[1]=='2'):
		m_pdb_seq=parsing_enva(m_pdb)
	if(sys.argv[1]=='3'):
		m_pdb_nf,m_pdb_p=parsing_enva(m_pdb)
		m_pdb_nf[np.isnan(m_pdb_nf)]=0
		#print m_pdb_nf
		#print m_pdb_p

	#print m_pdb+':'+m_pdb_seq
	#sys.exit(1)
        #return

	matrix = matlist.blosum62
	gap_open = -1.5
	gap_extend = -1.5

	listOfFiles = os.listdir('./')  
	listOfFiles= filter(os.path.isfile, os.listdir(os.getcwd()))
	files = [fi for fi in listOfFiles if fi.endswith('.env')]
	# print listOfFiles
	#count=0
	tmp_str_l=''
	tmp_str_g=''
	tmp_str=''
	for afile in files:
		token=afile.split('.')
		if(len(token)!=5):
			continue
		else:
			env_id=token[2]

		if(sys.argv[1]=='1'):
			a_pdb_seq=parsing_enva(afile)
                        #return
			print 'ID:'+env_id
			print m_pdb+':'+m_pdb_seq
			print afile+':'+a_pdb_seq
                        #return
			#alignments = pairwise2.align.globalxx(seq1, seq2)
			alignments = pairwise2.align.localds(m_pdb_seq,a_pdb_seq,matrix,gap_open, gap_extend)
			top_aln=alignments[0]
			m_pdb_x, a_pdb_y, score, begin, end = top_aln
			print 'Local'
			print m_pdb_x+'\n'+a_pdb_y
			print str(score)+'\n'
			tmp_str_l=tmp_str_l+str(env_id)+'\t'+str(score)+'\n'


			alignments = pairwise2.align.globalds(m_pdb_seq,a_pdb_seq,matrix,gap_open, gap_extend)
			gtop_aln=alignments[0]
			gm_pdb_x, ga_pdb_y, gscore, gbegin, gend = gtop_aln
			print 'Global'
			print gm_pdb_x+'\n'+ga_pdb_y
			print str(gscore)+'\n\n'
			tmp_str_g=tmp_str_g+str(env_id)+'\t'+str(gscore)+'\n'

		if(sys.argv[1]=='2'):
			a_pdb_f=parsing_enva(afile)
			tmp_str=tmp_str+str(env_id)+'\t'
			for ele in a_pdb_f:
				tmp_str=tmp_str+str(ele)+'\t'
			tmp_str=tmp_str+'\n'
			#print tmp_str

		if(sys.argv[1]=='3'):
			t_pdb_nf,t_pdb_p=parsing_enva(afile,m_pdb_p)
                        print afile
			print m_pdb_nf
			#print t_pdb_nf
			t_pdb_nf[np.isnan(t_pdb_nf)]=0
			print t_pdb_nf
			print 'Difference:'
			result=m_pdb_nf-t_pdb_nf
			result_avg=np.average(result)
			print result
			print 'Average:'
			print result_avg
			print '\n\n'
			#if(env_id==76):
				#sys.exit(1)
			tmp_str=tmp_str+str(env_id)+'\t'+str(result_avg)+'\t'
			for ele in np.nditer(result):
				tmp_str=tmp_str+str(ele)+'\t'
			tmp_str=tmp_str+'\n'
			#print tmp_str

			#sys.exit(1)

	if(sys.argv[1]=='1'):
		fp_for_out=open('env_aligment_l_score.csv','w')
		fp_for_out.write(tmp_str_l)
		fp_for_out.close()
		fp_for_out=open('env_aligment_g_score.csv','w')
		fp_for_out.write(tmp_str_g)
		fp_for_out.close()

	if(sys.argv[1]=='2'):
                print target_dir
                print tmp_str
		fp_for_out=open('env_aligment_feature.csv','w')
		fp_for_out.write(tmp_str)
		fp_for_out.close()
	
	if(sys.argv[1]=='3'):
		fp_for_out=open('env_normal_feature.csv','w')
		fp_for_out.write(tmp_str)
		fp_for_out.close()
		pass

def make_complex():

	final_result=''
	
	f=[]
	f.append(sys.argv[1])
	base_pdb=''
    
	fn_token=sys.argv[1].split('.')
	mpdb_name=fn_token[0]
	chain_ID=mpdb_name[-1]
	#print chain_ID
	
	fp_for_in=open(sys.argv[1])
	lines=fp_for_in.readlines()
	
	for line in lines:
		#if(not line.startswith('HETATM')):
		if(line.startswith('ATOM')):
			base_pdb=base_pdb+line
	fp_for_in.close()
	#print base_pdb
	#sys.exit(1)
	
	listOfFiles = os.listdir('./')  
	# print listOfFiles
	listOfFiles= filter(os.path.isfile, os.listdir(os.getcwd()))
	#files = [fi for fi in listOfFiles if not fi.endswith('.pdb')]
	files = [fi for fi in listOfFiles if fi.endswith('.pdb')]
	# print listOfFiles
	count=0
	ln_files=len(files)
	for f in files:
		tmp_pdb=''
		#print f
		token_pdb=f.split('.')
		if len(token_pdb)!=3:
			continue 
        
		count+=1
		print str(count)+'/'+str(ln_files)+':'+f
		token_t=token_pdb[1].split('_')
		pdb_num=token_t[2]
		#print pdb_num
		pdb_tmp_name=token_pdb[0]+'.C'+pdb_num+'.pdb'
		fp_for_pdb=open(f,'r')
		lines_pdb=fp_for_pdb.readlines()
		fp_for_pdb.close()
		for line_pdb in lines_pdb:
			if(line_pdb.startswith('HETATM')):
				if(line_pdb[12:17].strip()!='H'):
					#print line_pdb.strip()
					#print line_pdb[12:17]
					tmp_pdb=tmp_pdb+line_pdb

			if(line_pdb.startswith('CONECT') or line_pdb.startswith('MASTER') ):
				tmp_pdb=tmp_pdb+line_pdb
				#print tmp_pdb
		#print tmp_pdb
		tmp_pdb_f=''
		tmp_pdb_f=base_pdb+tmp_pdb+'END\n'
		#print tmp_pdb_f
		tmp_pdb_name=mpdb_name+'.L.'+pdb_num+'.pdb'
		print tmp_pdb_name
		fp_out_tmp=open(tmp_pdb_name,'w')
		fp_out_tmp.write(tmp_pdb_f)
		fp_out_tmp.close()
		arg='python ../calculate_rmsd3 '+tmp_pdb_name+' ' +sys.argv[1]
		#print arg
		result = commands.getoutput(arg)
		#print result
		final_result=final_result+pdb_num+'\t'+str(result)+'\n'
		
		# ENVA code
		arg2='./enva -e '+tmp_pdb_name+' '+chain_ID
		print arg2
		os.system(arg2)

		os.unlink(tmp_pdb_name)
		#sys.exit(1)

	#os.unlink('tmp_pdb.pdb')
	
	#print final_result
	fp_for_out=open('./Final_RMSD_result.csv','w')
	fp_for_out.write(final_result)
	fp_for_out.close()

def calcal_rmsd():


    #print each_dir,pdb_id
    #exit(1)

    #print sys.argv[1]

    files=[]
    files.append(sys.argv[1])
    files.append(sys.argv[2])

    time1=time()
    M = np.empty((0,3),float)
    f_count=0
    atom_count=[] 
    
    #print files
    #sys.exit(1)

    for filename in files:
        ext=os.path.splitext(filename)[-1]
        if(ext=='.pdb'):
            f_count+=1
            #print filename
            #print path
            #M = np.empty((0,3),float)
            fp_for_in=open('./'+filename,'r')
            lines=fp_for_in.readlines()
            #print lines
            a_count=0
            for line in lines:
                if(line[0:4]=='ATOM'):
                    a_count+=1
                    line=line.strip()
                    x_c=float(line[30:39])
                    y_c=float(line[38:47])
                    z_c=float(line[46:55])
                    tmp_a=np.array([[x_c,y_c,z_c]])
                    #print tmp_a
                    #M=np.concatenate((M,tmp_a),axis=0)
                    M=np.vstack((M,tmp_a))

                if(line[0:6]=='HETATM'):
                    a_count+=1
                    line=line.strip()
                    x_c=float(line[30:39])
                    y_c=float(line[38:47])
                    z_c=float(line[46:55])
                    tmp_a=np.array([[x_c,y_c,z_c]])

                    #print tmp_a
                    #M=np.concatenate((M,tmp_a),axis=0)
                    M=np.vstack((M,tmp_a))
            print str(f_count)+'th '+filename+' atom count is '+str(a_count)
            atom_count.append(a_count)
            #print M
            #print 
            #print M.shape
            #sys.exit(1)
    #print f_count,filename
    #print f_count,path
    #print M.shape
    print atom_count
    #sys.exit(1)

    #pdb_id=pdb_id+'_'+path+'.npy'
    #token=path.split('_')

    #t_pdb_id=pdb_id+token[1][0:2]+'.npy'
    #print t_pdb_id
    #np.save('./'+t_pdb_id,M)
    #M = np.empty((0,3),float)
    #sys.exit(1)
    #print M
    #sys.exit(1)
    #print path

    #print f_count, a_count
    #M=M.reshape(f_count,a_count,3)
    #print M
    #print M.shape
    #pdb_id=pdb_id+'.npy'
    #np.save('./'+pdb_id,M)
    
    #M=merge_matrix(pdb_id)
    M=M.reshape(f_count,a_count,3)
    print M
    print M.shape
    # sys.exit(1)
    #mHandler = MatrixHandler()
    #matrix = mHandler.createMatrix(M,'KABSCH_SERIAL_CALCULATOR')
    #inner_data = rmsd_matrix.get_data() 

    #rmsd_matrix = MatrixHandler().createMatrix(M,'KABSCH_SERIAL_CALCULATOR')
    #inner_data = rmsd_matrix.get_data() 
    #print inner_data
    calculator = pyRMSD.RMSDCalculator.RMSDCalculator(M,'KABSCH_SERIAL_CALCULATOR')
    rmsd = calculator.pairwiseRMSDMatrix()
    rmsd_matrix = CondensedMatrix(rmsd)
    inner_data = rmsd_matrix.get_data()


    # Save the matrix to 'to_this_file.bin'
    # mHandler.saveMatrix(pdb_id)
    # Load it from 'from_this_file.bin'
    # mHandler.loadMatrix("from_this_file")
    # Get the inner CondensedMatrix instance
    # rmsd_matrix = mHandler.getMatrix()
    # print rmsd_matrix

    # rmsd_matrix = MatrixHandler().createMatrix(M, 'KABSCH_SERIAL_CALCULATOR')
    #print M
    #print M.shape
    #pdb_id=pdb_id+'.npy'
    #np.save('./'+pdb_id,M)

    time2=time()
    print time2-time1
    #sys.exit(1)



def extract_coordinate(line):
    
    coordinate=[]

    x_c=line[30:39]
    y_c=line[38:47]
    z_c=line[46:55]

    return


def make_all_pdb():

    #listOfFiles = os.listdir('.')  
    listOfFiles= filter(os.path.isdir, os.listdir(os.getcwd()))
    #print listOfFiles
    #exit(1)
    p_count=0
    for pdb_id in listOfFiles:
        print 'Processing........'+pdb_id
        path='./'+pdb_id
        #print path
        #exit(1)
        make_npy_data(path,pdb_id)
        p_count+=1
        if(p_count==10):
            break
        #merge_matrix(pdb_id)

    return

def merge_matrix(pdb_id):
    
    listOfFiles= filter(os.path.isfile, os.listdir(os.getcwd()))
    files = [ fi for fi in listOfFiles if fi.startswith(pdb_id) ]

    M = np.empty((0,3),float)
    for ele in files:
        #print ele
        test_data=np.load(ele)
        #print test_data.shape
        M=np.vstack((M,test_data))
        os.remove(ele)

    return M
        

def make_npy_data(each_dir,pdb_id):

    #print each_dir,pdb_id
    #exit(1)

    time1=time()
    M = np.empty((0,3),float)
    f_count=0
    #for(path, dir, files) in os.walk("./"):
    for(path, dir, files) in os.walk(each_dir):
        if not dir:
            #print path
            ln_files=len(files)
            #print ln_files
            if ln_files>0:
                for filename in files:
                    ext=os.path.splitext(filename)[-1]
                    if(ext=='.pdb'):
                        f_count+=1
                        #print filename
                        #print path
                        #M = np.empty((0,3),float)
                        fp_for_in=open(path+'/'+filename,'r')
                        lines=fp_for_in.readlines()
                        #print lines
                        a_count=0
                        for line in lines:
                            if(line[0:4]=='ATOM'):
                                a_count+=1
                                line=line.strip()
                                x_c=float(line[30:39])
                                y_c=float(line[38:47])
                                z_c=float(line[46:55])
                        
                                tmp_a=np.array([[x_c,y_c,z_c]])
                                #print tmp_a
                                #M=np.concatenate((M,tmp_a),axis=0)
                                M=np.vstack((M,tmp_a))
                        #print M
                        #print 
                        #print M.shape
                        #sys.exit(1)
                    #print f_count,filename
                #print f_count,path
                #print M.shape
                #pdb_id=pdb_id+'_'+path+'.npy'
                token=path.split('_')

                t_pdb_id=pdb_id+token[1][0:2]+'.npy'
                print t_pdb_id
                np.save('./'+t_pdb_id,M)
                M = np.empty((0,3),float)
                #sys.exit(1)
                #print M
                #sys.exit(1)
        #print path

    #print f_count, a_count
    #M=M.reshape(f_count,a_count,3)
    #print M
    #print M.shape
    #pdb_id=pdb_id+'.npy'
    #np.save('./'+pdb_id,M)
    
    M=merge_matrix(pdb_id)
    M=M.reshape(f_count,a_count,3)
    print M.shape
    mHandler = MatrixHandler()
    matrix = mHandler.createMatrix(M,'KABSCH_SERIAL_CALCULATOR')
    # Save the matrix to 'to_this_file.bin'
    mHandler.saveMatrix(pdb_id)
    # Load it from 'from_this_file.bin'
    # mHandler.loadMatrix("from_this_file")
    # Get the inner CondensedMatrix instance
    # rmsd_matrix = mHandler.getMatrix()

    #rmsd_matrix = MatrixHandler().createMatrix(M, 'KABSCH_SERIAL_CALCULATOR')
    #print M
    #print M.shape
    #pdb_id=pdb_id+'.npy'
    #np.save('./'+pdb_id,M)

    time2=time()
    print time2-time1
    #sys.exit(1)


def make_Pariwise_matrix():

    time1=time()
    coordinates=np.load('1rbp.npy')
    #rmsd_matrix = MatrixHandler().createMatrix(coordinates, 'QCP_SERIAL_CALCULATOR')
    rmsd_matrix = MatrixHandler().createMatrix(coordinates, 'KABSCH_SERIAL_CALCULATOR')
    inner_data = rmsd_matrix.get_data() 
    print inner_data
    time2=time()
    print time2-time1


def add_file_dic_file(tlig_dict,a_file_loc):

	#print a_file_loc
	token=a_file_loc.split('/')
	#print token[-1]
	e_z_name=token[-1]
	#exit(1)
	token1=e_z_name.split('_')
	#print token1[0]
	lig = STBLigand.LigFV(token1[0])
	lig.reload_ligfv(a_file_loc) 
	ln_fseq_count=len(lig.l_fseq)

	l_index=0
	while(l_index<ln_fseq_count):
		alig_dic = {}
		index_A = []
		index_D = []
		index_P = []
		seq = ''.join(lig.l_fseq[l_index])

		index = 0
    		for atom in seq:
    			if atom=='A':
				index_A.append(index)
			if atom=='D':
				index_D.append(index)
			if atom=='P':
				index_P.append(index)
			index+=1
		alig_dic['A']=index_A
		alig_dic['D']=index_D
		alig_dic['P']=index_P
		l_name=lig.title+'.'+str(0)

		tlig_dict[l_name]=alig_dic
		l_index += 1
	return tlig_dict

def make_lib_fold():

	print 'Warning!!!: the exsiting library fold will be deleted! and New library fold will be created'
	check=raw_input("Press Enter to continue...or Press \'n\' to quit: ")
	if(check=='n'):
		sys.exit(1)

	
        # remove the existing library folder
	try:
		shutil.rmtree('./PHscan_Lib1')
	except OSError as e:
		#print ("Error: %s - %s." % (e.filename, e.strerror))
		print '\n\nThere is no \'PHscan_Lib1i\'  but we will create!\n\n'
		#sys.exit(1)


	# remove the existing library file
	exists=os.path.isfile('./ligand.lib.json') 
	if exists:
		os.remove('./ligand.lib.json')
	else:
		pass

	# remove the existing loc. file
	exists=os.path.isfile('./ligand.loc.json') 
	if exists:
		os.remove('./ligand.loc.json')
	else:
		pass
	
	path_base=os.getcwd()
	target='/input'
        i_base='./input'


	input_dir_base=path_base+'/input' 
	#print input_dir_base
	#print path_base+target
 
	if not os.path.exists(i_base):
		print '\nThere is no \'input\' fold!'
    		print 'Make a \'input\' fold!! and put the pdb list!!\n'
    		sys.exit(1)

	#input_fold=os.chdir(path_base+target)
	lines=os.listdir(i_base)
	#print lines
	#exit(1)
	nf_count=0
	tlig_dict={}
	loc_dict={}
	for line in lines:
		tmp_pos='./PHscan_Lib1'
		line=line.strip()
		for c_char in line:
        		tmp_pos=tmp_pos+'/'+c_char
    		#tmp_pos = path_base + tmp_pos
		#print tmp_pos
		#exit(1)
		if not os.path.exists(tmp_pos):
			nf_count+=1
			print "path doesn't exist. trying to make"
			os.makedirs(tmp_pos)
			#source_dir=input_dir_base+'/'+line
			source_dir=i_base+'/'+line
                        #print source_dir
			source_files=os.listdir(source_dir)
                        #print source_files

			loc_dict[line]=tmp_pos
                        #print loc_dict
	
			#exit(1)
			for a_file in source_files:
				if(a_file.find('_conf.')==-1):
					a_file_loc=source_dir+'/'+a_file
					copy(a_file_loc,tmp_pos)
				else:
					a_file_loc=source_dir+'/'+a_file
					z_name=source_dir+'/'+a_file+'.zip'
					#print z_name
					#print a_file_loc
					#sys.exit(1)

					if(a_file.find('_conf.dump')!=-1):
						tlig_dict=add_file_dic_file(tlig_dict,a_file_loc)
						#sys.exit(1)
					#sys.exit(1)

					zp = subprocess.call(['7z', 'a', '-p=swshin', '-y', z_name] + [a_file_loc])
					#a_file_loc_zip=a_file_loc+'.zip'
					#print a_file_loc
					z_file_loc=a_file_loc+'.zip'
					#print a_file_loc,z_file_loc,tmp_pos
					copy(z_file_loc,tmp_pos)
					os.remove(z_file_loc)
					#sys.exit(1)
				#sys.exit(1)
			#sys.exit(1)
		#sys.exit(1)
		else:
			lines=os.listdir(tmp_pos)
			num_files=len(lines)
			#print num_files
			if(num_files==8):
				print '\nPdb \''+line+'\' is already processed and exists!\n'
			else:
				print 'Some file is omitted! Check fold:'+tmp_pos+'\n'
				sys.exit(1)
		#sys.exit(1)
		#print tmp_pos

	with open('./ligand.loc.json','w') as fp1:
		json.dump(loc_dict,fp1)

	with open('./ligand.lib.json','w') as fp2:
		json.dump(tlig_dict,fp2)
	print '\n\n\nTotal '+str(nf_count)+' id(s) is(are) created and made a new library fold!\n\n\n'


def add_lib_fold():

        i_base='./input'
        l_base='./PHscan_Lib1'

        if not os.path.exists(l_base):
            pass
        else:
	    ## Loading existing lib file
    	    js = open('./ligand.lib.json').read()
	    tlig_dict= json.loads(js)

	    ## Loading existing lib loc. file
	    js = open('./ligand.loc.json').read()
	    loc_dict= json.loads(js)


	path_base=os.getcwd()
	target='/input'
        
	input_dir_base=path_base+'/input' 
	#print input_dir_base
	#print path_base+target


	if not os.path.exists(i_base):
		print '\nThere is no \'input\' fold!'
    		print 'Make a \'input\' fold!! and put the pdb list!!\n'
    		sys.exit(1)

	#input_fold=os.chdir(path_base+target)
	lines=os.listdir(i_base)
	#print lines
	#exit(1)

	af_count=0
	ef_count=0
	for line in lines:
		tmp_pos='./PHscan_Lib1'
		line=line.strip()
		for c_char in line:
        		tmp_pos=tmp_pos+'/'+c_char
    		#tmp_pos = path_base + tmp_pos
		#print tmp_pos
		#exit(1)
		if not os.path.exists(tmp_pos):
			af_count+=1
			print 'path doesn\'t exist. trying to make'
			os.makedirs(tmp_pos)
			#source_dir=input_dir_base+'/'+line
			source_dir=i_base+'/'+line
			source_files=os.listdir(source_dir)

			loc_dict[line]=tmp_pos

			#exit(1)
			for a_file in source_files:
				if(a_file.find('_conf.')==-1):
					a_file_loc=source_dir+'/'+a_file
					copy(a_file_loc,tmp_pos)
				else:
					a_file_loc=source_dir+'/'+a_file
					z_name=source_dir+'/'+a_file+'.zip'
					#print z_name
					#print a_file_loc
					#sys.exit(1)

					if(a_file.find('_conf.dump')!=-1):
						tlig_dict=add_file_dic_file(tlig_dict,a_file_loc)
						#sys.exit(1)

					zp = subprocess.call(['7z', 'a', '-p=swshin', '-y', z_name] + [a_file_loc])
					#a_file_loc_zip=a_file_loc+'.zip'
					#print a_file_loc
					z_file_loc=a_file_loc+'.zip'
					#print a_file_loc,z_file_loc,tmp_pos
					copy(z_file_loc,tmp_pos)
					os.remove(z_file_loc)
					#sys.exit(1)
				#sys.exit(1)
			#sys.exit(1)
		#sys.exit(1)
		else:
			ef_count+=1
			lines=os.listdir(tmp_pos)
			num_files=len(lines)
			#print num_files
			if(num_files==8):
				print '\nPdb \''+line+'\' is already processed and exists!\n'
			else:
				print 'Some file is omitted! Check fold:'+tmp_pos+'\n'
				sys.exit(1)
		#sys.exit(1)
		#print tmp_pos

	## Dump location to file
	with open('./ligand.loc.json','w') as fp1:
		json.dump(loc_dict,fp1)

	## Dump dictionary to file
	with open('./ligand.lib.json','w') as fp2:
		json.dump(tlig_dict,fp2)

	print '\n\n\n'
	print 'Total '+str(af_count)+' id(s) is(are) added to library fold!'
	print 'Total '+str(ef_count)+' id(s) exist(s) and skipped!\n\n'


def del_lib_fold():

	print 'Warning!!!: the exsiting library fold(s) will be deleted!'
	check=raw_input("Press Enter to continue...or Input \'n\' to quit: ")
	if(check=='n'):
		sys.exit(1)

        l_base='./PHscan_Lib1'
        if not os.path.exists(l_base):
            pass
        else:
	    ## Loading existing lib file
    	    js = open('./ligand.lib.json').read()
	    tlig_dict= json.loads(js)

	    ## Loading existing lib loc. file
	    js = open('./ligand.loc.json').read()
	    loc_dict= json.loads(js)


	path_base=os.getcwd()
	target='/input'

	pdb_id_lists=[]
        ln_sys_argv=len(sys.argv)
        for ele in range(2,ln_sys_argv):
            pdb_id_lists.append(sys.argv[ele])
	#target_id=sys.argv[2]
	#print target_id+'HIHIHI'
	#exit(1)
	if(len(pdb_id_lists)==0):
		show_usage()
		sys.exit(1)

	## Check if argv is file or not.
	exists=os.path.isfile('./'+pdb_id_lists[0]) 
	if exists:
		fp_for_in=open('./'+ipdb_id_lists[0],'r')
		pdb_id_lists=fp_for_in.readlines()
                fp_for_in.close()
	
	input_dir_base=path_base+'/input' 

	df_count=0
	print 

        # if case is 'All'
        if(pdb_id_lists[0]=='All' or pdb_id_lists[0]=='all'):
            if not os.path.exists(l_base):
                print 'There is no PHscan_lib1 folds\n'
                sys.exit(1)
            else:
                ## Remove the all library fold
                shutil.rmtree(l_base)
                print 'All PHscan_lib1 folds are removed!\n'

		## Remove the existing library file
		exists=os.path.isfile('./ligand.lib.json') 
		if exists:
		    os.remove('./ligand.lib.json')
		else:
		    pass

		## Remove the existing loc file
		exists=os.path.isfile('./ligand.loc.json') 
		if exists:
		    os.remove('./ligand.loc.json')
		else:
		    pass
                sys.exit(1)
        else:
            tmp_pos='./PHscan_Lib1'
            for line in pdb_id_lists:
	        line=line.strip()

		## Making path with pdb id
		for c_char in line:
        		tmp_pos=tmp_pos+'/'+c_char
    		#tmp_pos = path_base + tmp_pos
		#print tmp_pos
		#exit(1)
		
                if not os.path.exists(tmp_pos):
			print 'PDB id:'+line+' is not found! and check the id again!\n\n'
			exit(1)
		else:
			# remove the existing library folder
			try:
				print 'Delelting the '+line+' fold and fiels!'
				shutil.rmtree(tmp_pos)
				del tlig_dict[line+'.0']
				del loc_dict[line]
				df_count+=1
			except OSError as e:
				print ("Error: %s - %s." % (e.filename, e.strerror))
				os.exit(1)

	## Dump location to file
	with open('./ligand.loc.json','w') as fp1:
		json.dump(loc_dict,fp1)

	## Dump dictionary to file
	with open('./ligand.lib.json','w') as fp2:
		json.dump(tlig_dict,fp2)

	print '\n\n\nTotal '+str(df_count)+' id(s) is(are) deleted\n\n\n'

        sys.exit(1)

        '''
	for line in pdb_id_lists:
		tmp_pos='/PHscan_Lib1'
		line=line.strip()
		
		# if case is 'All'
		if (line=='All' or line=='all'):
			if not os.path.exists('.'+tmp_pos):
				sys.exit(1)
			else:
				## Remove the all library fold
				shutil.rmtree('.'+tmp_pos)
				## Remove the existing library file
				exists=os.path.isfile('./ligand.lib.json') 
				if exists:
					os.remove('./ligand.lib.json')
				else:
					pass
				## Remove the existing loc file
				exists=os.path.isfile('./ligand.loc.json') 
				if exists:
					os.remove('./ligand.loc.json')
				else:
					pass
				sys.exit(1)
	
		## Making path with pdb id
		for c_char in line:
        		tmp_pos=tmp_pos+'/'+c_char
    		tmp_pos = path_base + tmp_pos
		print tmp_pos
		#exit(1)

		if not os.path.exists(tmp_pos):
			print 'PDB id:'+line+' is not found! and check the id again!'
			exit(1)
		else:
			# remove the existing library folder
			try:
				print 'Delelting the '+line+' fold and fiels!'
				shutil.rmtree(tmp_pos)
				del tlig_dict[line+'.0']
				del loc_dict[line]
				df_count+=1
			except OSError as e:
				print ("Error: %s - %s." % (e.filename, e.strerror))
				os.exit(1)
	
	## Dump location to file
	with open('./ligand.loc.json','w') as fp1:
		json.dump(loc_dict,fp1)

	## Dump dictionary to file
	with open('./ligand.lib.json','w') as fp2:
		json.dump(tlig_dict,fp2)
	print '\n\n\nTotal '+str(df_count)+' id(s) is(are) deleted\n\n\n'
        '''

def show_lib_fold_info():

	# Read the lib file as global variable
	ligand_dict={}
	exists = os.path.isfile('./ligand.lib.json') 
	if exists:
		js= open('./ligand.lib.json').read()
		ligand_dict = json.loads(js)
		icount=0
		for key, value in ligand_dict.iteritems():
			print key, value
			icount+=1
		print 'Total '+str(icount)+' id exists\n'
	else:
		print 'There are no \'ligand.lib.json\' file'
		print 'Creat the \'ligand.lib.json\' file first! using optiion -c'


def show_usage():
	print 'Usage: command \'-c\' to creat a new indexing file'
	print '               \'-a\' to add a new id to indexing file'
	print '               \'-d\' id or id_list_file  to delete a id from indexing file'
	print '               \'-s\' to show indexing file'


#def main(flag):
def main():

    Run_search()
    #Search_ZINC()
    #P_make_SDF_lib()
    #P_make_lib()
    #key_pattern()
    #make_sdf_lib()
    #select_sample_random()
    #enva_analysis()
    #make_complex()
    # calcal_rmsd()
    # make_all_pdb()
    # make_npy_data()
    # make_Pariwise_matrix()


if __name__=="__main__":

        '''
	flag=0
	os.system('clear')
	num_of_arg=len(sys.argv)
	#print sys.argv, num_of_arg
	if(2==len(sys.argv) and sys.argv[1]=='-c'):
		#print sys.argv[1]
		print 'Creating a new indexing file\n'
		flag=1
		main(flag)
	
	if(2==len(sys.argv) and sys.argv[1]=='-a'):
		#print sys.argv[1]
		print 'Adding a pdb into indexing file\n'
		flag=2
		main(flag)

	if(3<=len(sys.argv) and sys.argv[1]=='-d'):
		#print sys.argv[1]
		print 'Deleting a pdb(s) from indexing file\n'
		flag=3
		main(flag)

	if(2==len(sys.argv) and sys.argv[1]=='-d'):
		#print sys.argv[1]
		#print 'Deleting a pdb(s) from indexing file\n'
		flag=5
		main(flag)

	if(2==len(sys.argv) and sys.argv[1]=='-s'):
		#print sys.argv[1]
		print 'Dispalying  indexing file\n'
		flag=4
		main(flag)

	if(1==len(sys.argv)):
		flag=5
		main(flag)
        '''
        main()
