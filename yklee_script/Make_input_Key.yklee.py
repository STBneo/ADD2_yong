import os, sys, glob, subprocess, apsw, itertools,argparse
import multiprocessing
from multiprocessing import Process, Manager
from functools import partial
import pandas as pd
from sqlite3 import Error
import sqlite3
import time
from datetime import datetime
import marshal

def key_dic_load():
    didi = {}
    with open('../Data/Table/Result_0.dat','rb') as F:
        for i in marshal.load(F):
            didi[i[0]] = i[1]
    return didi

def dict2df(inp):
    ttt = {}
    lll = []
    lili = []
    pdf = pd.DataFrame.from_dict(inp,orient='index').reset_index().rename(columns={'index':'Key',0:'Freq'}).sort_values(by='Freq',ascending=False).reset_index(drop=True)
    print(pdf)
    for i,j in zip(range(0,len(pdf['Freq'])),pdf['Freq']):
        ttt[j] = i
    for i in pdf['Freq']:
        lll.append(ttt[i])
    pdf['Rank'] = lll
    all_p = float(pdf['Rank'].max())
    for i in pdf['Rank']:
        t_p = (float(i)/all_p)*100
        lili.append('{:.3f}'.format(t_p))
    pdf['Percent'] = pd.DataFrame(lili).astype(float)
    print(pdf)
    return pdf

def analysis_Key(df,top_p,mins):
    outdf = df[df['Percent']<= float(top_p)][df['Freq'] >= int(mins)]
    return outdf

def make_dir(a):
    try:
        if os.path.exists(a):
            os.chdir(a)
            pass
        else:
            os.makedirs(a)
            os.chdir(a)
    except:
        print("DIR CREATE ERROR")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-top_p',required=True,default=100,help='Select the top X percent of Key Frequency')
    parser.add_argument('-mins',required=True,default=1,help='The minimum number of Key')
    args = parser.parse_args()

    Oridict = key_dic_load()
    df = dict2df(Oridict)
    odf = analysis_Key(df,args.top_p,args.mins)
    make_dir('Input_Key_Statistics')
    df.to_csv('Input_Temp_Freq.csv',index=False)
    odf.to_csv('Activate_Input.csv',index=False)
    
