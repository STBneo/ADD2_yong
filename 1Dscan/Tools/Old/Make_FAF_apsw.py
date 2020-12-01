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

def sql_connection():
    try:
        con = apsw.Connection(':memory:')
        return con
    except Error:
        print(Error)
    return

def sql_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE FAF(ID text PRIMARY KEY, MW float, LogP float, PSA float, RotatableB int, RigidB int, HBD int, HBA int, Rings int, MaxSizeRing int, Charge int, Total_Charge int, HeavyAtoms int, CarbonAtoms int, HeteroAtoms int, ratioH_C int, Lipinski_Violation int, Veber_Violation text, Egan_Violation text, Functionnal_Group text, Toxicity text)")
    #con.commit()
    return

def make_sdf_dic(con):
    #for i in range(0,1): #
    for i in range(0,197): #
        table = 'results.table.id.'+str(i)
        print(table)
        print_date_time()
        fr = open('Table/'+table,'r')

        while True:
            line = fr.readline()
            #print(line)
                
            if 'ZINC' in line:
                line = line.split('\t')
                #print(line)
                ID = line[0]
                MW = line[1]
                LogP = line[2]
                PSA = line[3]
                RotatableB = line[4]
                RigidB = line[5]
                HBD = line[6]
                HBA = line[7]
                Rings = line[8]
                MaxSizeRing = line[9]
                Charge = line[10]
                Total_Charge = line[11]
                HeavyAtoms = line[12]
                CarbonAtoms = line[13]
                HeteroAtoms = line[14]
                ratioH_C = line[15]
                Lipinski_Violation = line[16]
                Veber_Violation = line[17]
                Egan_Violation = line[18]
                Functionnal_Group = line[19]
                Toxicity = line[20].rstrip()

                ln_zid = sql_check(con,ID)
                if ln_zid == 0:
                    entities = (ID,MW,LogP,PSA,RotatableB,RigidB,HBD,HBA,Rings,MaxSizeRing,Charge,Total_Charge,HeavyAtoms,CarbonAtoms,HeteroAtoms,ratioH_C,Lipinski_Violation,Veber_Violation,Egan_Violation,Functionnal_Group,Toxicity)
                    sql_insert(con,entities)

            if not line: break
        fr.close()

    dest=apsw.Connection('./ZINC_FAF.db')
    with dest.backup('main',con,'main') as backup:
        backup.step()
    dest.close()
    con.close()

def sql_check(con,ID):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT ID FROM FAF WHERE ID = ?',(ID,))
    rows = cursorObj.fetchall()
    ln_zid=len(rows)
    return ln_zid

def sql_insert(con,entities):
    global du_count
    cursorObj = con.cursor()
    try:
        cursorObj.execute('INSERT INTO FAF(ID,MW,LogP,PSA,RotatableB,RigidB,HBD,HBA,Rings,MaxSizeRing,Charge,Total_Charge,HeavyAtoms,CarbonAtoms,HeteroAtoms,ratioH_C,Lipinski_Violation,Veber_Violation,Egan_Violation,Functionnal_Group,Toxicity) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', entities)
        return 1
    except sqlite3.IntegrityError:
        du_count += 1
        return 0

def sql_fetch():
    con = sqlite3.connect('./ZINC_FAF.db')
    con.text_factory = str
    cursorObj = con.cursor()
    ID = 'ZINC000829744282'
    cursorObj.execute('SELECT ID,MW,LogP,PSA,RotatableB,RigidB,HBD,HBA,Rings,MaxSizeRing,Charge,Total_Charge,HeavyAtoms,CarbonAtoms,HeteroAtoms,ratioH_C,Lipinski_Violation,Veber_Violation,Egan_Violation,Functionnal_Group,Toxicity FROM FAF WHERE ID = ?', [ID])
    #cursorObj.execute('SELECT * FROM FAF')
    #print(cursorObj.fetchone())
    
    rows = cursorObj.fetchall()
    #print(len(rows))
    for row in rows:
        print(row)

def main():
    print('---> Start')
    print_date_time()

    con = sql_connection()
    sql_table(con)
    make_sdf_dic(con)
    sql_fetch()
    
    print('---> End')
    print_date_time()

if __name__ == '__main__':
    main()

