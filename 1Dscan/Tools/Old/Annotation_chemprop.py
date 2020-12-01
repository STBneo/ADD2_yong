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

def read():
    os.system('rm -r ../Data/Annotation/SDF')
    os.system('mkdir ../Data/Annotation/SDF')
    os.system('mv ../Data/Annotation/*.sdf ../Data/Annotation/SDF')
    fr = open('../Data/Annotation/results.table.id','r')
    fw = open('../Data/Annotation/results.table.FDA.id','w')
    while True:
        line = fr.readline()
        if line == '': pass
        else:
            fw.write(line.rstrip()+'\tFDAdrug\n')

        if not line: break
        
        while True:
            line = fr.readline()
            if line == '': pass
            else:
                zid = line.split('\t')[0]
                #print(zid)
                row = sql_fetch(zid)
                fw.write(line.rstrip()+'\t'+str(row)+'\n')
                #print(line)
                #sys.exit(1)

            if not line: break

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
    read()

if __name__ == '__main__':
    main()

