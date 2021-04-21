import glob
import sys,os
from time import time
import argparse
import glob
import os
import subprocess
import pickle
from datetime import datetime
import sqlite3

from rdkit import RDConfig
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
from rdkit.Chem import ChemicalFeatures

import multiprocessing
from multiprocessing import Process, Manager
from functools import partial
import json
import copy
import re
import pandas as pd

from io import BytesIO
from zipfile import ZipFile
import zipfile

def SDF_load_MainS(zincid):
    try:
        #conn = sqlite3.connect('/lwork02/yklee/1D_Scan.v3/Data/DB_Table/Main_S.db')
        conn = sqlite3.connect('/ssd/swshin/1D_Scan.v2/Data/DB_Table/Main_S.db')
    except:
        print('DB connect Error')
        sys.exit(1)
    conn.text_factory = str
    cursorObj = conn.cursor()
    try:
        cursorObj.execute('SELECT Sdf FROM Sdf_Files WHERE Zid=?',(zincid,))
    except:
        print('Error %s'%zincid)
        sys.exit(1)
    rows = cursorObj.fetchall()

    if not rows:
        print(zincid)
    else:
        ff = BytesIO(rows[0][0])
        zfp = zipfile.ZipFile(ff,'r')
        zfp_name = zfp.namelist()
        if 'In' in zfp_name[0]:
            zid = zfp_name[0].split('.')[0].split('_')[-1]
        else:
            zid=zincid

        ln_zfp_name = len(zfp_name)
        with open(zid + '.sdf','w') as W:
            W.write(zfp.read(zfp_name[0]))
            W.write('$$$$\n')

def sng_work(zincid):
    scaffold_list = []
    mol1 = Chem.SDMolSupplier(zincid + '.sdf')
    amol = mol1[0]
    token = Chem.MolToSmiles(amol)
    with open(zincid + '.smi','w') as W:
        W.write(token + '\n')
    FNULL = open(os.devnull,'w')
    subprocess.call(['java','-jar','../../sng.jar','generate','-o',zincid+'.tmp',zincid+'.smi'],stdout=FNULL,stderr=subprocess.STDOUT)
    with open(zincid + '.tmp','r') as F:
        for line in F.readlines():
            tline = line.strip()
            if not tline.startswith('RING'):
                ascaffold = extract_scaffold(tline)
                if ascaffold is not None:
                    scaffold_list.append(ascaffold)
    return scaffold_list

def extract_scaffold(line):
    Max_Ring = 3
    token = line.split('\t')
    scaffold=None
    if int(token[0])<=Max_Ring:
        f_flag=0
        if mol_feature_extract(token[1]):
            f_flag=1
        if f_flag == 1:
            scaffold=token[1]
    return scaffold

def mol_feature_extract(m):

    # m: SMILES

    SMILES_flag=False
    SMILES_flag=check_SMILES(m)

    if(not SMILES_flag):
        return False


    f_flag=False

    mol=Chem.MolFromSmiles(m)
    try:
       m_RingCount = Descriptors.RingCount(mol)
    except:
        return
    #num_SSSR=Chem.GetSSSR(mol)
    num_sSSSR=Chem.GetSymmSSSR(mol)

    sub_rln_flag=True
    sub_idx_flag=True
    sub_het_flag=False
    sub_bond_flag=False

    for anum_sSSSR in num_sSSSR:

        ##### 1.Check the length of RING ####
        if len(list(anum_sSSSR))>=7:
            sub_rln_flag=False
            break

        idxs = list(anum_sSSSR)

        i=0
        ln_idxs=len(idxs)

        ##### 2.Check the index for long RING ####
        Diff_Index=12
        for idx in idxs:
            if i<ln_idxs-1:
                if abs(idxs[i]-idxs[i+1])>Diff_Index:
                    sub_idx_flag=False
                    break

            if i==ln_idxs-1:
                if abs(idxs[i]-idxs[0])>Diff_Index:
                    sub_idx_flag=False
                    break
            i+=1


        ##### 3.Check the hetero ATOM  ####
        for idx in idxs:
            atom=mol.GetAtomWithIdx(idx).GetSymbol()
            #### Check hetero atom!!!!!
            if atom=='N' or atom=='O' or atom=='S':
                sub_het_flag=True
                break


        ##### 4.Check the AROMATIC bond ####
        i=0
        for idx in idxs:
            #### Check aromatic or bouble bond!!!!!
            if i+1<ln_idxs:
                btype=mol.GetBondBetweenAtoms(idxs[i],idxs[i+1]).GetBondType()
                if (btype==Chem.rdchem.BondType.AROMATIC):
                    sub_bond_flag=True
                    break
            if i==ln_idxs-1:
                btype=mol.GetBondBetweenAtoms(idxs[i],idxs[0]).GetBondType()
                if (btype==Chem.rdchem.BondType.AROMATIC):
                    sub_bond_flag=True
                    break
            i+=1


        ##### 5.Check Donor or Acceptor ####
        '''
        for idx in idxs:
            fdefName = os.path.join(RDConfig.RDDataDir,'BaseFeatures.fdef')
            factory = ChemicalFeatures.BuildFeatureFactory(fdefName)
            feats = factory.GetFeaturesForMol(mol)
            print feats
            print len(feats)
            print feats[0].GetFamily()
            print feats[1].GetFamily()
            #print feats[2].GetFamily()
            sys.exit(1)
            #### Check hetero atom!!!!!
        '''

    m_NumAromaticCarbocycels = Descriptors.NumAromaticCarbocycles(mol)
    m_NumSaturatedCarbocycles = Descriptors.NumSaturatedCarbocycles(mol)

    # ===================================
    sub_AC_flag=True
    if(m_RingCount == m_NumAromaticCarbocycels or m_RingCount == m_NumSaturatedCarbocycles):
        sub_AC_flag=False
    # ===================================

    ok=False
    #if(sub_rln_flag and sub_idx_flag and sub_het_flag and sub_bond_flag):
    if(sub_rln_flag and sub_idx_flag and sub_het_flag and sub_bond_flag and sub_AC_flag and SMILES_flag):
        ok=True

    return ok
    #return sub_flag

def check_SMILES(asmiles):

    s_flag=True
    Max_Ring=3

    ridx_list=[]
    # Check the ring indexes
    for i in range(1,Max_Ring+1):
        tmp=[]
        tmp=[m.start() for m in re.finditer(str(i),asmiles)]
        if len(tmp)==2:
            ridx_list.append(tmp)

    # Check the ring indexes
    #print asmiles
    #print ridx_list

    list_idx=0
    sets = [set() for _ in xrange(3)]

    #print asmiles
    #print ridx_list

    for alist in ridx_list:
        if len(alist)==0:
            continue
        #print alist
        s=alist[0]
        e=alist[1]
        idx=1
        while(asmiles[s-1].isdigit()):
            s-=1
        s-=1
        while(asmiles[e-1].isdigit()):
            e-=1
        e-=1
        alist[0]=s
        alist[1]=e
        for i in range(s,e+1):
            sets[list_idx].add(i)

        list_idx+=1

    tmp_set=set()
    tmp_set=sets[0]&sets[1]
    tmp_set.update(sets[1]&sets[2])
    tmp_set.update(sets[0]&sets[2])

    smi_type=0
    if len(tmp_set)==0:
        smi_type=1
    else:
        smi_type=0


    #print asmiles
    #print ridx_list
    #print sets
    #print 'set:',smi_type,tmp_set

    if smi_type==1:
        for alist in ridx_list:
            #print alist,
            if len(alist)>0:
                for i in range(alist[0],alist[1]+1):
                    if((asmiles[i].isalpha() and asmiles[i].islower() and asmiles[i]!='c') or asmiles[i]=='='):
                        #print ' -> PASS: Separated'
                        #print
                        #name = raw_input('enter key')
                        return True
    if smi_type==0:
        list_idx=0
        for alist in ridx_list:
            go_ok=1
            #print alist,list_idx+1,
            if len(alist)>0:
                stack=[]
                for i in range(alist[0],alist[1]+1):
                    if((asmiles[i].isalpha() and asmiles[i].islower() and asmiles[i]!='c') or asmiles[i]=='='):
                        #print ' -> PASS: Overlapped'
                        #print
                        #name = raw_input('enter key')
                        return True

                    if(asmiles[i].isdigit() and int(asmiles[i])!=list_idx):
                        c_ring_num=list_idx+1
                        n_ring_num=int(asmiles[i])
                        stack.append(int(asmiles[i]))
                        i+=1
                        while(True):
                            if not asmiles[i].isdigit():
                                # Skip the asmiles[i], Beacuse asmiles[i] is not R_num
                                pass
                            if asmiles[i].isdigit():
                                # In case of closing R_num
                                if int(asmiles[i])==c_ring_num:
                                    break
                                # In case of other R_num
                                if int(asmiles[i])!=c_ring_num:
                                    # In case of other closing R_num, remove other starting R_num
                                    if int(asmiles[i]) in stack:
                                        idx_ch=stack.index(int(asmiles[i]))
                                        stack.remove(int(asmiles[i]))
                                        if len(stack)==0:
                                            break
                                    # In case of other starting R_num, add the starting R_num
                                    if stack[-1]!=int(asmiles[i]):
                                        stack.append(int(asmiles[i]))
                                    #name = raw_input('enter key')
                            i+=1
            list_idx+=1

    # Check fusion scaffold
    list_idx=1
    benz=[]
    for alist in ridx_list:
        if len(alist)>0:
            c_count=0
            for i in range(alist[0],alist[1]+1):
                if asmiles[i].isdigit():
                    continue
                if asmiles[i]=='c':
                    c_count+=1
                if asmiles[i]!='c':
                    break
            if c_count==6:
                benz.append(list_idx)
        list_idx+=1

    #print '\nbenz_list:',benz
    #print 'set size: ',len(sets),sets

    if '2' in asmiles or '3' in asmiles:
        for rn in benz:
            tmp_list=[1,2,3]
            tmp_list.remove(rn)
            for tmp_i in tmp_list:
                if (len(sets[rn-1])>0 and len(sets[tmp_i-1])>0) and ((sets[rn-1]<=sets[tmp_i-1] or sets[rn-1]>=sets[tmp_i-1])):
                    #print 'set1: ',sets[rn-1],'set2:',sets[tmp_i-1]
                    #print '-> PASS: Fusion'
                    #print
                    return True

    #print 'set:',smi_type,tmp_set
    #print ' -> Fail'
    #print
    #name = raw_input('enter key')
    #sys.exit(1)

    #return s_flag
    return False

def multi_work(zincid):
    zincid = zincid.strip()
    SDF_load_MainS(zincid)
    scl = sng_work(zincid)
    if not scl:
        pass
    else:
        for i in scl:
            if not i in didi.keys():
                lili = set()
            else:
                lili = didi[i].split(',')
                lili = set(lili)
            lili.add(zincid)
            lili = ','.join(lili)
            didi[i] = lili
    os.remove(zincid+'.tmp')
    os.remove(zincid+'.smi')

if __name__ == "__main__":
    with open('ttt.list','r') as F:
        sdf_list = F.readlines()
    didi = Manager().dict()
    global didi
    Ncpu = multiprocessing.cpu_count()
    Pool = multiprocessing.Pool(Ncpu-5)
    Pool.map(multi_work,sdf_list)
    Pool.close()
    Pool.join()

    #for sdf in sdf_list:
    #    multi_work(sdf)
    df = pd.DataFrame.from_dict(didi,orient='index').reset_index()
    df.columns=['SMILES','IDs']
    df.to_csv('SCF.csv',index=False)



