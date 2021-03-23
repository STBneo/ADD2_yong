import os, sys, glob, subprocess, apsw, itertools,argparse
import multiprocessing
from multiprocessing import Process, Manager
from functools import partial
import pandas as pd
from sqlite3 import Error
import sqlite3
import time
from datetime import datetime
import marshal
def pos_dic():
    temp_dic = {'CDK7': ['ZINC000000101319', 'ZINC000077485665', 'ZINC000004192450', 'ZINC000033278339', 'ZINC000467398634','ZINC000095526640'], \
    'FLT3':['ZINC000000008662', 'ZINC000058014319', 'ZINC000005814210', 'ZINC000006448596','ZINC000012322830', 'ZINC000096221013', \
    'ZINC000100498577', 'ZINC000013126934', 'ZINC000000575002', 'ZINC000009245306','ZINC000013148149', 'ZINC000217901089', \
    'ZINC000000057655', 'ZINC000000210268', 'ZINC000023334750', 'ZINC000000248216','ZINC000001001156', 'ZINC000000435149', \
    'ZINC000006508912', 'ZINC000015843244', 'ZINC000021114661', 'ZINC000057964036','ZINC000004137279', 'ZINC000019702144', \
    'ZINC000079020838', 'ZINC000000111962', 'ZINC000078733090', 'ZINC000075144163','ZINC000097201518', 'ZINC000065272148', \
    'ZINC000072404457', 'ZINC000085391937', 'ZINC000001075920', 'ZINC000000060207','ZINC000075544404'], \
    'EGFR':['ZINC000001076595', 'ZINC000217912735', 'ZINC000085877625', 'ZINC000020827506', 'ZINC000217901089','ZINC000001068379', \
    'ZINC000009281884', 'ZINC000249700260', 'ZINC000009059860'], \
    'ERBB4':['ZINC000096396694', 'ZINC000032751234', 'ZINC000101747211', 'ZINC000089977150', 'ZINC000033260731','ZINC000072333497']}
    return temp_dic


def sql_connection_K():
    try :
        con = apsw.Connection('./Data/DB_Table/ZINC_K.db')
        return con
    except Error:
        print(Error)
        sys.exit(1)
        return
def sql_connection_IDK():
    try:
        #con = sqlite3.connect('./Data/DB_Table/ZINC_IDK.db')
        con = sqlite3.connect('./Data/DB_Table/test_IDK.db')
        return con
    except Error:
        sys.exit(1)
        return
'''
def Key_dic_load():
    didi = {}
    with open('./Data/Table/Result_0.dat','r') as F:
    #with open('./Result_EGFR_input.dat','rb') as F:
        for i in marshal.load(F):
            didi[i[0]]= i[1]
    print("input Template Key Load OK")
    return didi
'''
def Key_dic_load():
    print(os.getcwd())
    k_set = set()
    a = 0
    with open('./Tools/Input_Key_Statistics/Activate_Input.csv','r') as F:
        for line in F.readlines():
            tline = line.strip().split(',')
            a += 1
            if a == 1:
                pass
            else:
                k_set.add(tline[0])
    return k_set

def pos_Key_load():
    didi = {}
    #with open('Result_CDK7_positive.dat','r') as F:
    with open('Result_EGFR_positive.dat','r') as F:
    #with open('Result_FLT3_positive.dat','rb') as F:
        for i in marshal.load(F):
            print(i[0])
            didi[i[0]] = i[1]
    print("Positive Key Load OK")
    return didi
def SCF_result_load():
    lili = []
    #with open('./Data/1D_Out_SCF/SCF_Out.list.Per.SMILES.txt','r') as F:
    with open('./Data/FLT3_input_Temp_SCF/SCF_Out.list.Per.SMILES.txt','r') as F:
        for line in F.readlines():
            lili.append(line.strip())

    print("SCF results Load OK")
    return lili

def SCF_result_analysis(mlist):
    Ncpu = multiprocessing.cpu_count()

    with open('../Data/EGFR_SCF/SCF_Out.list.Per.SMILES.txt','r') as F:
        a = 0
        b = 0
        flines = F.readlines()
        lend = len(flines)//50
        print(lend)
        lili = list(divide_list(flines,lend))
        print('''
        ####################
          Total Step %s
        ####################'''%(str(len(lili))))
        for li in lili:
            b += 1
            print('''
        ####################
             Step %s/%s
        ####################'''%(str(b),str(len(lili))))
            pool = multiprocessing.Pool(Ncpu-2)
            pool.map(find_zid_IDK,li)
            pool.close()
            pool.join()
            print(len(mlist))
            with open('result_%s.txt'%str(b),'w') as W:
                for line2 in mlist:
                    W.write(line2 + '\n')
            mlist = Manager().list()
            a = 0
            if b == 1:
                break

def SCF_result_analysis_core(li,k_set):
    t_set = Key_dics[li][0]
    tline = ','.join(Key_dics[li][1])
    if not t_set:
        pass
    else:
        ppp = t_set&k_set
        if not ppp:
            pass
        else:
            mlist.append(tline)

def divide_list(ls,n):
    for i in range(0,len(ls),n):
        yield ls[i:i+n]
def find_zid(con,alp):
    con = sql_connection_IDK()
    cursorObj = con.cursor()
    query = 'SELECT * FROM Key_Table WHERE Key=\'%s\''%(alp)
    cursorObj.execute(query)
    rows = cursorObj.fetchall()
    cursorObj.close()
    con.close()
    if not rows:
        pass
    else:
        ppp = unicode.encode(rows[0][1],'utf-8')
        p_set = set(ppp.split(','))
        print("Find Key %s ID set OK"%alp)
        return p_set
def check_intersection(line,mlist):
    tline = line.strip().split(',')
    alp = tline[2]
    try :
        con = sqlite3.connect('../..//DB_Table/ZINC_IDK.db')
    except:
        sys.exit(1)

    try :
        cursorObj=con.cursor()
    except:
        sys.exit(1)
    query = "SELECT * FROM IDK_Table WHERE Zid=\'%s\'"%(alp)
    cursorObj.execute(query)
    rows = cursorObj.fetchall()
    if not rows:
        pass
    else:
        ppp = unicode.encode(rows[0][1],'utf-8')
        p_set = set(ppp.split(','))
        if not p_set:
            pass
        else:
            t_set = p_set&k_set
            if not t_set:
                pass
            else:
                mlist.append(','.join(tline))

def SCF_to_Key(zid,mlist) : 
    zzid = zid.split(',')[2]
    if zzid in tset:
        mlist.append(zid)
    else:
        pass
def dropop(df,i):
    df1 = df[df[0] == i]
    df2 = df1.drop_duplicates()
    return df2
def make_directory(a):
    try:
        if os.path.exists(a):
            os.chdir(a)
        else:
            os.mkdir(a)
            os.chdir(a)
    except:
        print('DIR make Error')

def ZINC_IDK_search():
    Ncpu = multiprocessing.cpu_count()
    mlist = Manager().list()
    b = 0
    with open('../../1D_Out_SCF/SCF_Out.list.Per.SMILES.txt','r') as F:
        flines = F.readlines()
        #flines = flines[:]
        len_d = len(flines)//10
        div_list = list(divide_list(flines,len_d))
        print(len_d)
        for li in div_list:
            b += 1
            print(b)
            pool = multiprocessing.Pool(Ncpu-2)
            func = partial(check_intersection,mlist=mlist)
            pool.map(func,li)
            pool.close()
            pool.join()
            print('count line')
            print(len(mlist))

            with open('result_%s.txt'%str(b),'w') as W:
                for line2 in mlist:
                    W.write(line2 + '\n')
            del mlist
            mlist = Manager().list()

if __name__ == "__main__":
    k_set = Key_dic_load()
    Ncpu = multiprocessing.cpu_count()
    df_list = []
    df_list2 = []
    #k_set = set(key_dic.keys())
    print(k_set)
    global k_set
    make_directory('./Data/SKR_Out/SK_result')
    ZINC_IDK_search()
    print(os.getcwd())
    for i in glob.glob('result_*.txt'):
        try:
            df = pd.read_csv(i,header=None)
            df_list.append(df)
        except:
            pass
    df1 = pd.concat(df_list)
    for i in sorted(df1[0].drop_duplicates()):
        df2 = dropop(df1,i)
        df_list2.append(df2)
    df_fin = pd.concat(df_list2)
    df_fin.to_csv('SK_result.csv',index=False)
