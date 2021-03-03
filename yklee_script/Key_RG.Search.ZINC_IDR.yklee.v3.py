import os,sys,glob,subprocess,apsw,itertools,argparse,marshal
import multiprocessing
from multiprocessing import Manager,Process
from functools import partial
import pandas as pd
from sqlite3 import Error
import sqlite3
import time
from datetime import datetime

def load_FG2():
    with open('FG_combination.code.yklee.marshal','rb') as F:
        didi = marshal.load(F)
    return didi

def sql_connection_IDR():
    try:
        con = apsw.Connection('./Data/DB_Table/ZINC_IDR.db')
        return con
    except Error:
        print(Error)
        sys.exit(1)
        return

def divide_list(ls,n):
    for i in range(0,len(ls),n):
        yield ls[i:i+n]

def find_zid_IDR(alp):
    query = "SELECT * FROM IDR_Table WHERE zid=?"
    conIDRcursor.execute(query,(alp,))
    rows = conIDRcursor.fetchall()
    if not rows:
        pass
    else:
        ppp = unicode.encode(rows[0][1],'utf-8')
        p_set = set(ppp.split(','))
        return p_set

def change_FG_code():
    FG2_dic = load_FG2()
    k_set = set()
    a = 0
    with open('./Tools/Input_RG_Statistics/Activate_Input.csv','r') as F:
        for line in F.readlines():
            tline = line.strip().split(',')
            a +=1
            if a == 1:
                pass
            else:
                if not tline[0] in FG2_dic.keys():
                    pass
                else:
                   k_set.add(FG2_dic[tline[0]])
    return k_set

def check_intersection(alp,mlist):
    p_set = Key_dics[alp][0]
    ttline = Key_dics[alp][1]
    if not p_set:
        pass
    else:
        t_set = k_set & p_set
        if not t_set:
            pass
        else:
            mlist.append(ttline)

def Key_RG_search():
    print(os.getcwd())
    Ncpu = multiprocessing.cpu_count()
    mlist = Manager().list()
    b = 0
    with open('../SK_result/SK_result.csv','r') as F:
        flines = F.readlines()
        len_d = len(flines)//10
        div_list = list(divide_list(flines,len_d))
        for li in div_list:
            b +=1

            for line in li:
                tline = line.strip().split(',')
                zid = tline[2]
                p_set = find_zid_IDR(zid)
                Key_dics[zid] = [p_set,','.join(tline)]
            print('Checking ID START Step %s'%str(b))
            pool = multiprocessing.Pool(Ncpu-2)
            func = partial(check_intersection,mlist=mlist)
            pool.map(func,Key_dics.keys())
            pool.close()
            pool.join()
            print('Checking ID END Step %s'%str(b))
            with open('result_%s.txt'%str(b),'w') as W:
                for line2 in mlist:
                    W.write(line2 + '\n')
            mlist = Manager().list()
            Key_dics.clear()

def make_complete_file():
    print('Make Integration File')
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
    df_fin.to_csv('SKR_result.csv',index=False)
    print('Completely make SKR_result.csv')

def make_dir(a):
    try:
        print('Checking Directory')
        if os.path.exists(a):
            os.chdir(a)
            pass
        else:
            os.mkdir(a)
            os.chdir(a)
    except:
        os.mkdir(a)
        os.chdir(a)
        print('DIR CREATE ERROR')

def dropop(df,i):
    df1 = df[df[0] ==i]
    df2 = df1.drop_duplicates()
    return df2

if __name__ == "__main__":
    print('Key - R Group Search START')
    con = sql_connection_IDR()
    conIDRcursor = con.cursor()
    k_set = change_FG_code()
    Key_dics = Manager().dict()
    global conIDRcursor,k_set,Key_dics
    make_dir('./Data/SKR_Out/SKR_result')
    Key_RG_search()
    make_complete_file()
    print('Key - R Group Search END')