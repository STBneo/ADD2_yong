import os,sys,glob,subprocess,apsw
import multiprocessing
from multiprocessing import Manager,Process
from functools import partial
import pandas as pd
from sqlite3 import Error
import sqlite3
import time
from datetime import datetime

def sql_connection():
    try :
        con = apsw.Connection('./final_inte.db')
        return con
    except Error:
        print(Error)

def read_list(a):
    df = pd.read_csv(a,sep='\t')
    df[0] = 1
    return df['zinc_id']

def DB_work():
    con = sql_connection()
    cursorObj = con.cursor()
    query = cursorObj.execute("SELECT * FROM R_Table")
    cols = [column[0] for column in query.description]
    df = pd.DataFrame.from_records(data=query.fetchall(),columns=cols)
    con.close()
    dd = df.set_index('Rgroup').to_dict('dict')
    return dd['ZID']

def working(dict1,zids,dio):
    for i in dict1.keys()[:2]:
        list2set = set(dict1[i].split(','))
        Ncpu = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(Ncpu-1)
        func = partial(drop_id2,list2set)
        pool.map(func,zids)
        pool.close()
        pool.join()
        dio[i] = list(list2set)

def drop_id2(list2set,zid):
    if id in list2set:
        list2set.remove(zid)
        print('remove %s'%id)
    else:
        pass

def multi_work(dict1,zids):
    Ncpu = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(Ncpu-1)

    func = partial(drop_id,dict1,zids)
    pool.map(func,dict1.keys())
    pool.close()
    pool.join()

if __name__ == "__main__":
    zids = read_list('id_023_needs.txt')
    print(len(zids))
    didi = DB_work()
    dio = Manager().dict()

    working(didi,zids,dio)
    print(dio)
    fdf = pd.DataFrame.from_dict(dio,orient='index').reset_index().rename(columns={'index':'Rgroup'})
    con = sqlite3.connect('./temp.db')
    fdf.to_sql('R_Table',con,index=False)
    fdf.to_pickle('./tmp.pkl')
    print(fdf)

