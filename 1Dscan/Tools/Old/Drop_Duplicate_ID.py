import pandas as pd
import multiprocessing,glob,os,sys,time
from multiprocessing import Manager
from functools import partial

def subtract_list(a,b,c,zid):
    try :
        if a[zid] == 1:
            pass
    except:
        b[zid] = 1
        c[zid] = 1

def read_list(a):
    df = pd.read_csv(a,sep='\t')
    df[0] = 1
    dd = df.set_index('zinc_id').to_dict('dict')
    print(len(dd[0].keys()))
    return dd[0]

def multi_work(dict1,dict2,dict3):
    temp_dict = Manager().dict()
    Ncpu = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(Ncpu-1)

    func = partial(subtract_list,dict1,dict2,temp_dict)
    print(len(dict3.keys()))
    pool.map(func,dict3.keys())
    pool.close()
    pool.join()
    didi = pd.DataFrame.from_dict(dict2,orient='index').reset_index().rename(columns={'index':'zinc_id'}).drop([0],axis=1)
    uni_dict = pd.DataFrame.from_dict(temp_dict,orient='index').reset_index().rename(columns={'index':'zinc_id'}).drop([0],axis=1)

    return didi,uni_dict

if __name__ == "__main__":
    f_list = sorted(glob.glob('*.txt'))
    d1 = read_list(f_list[0])
    main_dict = Manager().dict(d1)
    n = 0
    for i in f_list[1:]:
        d2 = read_list(i)
        if n == 0:
            didi,uni_dict = multi_work(d1,main_dict,d2)
            n +=1
        else:
            didi,uni_dict = multi_work(didi,main_dict,d2)
        didi.to_csv('%s_needs.txt'%(i.split('.')[0]),sep='\t',index=False)
        uni_dict.to_csv('%s_uniq.txt'%(i.split('.')[0]),sep='\t',index=False)