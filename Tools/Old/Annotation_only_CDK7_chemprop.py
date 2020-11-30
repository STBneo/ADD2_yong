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
  
    sdf_path = '../Data/Dic_Lib_Output_SDF_RAW_10/All/'
    fr = open('../Data/Chemprop_CDK7/CDK7.all_res.csv','r')
    while True:
        line = fr.readline()
        if not line:break
        
        while True:
            line = fr.readline()
            if not line:break
            line = line.split('\t')
            zid = line[0]
            row = line[1].rstrip()
            if row == '':
                row = -1
            if float(row) >= 0.5:
                os.system('cp '+sdf_path+zid+'.sdf ../Data/FDA/PASS')

def main():
    print('Start')
    print_date_time()
    read()
    print('End')
    print_date_time()

if __name__ == '__main__':
    main()
