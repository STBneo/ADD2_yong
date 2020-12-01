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
import multiprocessing
from functools import partial

def print_date_time():
	now = datetime.now()
	w=datetime.now()
	dt_string=now.strftime("%d/%m/%Y %H:%M:%S")
	print dt_string

def copy_All(sdf_path,R,sdf):
    os.system('cp '+sdf_path+R+sdf+' ../Data/Dic_Lib_Output_SDF/All')

def write(path,DB_path,sdf_ls):
    fw = open(path+'results.table.id','w')
    fw.write('ID,MW,LogP,PSA,RotatableB,RigidB,HBD,HBA,Rings,MaxSizeRing,Charge,Total_Charge,HeavyAtoms,CarbonAtoms,HeteroAtoms,ratioH_C,Lipinski_Violation,Veber_Violation,Egan_Violation,Functionnal_Group,Toxicity'.replace(',','\t')+'\tFDA\n')

    for sdf in sdf_ls:
        zid = sdf[:-4]
        rows_FAF = sql_fetch_FAF(DB_path,zid)
        row_chemprop = sql_fetch_chemprop(DB_path,zid)
        row_FAF = ''
        #print(zid)
        #print(rows_FAF)
        #print(type(rows_FAF))
        
        if rows_FAF is None:
            pass
        
        else:
            rows_FAF = list(rows_FAF)
            #print(rows_FAF)
            for FAF in rows_FAF:
                FAF = str(FAF)
                row_FAF += FAF+'\t'
            #print(row_FAF)
            #print(row_FAF+str(row_chemprop)+'\n')
            #sys.exit(1)
            
            if row_chemprop is None:
                #print(row_chemprop)
                if 'ZINC' in zid:
                    row_chemprop = -1
                else:
                    row_chemprop = 1
            fw.write(row_FAF+str(row_chemprop)+'\n')
    
    fw.close()

def sql_fetch_FAF(DB_path,zid):
    try:
        con = sqlite3.connect(DB_path+'Main_FAF.db')
    except:
        print('Failed to connect Main_FAF.db')
    con.text_factory = str
    cursorObj = con.cursor()

    cursorObj.execute('SELECT ID,MW,LogP,PSA,RotatableB,RigidB,HBD,HBA,Rings,MaxSizeRing,Charge,Total_Charge,HeavyAtoms,CarbonAtoms,HeteroAtoms,ratioH_C,Lipinski_Violation,Veber_Violation,Egan_Violation,Functionnal_Group,Toxicity FROM FAF WHERE ID = ?', [zid])
    #cursorObj.execute('SELECT * FROM FAF')
    #print(cursorObj.fetchone())
    
    rows = cursorObj.fetchall()
    #print(len(rows))
    for row in rows:
        #print(row)
        #print(row[0])
        #print(len(row))
        #sys.exit(1)
        return row

def sql_fetch_chemprop(DB_path,zid):
    try:
        con = sqlite3.connect(DB_path+'ZINC_FDA.db')
    except:
        print('Failed to connect ZINC_FDA.db')
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
    print('---> Start')
    print_date_time()

    path = '../Data/Annotation/'
    DB_path = '../Data/DB_Table/'
    os.system('rm -r '+path)
    os.system('mkdir '+path)
    #count(DB_path)

    print('---> Copy All Rounds SDF')
    print_date_time()
    sdf_path = '../Data/Dic_Lib_Output_SDF/'
    os.system('rm -r '+sdf_path+'All')
    R_ls = os.listdir(sdf_path)
    #print(R_ls)
    os.system('mkdir '+sdf_path+'All')
    for R in R_ls:
        R = R+'/'
        sdf_ls = os.listdir(sdf_path+R)
        #print(sdf_ls)
        n_cpu = multiprocessing.cpu_count()-1
        pool = multiprocessing.Pool(processes=n_cpu)
        func = partial(copy_All,sdf_path,R)
        pool.map(func,sdf_ls)
        pool.close()
        pool.join()
    #sys.exit(1)
     
    print('---> Fetch all SDF')
    print_date_time()
    sdf_path = '../Data/Dic_Lib_Output_SDF/All'
    #sdf_path = '../Data/Dic_Lib_Output_SDF/0R'
    sdf_ls = os.listdir(sdf_path)
    write(path,DB_path,sdf_ls)
    #sys.exit(1)
   
    print('---> End')
    print_date_time()

if __name__ == '__main__':
    main()
