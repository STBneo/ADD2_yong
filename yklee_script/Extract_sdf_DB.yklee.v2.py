import os, sys
#import StringIO
import zipfile
import sqlite3
import multiprocessing
from multiprocessing import Manager
from functools import partial
from time import time
import glob
from io import BytesIO
import pybel
from zipfile import ZipFile
from StringIO import StringIO
import pandas as pd


# python Extract_sdf_DB.V2.py ./test2   in test: CSV file


def sql_fetch(DB_path, sdf_path, f_zid_ls, p_zid_ls, zid):

    try:
        con = sqlite3.connect(DB_path+'Main_S.db')
    except Error:
        print('DB connection failed!')
        sys.exit(1)

    con.text_factory = str
    cursorObj = con.cursor()
    
    try:
        cursorObj.execute('SELECT Sdf FROM Sdf_Files WHERE Zid = ?', [zid]) 
        rows = cursorObj.fetchall()
        ln_zid = len(rows)
        tmp_sdf=''

        if ln_zid != 0:
            try:
                fp=BytesIO(rows[0][0])
                zfp=zipfile.ZipFile(fp,'r')
                zfp_name=zfp.namelist()
                ln_zfp_name=len(zfp_name)
                #print(ln_zfp_name)
                if ln_zfp_name!=1:
                    print('Error: more than two id')
                else:
                    pass
                    #print(zfp_name[0])
                    f_name=zfp_name[0].split('_')
                    #print(f_name[-1])
                    tmp_sdf=zfp.read(zfp_name[0])                    
                    zfp.close()
            except:
                print('Error_try')

            #print(sdf_path,zid)
            if 'STK' not in zid:
                tmp_sdf=tmp_sdf+'$$$$\n'
            #print(tmp_sdf)
            mymol = pybel.readstring('sdf',tmp_sdf)
            #mymol_pdb = mymol.write(format='pdb')
            mymol.write(format='pdb',filename=sdf_path + zid+'.pdb')
            tmp_c=p_zid_ls[0]
            tmp_c+=1
            p_zid_ls[0]=tmp_c
            #print('')
        else:
            #f_zid_ls.append(zid)
            f_zid_lsi[0]+=1
    except:
        pass
def divide_list(ls,n):
    for i in range(0,len(ls),n):
        yield ls[i:i+n]

def read_afile(in_afile,t_f,f_count):
    time1 = time()
    DB_path = '../Data/DB_Table/'

    zid_ls = []
    zid_file = in_afile
    R = 'SKR' #zid_file.split('/')[-1].split('.')[3]
    df = pd.read_csv(zid_file,sep='\t')
    print(df)
    zid_ls = df['ID'][:100]
    sdf_path = '../Data/Dic_Lib_Output_PDB/'+R+'/'
    #os.system('rm -r '+sdf_path)
    os.system('mkdir '+sdf_path)

    manager = Manager()
    f_zid_ls = manager.list()
    p_zid_ls = manager.list()
    
    f_zid_ls.append(0)
    p_zid_ls.append(0)

    n_cpu = multiprocessing.cpu_count()-1
    pool = multiprocessing.Pool(processes=n_cpu)
    func = partial(sql_fetch, DB_path, sdf_path, f_zid_ls, p_zid_ls)
    pool.map(func, zid_ls)
    #pool.map(func, zid_ls[0:10001])
    pool.close()
    pool.join()
    time2 = time()

    print('\n'+str(f_count+1)+'/'+str(t_f)+' For :'+in_afile)
    print('Total ID : '+str(len(zid_ls))+' (with duplicates)')
    print('Passed ID : '+str(p_zid_ls[0])+' (without duplicates)')
    print('Failed ID : '+str(f_zid_ls[0]))
    print('Processing time: '+str(time2-time1)+'\n')

def read_tdir():
    #t_path='../Data/Dic_Lib_Input/' 
    #sdfs_path=t_path+'/*.csv'
    t_path = '../Data/Annotation/'#'../Data/SKR_Out/SKR_result/'
    sdfs_path = t_path + 'results.table.id.pass'
    print(os.getcwd())
    t_files=glob.glob(sdfs_path)
    return t_files

def main():
    f_files=read_tdir()
    ln_f_files=len(f_files)
    f_count=0
    os.system('rm -r ../Data/Dic_Lib_Output_SDF')
    os.system('mkdir ../Data/Dic_Lib_Output_SDF')
    for afile in f_files:
        read_afile(afile,ln_f_files,f_count)
        f_count+=1

if __name__ == '__main__':
    time1 = time()
    main()
    time2 = time()
    print('\nTotal Processing time: '+str(time2-time1)+'\n')

