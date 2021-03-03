import os, sys, glob, subprocess, apsw, itertools,argparse,multiprocessing,marshal,sqlite3,time
from multiprocessing import Process, Manager
from functools import partial
import pandas as pd
from sqlite3 import Error

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
    with open('./Data/Table/Result_0.dat','rb') as F:
        for i in marshal.load(F):
            didi[i[0]]= i[1]
    print("input Template Key Load OK")
    return didi

def find_zid(alp):
    cursorObj = conK.cursor()
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

def SK_search():
    Ncpu = multiprocessing.cpu_count()
    mlist = Manager().list()
    b = 0
    with open('../../1D_Out_SCF/SCF_Out.list.Per.SMILES.txt','r') as F:
        flines = F.readlines()
        len_d = len(flines)//10
        div_list = list(divide_list(flines,len_d))
        for li in div_list:
            b += 1
            print('Checking ID START Step %s by multiprocessing'%str(b))
            func = partial(check_intersection,mlist=mlist)
            pool = multiprocessing.Pool(Ncpu-2)
            pool.map(func,li)
            pool.close()
            pool.join()
            print('Checking ID END Step %s'%str(b))
            with open('result_%s.txt'%str(b),'w') as W:
                for line2 in mlist:
                    W.write(line2 + '\n')
            mlist = Manager().list()


def check_intersection(line,mlist):
    tline = line.strip().split(',')
    zid = tline[2]
    if zid in tset:
        mlist.append(','.join(tline))
    else:
        pass

def dropop(df,i):
    df1 = df[df[0] == i]
    df2 = df1.drop_duplicates()
    return df2

def make_dir(a):
    try:
        print('Checking Directory')
        if os.path.exists(a):
            os.chdir(a)
            pass
        else:
            os.makedirs(a)
            os.chdir(a)
    except:
        print('DIR CREATE ERROR')

def divide_list(ls,n):
    for i in range(0,len(ls),n):
        yield ls[i:i+n]

def make_complete_file():
    print('Integration Files')
    df_list = []
    for i in glob.glob('result_*.txt'):
        df = pd.read_csv(i,header=None)
        df_list.append(df)
    df1 = pd.concat(df_list)
    df_list[:] = []
    for i in sorted(df1[0].drop_duplicates()):
        df2 = dropop(df1,i)
        df_list.append(df2)
    df_fin = pd.concat(df_list)
    df_fin.to_csv('SK_result.csv',index=False)
    print('Completely make SK_result.csv')

if __name__ == "__main__":
    print('Scaffold - Key Search START')
    conK = sql_connection_K()
    key_dic = Key_dic_load()

    Key_dics = Manager().dict()
    mlist = Manager().list()
    tset = set()
    df_list = []

    global conK,tset


    make_dir('./Data/SKR_Out/SK_result')
    print('N. Of Keys : ' + str(len(key_dic.keys())))
    for i in key_dic.keys():
        id_set = find_zid(i)
        tset = tset|id_set

    SK_search()
    make_complete_file()
    os.chdir('../../../')
    print('Scaffold - Key Search END')
