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
from zipfile import ZipFile
from StringIO import StringIO


# python Extract_sdf_DB.V2.py ./test2   in test: CSV file


def sql_fetch(DB_path, sdf_path, f_zid_ls, p_zid_ls, zid):

    try:
        con = sqlite3.connect(DB_path+'ZINC_S.db')
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
            tmp_sdf=tmp_sdf+'$$$$\n'
            #print(tmp_sdf)
            fp_for_out = open(sdf_path+zid+'.sdf', 'w')
            fp_for_out.write(tmp_sdf)
            fp_for_out.close()
            #p_zid_ls.append(zid)
            #p_zid_ls[0]+=1
            tmp_c=p_zid_ls[0]
            tmp_c+=1
            p_zid_ls[0]=tmp_c
            #print('')
        else:
            #f_zid_ls.append(zid)
            f_zid_lsi[0]+=1
    except:
        pass


def read_afile(in_afile,t_f,f_count):

    time1 = time()
    DB_path = '/lwork01/swshin/PHscan_1D_ZINC15_M/Data/DB_Table/'

    zid_ls = []
    zid_file = in_afile
    fr = open(zid_file, 'r')

    while True:
        line = fr.readline()
        zid = line.split(',')[0]
        if len(zid) >= 7:
            zid = 'ZINC00'+zid
            zid_ls.append(zid)
        if not line: break

    fr.close()

    sdf_path = './'+zid_file[:-4]+'/'
    os.system('rm -r '+sdf_path)
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
    print('Total ID : '+str(len(zid_ls)))
    #print('Passed ID : '+str(len(p_zid_ls)))
    #print('Failed ID : '+str(len(f_zid_ls)))
    print('Passed ID : '+str(p_zid_ls[0]))
    print('Failed ID : '+str(f_zid_ls[0]))
    print('Processing time: '+str(time2-time1)+'\n')

def read_tdir():
    t_path=sys.argv[1] 
    sdfs_path=t_path+'/*.csv'
    t_files=glob.glob(sdfs_path)
    return t_files


def main():

    f_files=read_tdir()
    ln_f_files=len(f_files)
    f_count=0
    for afile in f_files:
        read_afile(afile,ln_f_files,f_count)
        f_count+=1


if __name__ == '__main__':
    time1 = time()
    main()
    time2 = time()
    print('\nTotal Processing time: '+str(time2-time1)+'\n')
