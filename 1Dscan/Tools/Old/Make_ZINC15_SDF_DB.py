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

def sql_connection():
    try:
        con = sqlite3.connect('./Out_ZINC_DB/ZINC_S.db')
        con.text_factory = str
        return con

    except Error:
        print(Error)

def sql_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE Sdf_Files(Zid text PRIMARY KEY, Sdf blob)")
    con.commit()

def make_sdf_dic(con):
    du_count = 0
    for j in range(0,200):
        j = str(j)
        if len(j) == 1:
            j = '00'+j
        elif len(j) == 2:
            j = '0'+j
        
        print('In_?_'+j+'.txt')
        time1 = time()

        dic = {}
        test_dic = {}

        Data_path = sys.argv[1]
        In_ls = os.listdir(Data_path)
        for In in In_ls:
            i = str(In.split('_')[1])
            In_path = Data_path+'/'+In+'/merge_sdf/'
            In_file = 'In_'+i+'_'+j+'.txt'
            if os.path.exists(In_path+In_file):
                fr = open(In_path+In_file, 'r')
                #print(In_file)

                while True:
                    line = fr.readline()
                    if not line:break
                    if 'ZINC' in line and '_' not in line:
                        zid = line.rstrip()
                        #print(zid)
                        sdf_ls = line

                        while True:
                            line = fr.readline()
                            #print(line)
                            sdf_ls += line
                            if 'END' in line:break
                        test_dic[zid]=sdf_ls
                
                        #dic[zid] = temp_zipfile(i,j,sdf_ls,zid,dic)
                        #dic[zid] = stringIO_zipfile(i,j,sdf_ls,zid,dic)
                        #dic[zid] = lzma(i,j,sdf_ls,zid,dic)
                        du_count = sql_insert(i,j,sdf_ls,zid,dic,con,du_count)

                fr.close()
        #print(dic)
        time2 = time()
        print(str(time2-time1))
    con.commit()
    return du_count

def sql_insert(i,j,sdf_ls,zid,dic,con,du_count):
    mf = StringIO.StringIO()
    with zipfile.ZipFile(mf, mode='w', compression=zipfile.ZIP_DEFLATED) as zf: 
        zf.writestr('In_'+i+'_'+j+'_'+zid+'.txt', sdf_ls)
    sdf_ls_zip = mf.getvalue()
    entities = (zid, sdf_ls_zip)
    
    #entities = (zid, sdf_ls)
    cursorObj = con.cursor()
    try:
        cursorObj.execute('INSERT INTO Sdf_Files(Zid, Sdf) VALUES(?, ?)', entities)
    except sqlite3.IntegrityError:
        #print entities[0]
        du_count += 1
    return du_count


def sql_fetch(con):
    cursorObj = con.cursor()
    zid = 'ZINC000185989040'
    #cursorObj.execute('SELECT * FROM Sdf_Files')
    cursorObj.execute('SELECT Sdf FROM Sdf_Files WHERE Zid = ?', [zid])
    #print(cursorObj.fetchone())
    
    rows = cursorObj.fetchall()
    for row in rows:
        print(row)
    

def main():
    os.system('rm ./Out_ZINC_DB/ZINC_S.db')
    con = sql_connection()
    sql_table(con)
    du_count = make_sdf_dic(con)
    print(du_count)
    #sql_fetch(con)

if __name__ == '__main__':
    main()
