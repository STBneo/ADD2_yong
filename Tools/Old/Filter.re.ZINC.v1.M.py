import itertools
import os,sys
import pandas as pd
import random
import pickle
import marshal
from time import time

# Scoring the result file

def Search_Dir():

    time1=time()
    T_base='../Data'
    print '\nStarting Post-procssing for all round.....'
    arg='rm ../Data/Dic_Lib_Input/*'
    os.system(arg)

    for(path, adir, files) in os.walk(T_base):
        #print adir
        #print path
        #print files
        if(path.endswith('R') and path.startswith('../Data/1D_Out_')):
            token=path.split('_')
            print ' Starting post-procssing....: '+token[-1]
            print '  '+path
            #'''
            #print token[-1]
            #sys.exit(1)
            arg='cat '+path+'/*.frq.* > '+path+'/All.f.csv'
            os.system(arg)
            #sys.exit(1)
            arg='sort -k1 -t\',\' '+path+'/All.f.csv > '+path+'/All.f.s1.csv'
            os.system(arg)
            #sys.exit(1)
            f_name='All.f.s1.csv'
            path_file=os.path.join(path,f_name)
            Filter_Re_File(path_file)
            arg='sort -k2nr -t\',\' '+path+'/All.f.s1.f.csv > '+path+'/All.f.final_re.'+token[-1]+'.csv'
            os.system(arg)
            #arg='head -3500 '+path+'/All.f.final_re.'+token[-1]+'.csv > A.csv'
            arg='head -10000 '+path+'/All.f.final_re.'+token[-1]+'.csv > A.csv'
            os.system(arg)
            arg='mv A.csv '+path+'/All.f.final_re.'+token[-1]+'.csv'
            os.system(arg)
            arg='cp '+path+'/All.f.final_re.'+token[-1]+'.csv ../Data/Dic_Lib_Input '
            os.system(arg)
            arg='rm '+path+'/All.f.s1.f.csv '+path+'/All.f.csv'
            os.system(arg)
            print ' Ending post-procssing......: '+token[-1]+'\n'
            #'''
            #sys.exit(1)

    time2=time()
    print '\nEnding postprocessing result_files.'
    #print 'The location of a key file is \'../input.key.m.list.txt\'.'
    print 'The Post processing time of result files: '+str(time2-time1)+'\n\n'


def Filter_Re_File(path_file):

    #fp_for_in=open('./1D_Out/All.f.s1.csv','r')
    #fp_for_out=open('./1D_Out/All.f.s1.f.csv','w')

    #print path_file[0:-3]+'f.csv'
    path_file_out=path_file[0:-3]+'f.csv'
    
    fp_for_in=open(path_file,'r')
    fp_for_out=open(path_file_out,'w')

    lines=fp_for_in.readlines()
    #print len(lines)
    ln_line=len(lines)
    line_count=0
    while(line_count<ln_line-1):
        if(lines[line_count].startswith('ZINC_ID')):
            fp_for_out.write(lines[line_count])
            break
        line_c=lines[line_count].strip()
        token_c=line_c.split(',')
        line_n=lines[line_count+1].strip()
        token_n=line_n.split(',')

        #print line_c

        if(token_c[0]!=token_n[0]):
            score=1+int(token_c[2])+int(token_c[4])
            fp_for_out.write(token_c[0]+','+str(score)+'\n')
            #print token_c[0],score
            line_count+=1
        else:
            same_count=1
            ZINC_id_c=token_c[0]
            main_key_frq=int(token_c[2])
            sub_key_frq=int(token_c[4])
            s_flag=1
            #print line_count,line_c,'1'
            #print main_key_frq,sub_key_frq
            while(s_flag):
                #print line_count
                line_count+=1
                line=lines[line_count].strip()
                token=line.split(',')
                #print line_count,line
                #print token[2],token[4]
                if(ZINC_id_c==token[0]):
                    #print line_count,line
                    #print token[2],token[4]
                    main_key_frq=main_key_frq+int(token[2])
                    sub_key_frq=sub_key_frq+int(token[4])
                    same_count+=1
                    #print main_key_frq,sub_key_frq
                else:
                    score=main_key_frq+sub_key_frq+same_count
                    fp_for_out.write(ZINC_id_c+','+str(score)+'\n')
                    #print line
                    #print token[2],token[4]
                    #print ZINC_id_c,score
                    s_flag=0
                    line_count-=1
    fp_for_in.close()
    fp_for_out.close()

def Read_lib(lib_file):
    l_base='./Data/Lib'

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

    O_base='./Data/1D_Out/'
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
        Input_files_path='./Data/Input/'
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

    Search_Dir()
    #Filter_Re_File()

if __name__=="__main__":
    main()
