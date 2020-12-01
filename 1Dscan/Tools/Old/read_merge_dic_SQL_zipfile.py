import os, sys
import StringIO
import zipfile
import pickle
import marshal
#import lzma
#from backports import lzma
import sqlite3
from sqlite3 import Error
import apsw
from time import time
import multiprocessing
from functools import partial

def sql_fetch(R, zid):
    #print(R, zid)
    con = sqlite3.connect('../Data/DB_Table/ZINC_S.db')
    con.text_factory = str
    cursorObj = con.cursor()
    
    try:
        cursorObj.execute('SELECT Sdf FROM Sdf_Files WHERE Zid = ?', [zid]) 
        #print(cursorObj.fetchone())
   
        sdf_path = '../Data/Dic_Lib_Output_SDF/'+R+'/'
        fw = open(sdf_path+zid+'.zip', 'w')
        fw.writelines(cursorObj.fetchone())
        fw.close()

        os.system('unzip '+sdf_path+zid+'.zip -d '+sdf_path)
        os.system('rm '+sdf_path+zid+'.zip')
        os.system('mv '+sdf_path+'In*'+zid+'.txt '+sdf_path+zid+'.sdf')
    
    except:
        pass

zid_files_path = '../Data/Dic_Lib_Input/'
zid_files = os.listdir(zid_files_path)
#zid_check_ls = []
for zid_file in zid_files:
    R = zid_file.split('.')[3]
    os.system('rm -r ../Data/Dic_Lib_Output_SDF/'+R)
    os.system('mkdir -p ../Data/Dic_Lib_Output_SDF/'+R)
    zid_ls = []
    fr = open(zid_files_path+zid_file, 'r')
    while True:
        line = fr.readline()
        zid = line.split(',')[0]
        #print(type(zid))
        zid = 'ZINC00' + zid
        if len(zid) >= 14 and zid not in zid_ls:
            #zid_check_ls.append(zid)
            zid_ls.append(zid)
        if not line: break
    fr.close()

    n_cpu = multiprocessing.cpu_count()-1
    pool = multiprocessing.Pool(processes=n_cpu)
    func = partial(sql_fetch, R)
    pool.map(func, zid_ls)
    pool.close()
    pool.join()
