import itertools
import os,sys
import pandas as pd
import random
import time
import pickle
import marshal
import argparse
import sqlite3
from sqlite3 import Error
import apsw


## for DB_F
def sql_connection_F():
    try:
        con = apsw.Connection('../Data/DB_Table/ZINC_F.db')
        return con
    except Error:
        print(Error)
    return


def sql_table_F(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE F_Table(Zid txt PRIMARY KEY, feature text)")
    #con.commit()
    return 


def sql_insert_F(con, entities):
    global du_count
    cursorObj = con.cursor()
    try:
        cursorObj.execute('INSERT INTO F_Table(Zid, feature) VALUES(?, ?)', entities)
    except apsw.ConstraintError:
        #print entities
        du_count+=1
    #con.commit()
    return


def sql_fetch_F(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM F_Table')
    rows = cursorObj.fetchall()
    for row in rows:
        print(row)

    print len(rows)
    return


def sql_search_F(con,Zid):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT Zid,feature FROM F_Table where Zid=?',(Zid,))
    rows = cursorObj.fetchall()
    return rows[0][1]
    

## for DB_K
def sql_connection_K():
    try:
        con = apsw.Connection('../Data/DB_Table/ZINC_K.db')
        return con
    except Error:
        print(Error)
    return


def sql_connection_SK():
    try:
        con = apsw.Connection('../Data/DB_Table/Seed_K.db')
        return con
    except Error:
        print(Error)
    return


def sql_table_K(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE Key_Table(Key txt PRIMARY KEY, ids text")
    #con.commit()
    return


def sql_insert_K(con, entities):
    global du_count
    cursorObj = con.cursor()
    try:
        cursorObj.execute('INSERT INTO Key_Table(Key, ids) VALUES(?, ?)', entities)
    except apsw.ConstraintError:
        #print entities
        du_count+=1
    #con.commit()
    return


def sql_update_K(con,akey,tmp_list):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT Key, ids  FROM Key_Table where Key=?',(akey,))
    rows = cursorObj.fetchall()
    tmp2_list=list(set(tmp_list))
    zids=','.join(tmp2_list)
    zids=rows[0][1]+','+zids
    zkey=akey
    
    try:
        cursorObj.execute('UPDATE Key_Table SET ids=? WHERE Key=?',(zids,zkey,))
    except apsw.ConstraintError as e:
        print e
    #con.commit()
    return


def sql_fetch_K(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM Key_Table')
    rows = cursorObj.fetchall()
    for row in rows:
        print(row)
    print len(rows)
    return


def sql_remove_reduant_ids_K(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM Key_Table')
    rows = cursorObj.fetchall()
    for row in rows:
        #print row[0],row[1]
        zkey=row[0]
        db_list=row[1].split(',')
        #db_list=list(set(db_list))
        db_list=set(db_list)
        #print db_list 
        zids=','.join(db_list)
        #print zids
        try:
            cursorObj.execute('UPDATE Key_Table SET ids=? WHERE Key=?',(zids,zkey,))
        except apsw.ConstraintError as e:
            print e
    #print len(rows)
    return


def sql_check_pattern_K(con,akey):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT Key, ids  FROM Key_Table where Key=?',(akey,))
    rows = cursorObj.fetchall()
    ln_key=len(rows)
    return


def sql_connection_SF():
    print(os.getcwd())
    try:
        con = apsw.Connection('./Data/DB_Table/Seed_F.db')
        return con
    except Error:
        print(Error)
    return


def sql_search_SF(con,Zid):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT Zid,feature FROM SF_Table where Zid=?',(Zid,))
    rows = cursorObj.fetchall()
    return rows[0][1]


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


def make_dic(con_F,list_count,files):

    ln_key=int(sys.argv[1])
    item=['A','D','P']
    candidate=list(map(''.join,itertools.product(item,repeat=ln_key)))

    dic_count={}
    dic_id={}

    for afile in files:
        #Test code#
        #print afile
        #sys.exit(1)

        # In case of seed, use the full name of seed including extention
        feat=sql_search_SF(con_F,afile[:-4])

        # Show result 
        print afile,feat,len(feat)
        #sys.exit(1)
        
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
            feat=sql_search_SF(con_F,afile[:-4])
            tmp_c_str=tmp_c_str+ac_id+':'+feat+'\t'
            #tmp_c_str=tmp_c_str+ac_id+':'+AFile_dic[ac_id]+'\t'
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

    fw = open('Result_1.dat', 'a')
    #print(str(list_count)+'\t'+str(len(set(files)))+'\t'+str(dic_count_sorted[0:5])+'\n')
    fw.write(str(list_count)+'\t'+str(len(set(files)))+'\t'+str(dic_count_sorted[0:5]).replace('[','').replace(']','').replace('), (',')\t(')+'\n')
    fw.close()

def find_key(length):

    time_sp1=time.time()

    print 'Connecting the DB file.....'
    #con_K=sql_connection_K()
    con_SF=sql_connection_SF()

    ln_key=int(sys.argv[1])
    print 'The Key length is ',ln_key,'\n'

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

    list_count=1
    #print l_list
    #return
    for alist in l_list:
        #print alist
        make_dic(con_SF,list_count,alist)
        list_count+=1

    time_sp2=time.time()
    print '\nProcessing the 1DScan with keys: '+str(time_sp2-time_sp1)+'\n'

def main():

    #python prog. key_length: ex python Key_gen.py 5
    #os.system('rm Result_1.dat')
    length = sys.argv[1]
    find_key(length)

if __name__=="__main__":
    main()
