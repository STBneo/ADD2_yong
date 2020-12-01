import sys,os
import glob
import StringIO
import zipfile
import pickle
import marshal
import sqlite3
from sqlite3 import Error
import apsw
from time import time
from datetime import datetime

def print_date_time():
    now = datetime.now()
    w=datetime.now()
    dt_string=now.strftime("%d/%m/%Y %H:%M:%S")
    print dt_string

def read():
    os.system('rm -r ../Data/FDA')
    os.system('mkdir ../Data/FDA')
    os.system('mkdir ../Data/FDA/PASS')
   
    fw = open('../Data/FDA/ID_FDA.txt','w')
    sdf_path = '../Data/Dic_Lib_Output_SDF_RAW_10/'
    for i in range(1,9):
        R = str(i)+'R'
        print(R)
        print_date_time()
        sdf_ls = os.listdir(sdf_path+R)
    
        for sdf in sdf_ls:
            zid = sdf[:-4]
            row = sql_fetch(zid)
            if str(row) == 'None':
                row = -1
            fw.write(zid+'\t'+str(row)+'\n')

            if float(row) >= 0.5:
                os.system('cp '+sdf_path+R+'/'+sdf+' ../Data/FDA/PASS')
    fw.close()

def sql_fetch(zid):
    try:
        con = sqlite3.connect('../Data/DB_Table/ZINC_FDA.db')
    except:
        print('Failed')
    con.text_factory = str
    cursorObj = con.cursor()
    
    #zid = 'ZINC000034979053'
    cursorObj.execute('SELECT Info FROM FDA WHERE Zid = ?',(zid,))
    #cursorObj.execute('SELECT Zid, Info FROM FDA WHERE Zid = ?',(zid,))
    #cursorObj.execute('SELECT * FROM FDA')
    #print(cursorObj.fetchone())

    rows = cursorObj.fetchall()
    #print(len(rows))
    for row in rows:
        #print(row[0])
        #sys.exit(1)
        return row[0]

def main():
    print('Start')
    print_date_time()
    read()
    print('End')
    print_date_time()

if __name__ == '__main__':
    main()
