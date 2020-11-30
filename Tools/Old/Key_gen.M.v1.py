import itertools
import os,sys
import pandas as pd
import random
import time
import pickle
import marshal

def Read_lib(lib_file):
    l_base='.././Data/Lib'

    chembl_dic={}

    path_file=os.path.join(l_base,lib_file)
    if not os.path.exists(l_base):
        pass
    else:
	exists=os.path.isfile(path_file) 
	if exists:
            with open(path_file,'rb') as fp:
                Dic=marshal.load(fp)
	else:
            print 'There is no Dic.picklefile'
            return

    return Dic


def make_dic(Key_dic,AFile_dic,list_count,files):

    ln_key=int(sys.argv[1])

    item=['A','D','P']
    candidate=list(map(''.join,itertools.product(item,repeat=ln_key)))

    dic_count={}
    dic_id={}

    for afile in files:
        #print afile,afile[:-4]
        #feat=AFile_dic[afile[:-4]]['f']
        feat=AFile_dic[afile[:-4]]
        print afile,feat,len(feat)
        
        check_list=[]
        for c_tmp in candidate:
	    if c_tmp in feat:
	    #if feat in c_tmp:
		    #check_list.append(name)
		    if not c_tmp in dic_count:
			dic_id[c_tmp]=[afile[:-4]]
			dic_count[c_tmp]=1
		    else:
			dic_id[c_tmp].append(afile[:-4])
			dic_count[c_tmp]+=1
	    else:
		pass

    dic_count_sorted=sorted(dic_count.items(),key=lambda x:x[1],reverse=True)

    O_base='.././Data/Key_Info/'
    sub_s_f='Sub_Clust.list.'+str(list_count)+'txt'
    path_file=os.path.join(O_base,sub_s_f)
    fp_for_sub=open(path_file,'w')

    l_count=0 
    
    #print dic_id

    for ele in dic_count_sorted:
        tmp_str=ele[0]+'\t'
        #print ele[0]
        #print dic_id[ele[0]]
        #c_ids='\t'.join(dic_id[ele[0]])

        c_id_list=dic_id[ele[0]]
        tmp_c_str=ele[0]+'\t'
        for ac_id in c_id_list:
            tmp_c_str=tmp_c_str+ac_id+':'+AFile_dic[ac_id]+'\t'
        #print tmp_c_str
        #print c_ids
        tmp_c_str=tmp_c_str.strip()
        tmp_c_str=tmp_c_str+'\n'
        #tmp_str=tmp_str+c_ids+'\n'
        fp_for_sub.write(tmp_c_str)
        l_count+=1
        if l_count==10:
            break
    fp_for_sub.close()

    #print dic_count
    #print dic_id
    print '\n### Ending to find common Keys at ',list_count,'th list#\n\n'
    print '!!!The result file is located in ./Data/1D_Out/Sub_Cluster!!!\n\n'
    print('key length : ', ln_key)
    print('Num of compounds : ', len(set(files)))
    print('Num of Keys : ' ,len(dic_count.keys()))
    print(dic_count_sorted)
    print('\n')
    print('****************************************************************')

    
    T_base='.././Data/Table'
    T_file='Result_0.dat'
    path_file=os.path.join(T_base,T_file)
    ouf=open(path_file,'wb')
    #print dic_count_sorted
    marshal.dump(dic_count_sorted,ouf)
    ouf.close()



def find_key(length):

    time_sp1=time.time()

    #print len(sys.argv)
    #sys.exit(1)

    print '\n### Starting Reading files ###\n'
    print 'Reading key lib.........'
    ln_key=int(sys.argv[1])

    print 'The Key length is ',ln_key,'\n' 
    if ln_key==4:
        Key_dic=Read_lib('1D_key_lib_4_m.dat')
    if ln_key==5:
        Key_dic=Read_lib('1D_key_lib_5_m.dat')
    if ln_key==6:
        Key_dic=Read_lib('1D_key_lib_6_m.dat')


    #print Key_dic.keys()
    #return

    #print 'Reading key lib.........'
    #Key_dic=Read_lib('1D_key_lib_5.pickle')
    print 'Reading A file lib......'
    AFile_dic=Read_lib('1D_lib_F.ADP_m.dat')

    #return

    l_list=[]

    if len(sys.argv)==2:
        c_path=os.getcwd()
        Input_files_path='.././Data/Input/'
        os.chdir(Input_files_path)
        listOfFiles= filter(os.path.isfile, os.listdir(os.getcwd()))
        files = [fi for fi in listOfFiles if fi.endswith('.sdf')]
        os.chdir(c_path)
        #print files
        if len(files)==0:
            print 'locate the ligand file in ./Data/Input folder!'
            return
        l_list.append(files)

    if len(sys.argv)==3:
        l_list=[]
        tmp_list=[]
        fp_for_in=open(sys.argv[2])
        while(1):
            line=fp_for_in.readline()
            if(line==''):
                l_list.append(tmp_list)
                #print 'Done!\n'
                break
            else:
                if line.startswith('$$$'):
                    l_list.append(tmp_list)
                    #print len(tmp_list)
                    tmp_list=[]
                else:
                    line=line.strip()
                    tmp_list.append(line)
    #print l_list
    #return

    list_count=1
    #print l_list
    #return
    for alist in l_list:
        #print alist
        make_dic(Key_dic,AFile_dic,list_count,alist)
        list_count+=1

    time_sp2=time.time()
    print '\nProcessing the 1DScan with keys: '+str(time_sp2-time_sp1)+'\n'

def main():

    #python prog. key_length: ex python Key_gen.py 5

    length = sys.argv[1]
    find_key(length)

if __name__=="__main__":
    main()
