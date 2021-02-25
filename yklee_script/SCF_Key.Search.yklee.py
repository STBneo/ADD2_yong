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

def Key_dic_load():
    didi = {}
    #with open('./Data/Table/Result_0.dat','r') as F:
    with open('./Result_FLT3_input.dat','rb') as F:
        for i in marshal.load(F):
            didi[i[0]]= i[1]
    print("input Template Key Load OK")
    return didi
def pos_Key_load():
    didi = {}
    #with open('Result_CDK7_positive.dat','r') as F:
    #with open('Result_EGFR_positive.dat','r') as F:
    with open('Result_FLT3_positive.dat','rb') as F:
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
def divide_list(ls):
    n = 10000000
    for i in range(0,len(ls),n):
        yield ls[i:i+n]
def find_zid(con,alp):
    cursorObj = con.cursor()
    query = 'SELECT * FROM Key_Table WHERE Key=\'%s\''%(alp)
    cursorObj.execute(query)
    rows = cursorObj.fetchall()
    cursorObj.close()
    if not rows:
        pass
    else:
        ppp = unicode.encode(rows[0][1],'utf-8')
        p_set = set(ppp.split(','))
        print("Find Key %s ID set OK"%alp)
        return p_set

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

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('-top_p',required=True, default=100, help='Select the top X percent of Key frequency.')
    parser.add_argument('-mins',required=True, default=1, help='The minimum number of Key.')
    args=parser.parse_args()

    con = sql_connection_K()
    key_dic = Key_dic_load()
    pos_key = pos_Key_load() 
    print('Key Intersection')
    print(set(key_dic.keys())&set(pos_key.keys()))
    scf_list = SCF_result_load()
    scf_list = list(divide_list(scf_list))
    print(len(scf_list))
    Ncpu = multiprocessing.cpu_count()
    Key_dics = Manager().dict()
    tset = set()
    mlist = Manager().list()
    global tset
    df_list = []
    df_list2 = []
    a = 0
    try:
        if os.path.exists('SCF_KEY_search'):
            os.chdir('SCF_KEY_search')
        else:
            os.mkdir('SCF_KEY_search')
            os.chdir('SCF_KEY_search')
    except:
        print('Error')
    for i in key_dic.keys():
        id_set = find_zid(con,i)
        tset = tset|id_set
    for lili in scf_list:
        a += 1
        pool = multiprocessing.Pool(Ncpu-4)
        func = partial(SCF_to_Key,mlist=mlist)
        pool.map(func,lili)
        pool.close()
        pool.join()
        with open('tmp_%s.txt'%(str(a)),'w') as W:
            for line in mlist:
                W.write(line + '\n')
    tset.clear()
    mlist.Manager().dict()
    for i in sorted(glob.glob('tmp_*.txt')):
        df = pd.read_csv(i,header=None)
        df_list.append(df)
    df1 = pd.concat(df_list)
    for i in sorted(df1[0].drop_duplicates()):
        df2 = dropop(df1,i)
        df_list2.append(df2)
    df_fin = pd.concat(df_list2)
    df_fin.to_csv('SK_result.csv',index=False)
