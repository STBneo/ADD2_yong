from rdkit import Chem
from rdkit.Chem import Descriptors
import glob
from rdkit.Chem import AllChem
import sys,os
from time import time
import argparse
import glob
import os
import subprocess
import pickle
from rdkit.Chem import Draw
from datetime import datetime
from rdkit.Chem import ChemicalFeatures
from rdkit import RDConfig
import multiprocessing
from multiprocessing import Process, Manager
from functools import partial
import json
import copy
import re

#for negative data python anal_mols.rdkit.py 0 ./Drug_Bank/sdf_output_toxi/
#for positive data python anal_mols.rdkit.py 1 ./Drug_Bank/sdf_output_toxi/

def featurize_atoms(mol):
    feats = []
    for atom in mol.GetAtoms():
        feats.append(atom.GetAtomicNum())
    return {'atomic': torch.tensor(feats).reshape(-1, 1).float()}
                    
def featurize_bonds(mol):
    feats = []
    bond_types = [Chem.rdchem.BondType.SINGLE, Chem.rdchem.BondType.DOUBLE,Chem.rdchem.BondType.TRIPLE, Chem.rdchem.BondType.AROMATIC]
    for bond in mol.GetBonds():
        btype = bond_types.index(bond.GetBondType())
        # One bond between atom u and v corresponds to two edges (u, v) and (v, u)
        feats.extend([btype, btype])
    return {'type': torch.tensor(feats).reshape(-1, 1).float()}


def find_atom(one_hot):
    atoms=['C',' N',' O',' S',' F',' Si',' P',' Cl',' Br',' Mg',' Na',' Ca',' Fe',' As',' Al',' I',' B',' V',' K',' Tl',' Yb',' Sb',' Sn',' Ag',' Pd',' Co',' Se',' Ti',' Zn',' H',' Li',' Ge',' Cu',' Au',' Ni',' Cd',' In',' Mn',' Zr',' Cr',' Pt',' Hg',' Pb']
    #print(len(atoms))
    #print(len(one_hot))
    a_idx=one_hot.index(True)
    a_type=atoms[a_idx]
    #print (a_idx,a_type)
    return a_type


def find_bond_type(one_hot):
    atoms=['C',' N',' O',' S',' F',' Si',' P',' Cl',' Br',' Mg',' Na',' Ca',' Fe',' As',' Al',' I',' B',' V',' K',' Tl',' Yb',' Sb',' Sn',' Ag',' Pd',' Co',' Se',' Ti',' Zn',' H',' Li',' Ge',' Cu',' Au',' Ni',' Cd',' In',' Mn',' Zr',' Cr',' Pt',' Hg',' Pb']
    #print(len(atoms))
    #print(len(one_hot))
    a_idx=one_hot.index(True)
    a_type=atoms[a_idx]
    #print (a_idx,a_type)
    return a_type


def write_feature(fp_for_out,f_type,*f_list):
   
    #print (f_list,len(f_list))
    #sys.exit(1)

    if(len(f_list)==1 and f_list=='\n'):
        fp_for_out.wirte(f_list)
        return
    else:
        tmp_res=''
        for af_list in f_list:
            #print(af_list)
            #s=[str(i) for i in af_list]
            #res=",".join(s)
            res=','.join(map(str,af_list))
            tmp_res=tmp_res+res+','
        tmp_res=tmp_res+str(f_type)
        #print(tmp_res)
        #sys.exit(1)
        fp_for_out.write(tmp_res+'\n')
            
        return
            

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


def mol_feature_extract(m):

    # m: SMILES

    SMILES_flag=False
    SMILES_flag=check_SMILES(m)

    if(not SMILES_flag):
        return False

    #sys.exit(1)

    f_flag=False

    #print 
    #print 'smiles:',m
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
        #print list(anum_sSSSR)
        if len(list(anum_sSSSR))>=7:
        #if len(list(anum_sSSSR))>=7 or len(list(anum_sSSSR))<=3:
            #print list(anum_sSSSR)
            sub_rln_flag=False
            break

        idxs = list(anum_sSSSR)
        #print idxs,len(idxs)

        i=0
        ln_idxs=len(idxs)

        ##### 2.Check the index for long RING ####
        Diff_Index=12 
        for idx in idxs:
            #print idxs[i],idxs[i+1],abs(idxs[i]-idxs[i+1])
            if i<ln_idxs-1:
                #print idxs[i],idxs[i+1],abs(idxs[i]-idxs[i+1])
                if abs(idxs[i]-idxs[i+1])>Diff_Index:
                    sub_idx_flag=False
                    break
                    
            if i==ln_idxs-1:
                #print idxs[i],idxs[0],abs(idxs[i]-idxs[0])
                if abs(idxs[i]-idxs[0])>Diff_Index:
                    sub_idx_flag=False
                    break
            i+=1
       

        ##### 3.Check the hetero ATOM  ####
        for idx in idxs:
            atom=mol.GetAtomWithIdx(idx).GetSymbol()
            #print 'index:',int(idx),'atom:',atom
            #### Check hetero atom!!!!!
            if atom=='N' or atom=='O' or atom=='S':
                sub_het_flag=True
                break


        ##### 4.Check the AROMATIC bond #### 
        i=0
        for idx in idxs:
            #### Check aromatic or bouble bond!!!!!
            #print sub_flag
            if i+1<ln_idxs:
                #print i,i+i,idxs[i],idxs[i+1]
                btype=mol.GetBondBetweenAtoms(idxs[i],idxs[i+1]).GetBondType()
                #print btype 
                #if btype=='AROMATIC' or btype=='DOUBLE':
                #if (btype==Chem.rdchem.BondType.AROMATIC or btype==Chem.rdchem.BondType.DOUBLE or btype==Chem.rdchem.BondType.TRIPLE):
                if (btype==Chem.rdchem.BondType.AROMATIC):
                    #print 'AROMATIC'
                    sub_bond_flag=True
                    break
            if i==ln_idxs-1:
                #print i,'0',idxs[i],idxs[0]
                btype=mol.GetBondBetweenAtoms(idxs[i],idxs[0]).GetBondType()
                #print btype
                #Chem.rdchem.BondType.AROMATIC
                #if (btype==Chem.rdchem.BondType.AROMATIC or btype==Chem.rdchem.BondType.DOUBLE or btype==Chem.rdchem.BondType.TRIPLE):
                if (btype==Chem.rdchem.BondType.AROMATIC):
                #if btype=='AROMATIC' or btype=='DOUBLE':
                    #print 'AROMATIC'
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



    #print 'sub_flag:',sub_flag
    m_NumAromaticCarbocycels = Descriptors.NumAromaticCarbocycles(mol)
    m_NumSaturatedCarbocycles = Descriptors.NumSaturatedCarbocycles(mol)


    # ===================================
    sub_AC_flag=True 
    if(m_RingCount == m_NumAromaticCarbocycels or m_RingCount == m_NumSaturatedCarbocycles): 
        sub_AC_flag=False 
    # ===================================

    '''
    # Only C and H
    # Non-aromatic compound
    m_NumAromaticRings = Descriptors.NumAromaticRings(mol)
    # Aromatics
    m_NumAliphaticRings = Descriptors.NumAliphaticRings(mol)

    # Important Rule
    # Must include rule_1
    m_NumAromaticHeterocycels = Descriptors.NumAromaticHeterocycles(mol)

    # Must exclude rule_2
    m_NumAromaticCarbocycels = Descriptors.NumAromaticCarbocycles(mol)

    # Must exclude rule_3
    m_NumSaturatedHeterocycles = Descriptors.NumSaturatedHeterocycles(mol)

    # Must exclude rule_3
    m_NumSaturatedCarbocycles = Descriptors.NumSaturatedCarbocycles(mol)

    print m
    print 'm_SSSR: ', num_SSSR
    print 'm_RingCount: ', m_RingCount
    print 'm_NumAromaticRings: ',m_NumAromaticRings
    print 'm_NumAliphaticRings: ',m_NumAliphaticRings
    print 'm_NumAromaticHeterocycels: ',m_NumAromaticHeterocycels
    print 'm_NumAromaticCarbocycels: ',m_NumAromaticCarbocycels
    print 'm_NumSaturatedHeterocycles: ',m_NumSaturatedHeterocycles
    print 'm_NumSaturatedCarbocycles: ',m_NumSaturatedCarbocycles

    if (m_RingCount==m_NumAromaticHeterocycels):    
        f_flag=False
    else:
        f_flag=True
     


    raw_input("Press Enter to continue...")
    '''
    '''
    sub_rln_flag=True
    sub_idx_flag=True
    sub_het_flag=False 
    sub_bond_flag=False 
    '''
    '''
    print 'rln: ',sub_rln_flag
    print 'dix: ',sub_idx_flag
    print 'het: ',sub_het_flag 
    print 'bond:',sub_bond_flag
    print 
    '''

    ok=False
    #if(sub_rln_flag and sub_idx_flag and sub_het_flag and sub_bond_flag):
    if(sub_rln_flag and sub_idx_flag and sub_het_flag and sub_bond_flag and sub_AC_flag and SMILES_flag):
        ok=True

    return ok
    #return sub_flag



def mol_scaffold_extract(lid,amol):

    # making smiles
    t_dir='./sng_tmp/'
    smiles=Chem.MolToSmiles(amol)
    # print smiles
    f_name=lid+'.smi'

    # write smiles
    t_path=os.path.join(t_dir,f_name)
    fp_for_out=open(t_path,'w')
    fp_for_out.write(smiles)
    fp_for_out.close()

    # excuate sng
    FNULL = open(os.devnull, 'w')
    subprocess.call(['java','-jar','sng.jar','generate','-o', t_dir+lid+'.tmp',t_dir+f_name], stdout=FNULL, stderr=subprocess.STDOUT)

    # read the sng output
    re_name=lid+'.tmp'
    t_path=os.path.join(t_dir,re_name)
    fp_for_in=open(t_path,'r')
    lines=fp_for_in.readlines()
    fp_for_out.close()
    #print lines

    scaffold_list=[]
    for aline in lines: 
        aline=aline.strip()
        if 'RING' not in aline:
            #print aline
            ascaffold=processing_line(aline)
            if ascaffold is not None: 
                #print ascaffold
                scaffold_list.append(ascaffold)

    #print scaffold_list
    #sys.exit(1)
    return scaffold_list


def processing_line(aline):

    Max_RING=3

    token=aline.split('\t')
    #print int(token[0])
    scaffold=None

    if int(token[0])<=Max_RING:
    #if int(token[0])==3: 
        #print token[0]
        f_flag=0
        # apply reult 1
        '''
        if 'N' in token[1]:
            f_flag=1
        if 'O' in token[1]:
            f_flag=1
        if 'S' in token[1]:
            f_flag=1
        '''
        # apply the rule 
        if mol_feature_extract(token[1]):
            f_flag=1

        if f_flag==1:
            scaffold=token[1]


    return scaffold 


def print_date_time():

    now = datetime.now()
    w=datetime.now()
    dt_string=now.strftime("%d/%m/%Y %H:%M:%S")
    print 'Date and Time: ',dt_string


def make_db(i_path):

    time1=time()

    t_dir='./sng_tmp/'
    if not os.path.exists(t_dir):
        os.makedirs(t_dir)
    else:
        arg='rm '+t_dir+'*'
        os.system(arg)
        #shutil.rmtree(l_base)

    t_dir='../Data/Input_SCF/'
    if not os.path.exists(t_dir):
        os.makedirs(t_dir)
    else:
        arg='rm '+t_dir+'*'
        os.system(arg)
        #shutil.rmtree(l_base)

    #print i_path 
    f_list=glob.glob(i_path+'*.sdf')
    f_list.sort()
    #print(f_list)
    #print(len(f_list))
    ln_f=len(f_list)

    tmp_dic={}
    tmp_set=set()
    #return

    manager = Manager()
    Re_dic = manager.dict()

    id_list = manager.list()
    tmp_dic  = manager.dict()

    SMILES_dic = manager.dict()
    smi_list = manager.list()

    #print type(Re_dic)
    #print type(SMILES_dic)
    #print Re_dic2
    #sys.exit(1)

    #print ln_f,f_list
    #return

    Num_Of_CPU=multiprocessing.cpu_count()
    #Num_Of_CPU=2
    #print Num_Of_CPU
    pool = multiprocessing.Pool(processes=(Num_Of_CPU-1))
    func=partial(core_make,ln_f,f_list,tmp_dic,id_list)
    pool.map(func,f_list)
    pool.close()

    #print tmp_dic
    tmp_dic=dict(tmp_dic)
    #print tmp_dic

    # For the fold for scaffolds decomposition output which is input for Scaffold DB searching 
    st_dir='../Data/Input_SCF/'
    if not os.path.exists(st_dir):
        os.makedirs(st_dir)
    else:
        arg='rm '+st_dir+'*'
        os.system(arg)
        #shutil.rmtree(l_base)
   
    Scaffold_id=0
    smiles=tmp_dic.keys()
    for asmiles in smiles:
        print asmiles
        f_name='Scaffold.'+str(Scaffold_id)+'.smi'
        f_path=st_dir+f_name
        print f_path
        fp_for_out=open(f_path,'w')
        fp_for_out.write(asmiles)
        Scaffold_id+=1
        fp_for_out.close()
    # remove Input_SCF contents before use!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!         

    '''
    s_count=0
    ln_key=len(tmp_dic)
    fp_out_s_list=open('Scaffold_db_list.txt','w')
    tmp_str='SMILES\tLId\n'
    fp_out_s_list.write(tmp_str)
    for key, value in tmp_dic.iteritems():
        tmp_str=''
        res=",".join(value)
        tmp_str=key+'\t'+res+'\n'
        fp_out_s_list.write(tmp_str)
        
        # for scaffold sdf format
        try:
            amol=Chem.MolFromSmiles(key)
            AllChem.Compute2DCoords(amol)
            asdf=Chem.MolToMolBlock(amol)
            #sys.exit(1)
        except:
            continue

        sf_fname='sf_id_'+str(s_count)+'.sdf'
        gsf_fname=st_dir+'sf_id_'+str(s_count)+'.png'
        #Draw.MolToFile(asdf,gsf_fname)
        print 'Processing: '+str(s_count)+'/'+str(ln_key)+','+gsf_fname

        s_count+=1
        t_path=os.path.join(st_dir,sf_fname)
        fp_for_sdf=open(t_path,'w')
        fp_for_sdf.write(asdf+'$$$$\n')
        fp_for_sdf.close()

        arg='obabel '+t_path+' -O '+gsf_fname
        #print arg
        os.system(arg)

    #fp_for_out.close()
    fp_out_s_list.close()

    #print tmp_dic
    #save the dic
    with open('scaffold_db.pickle', 'wb') as handle:
        pickle.dump(tmp_dic,handle,protocol=pickle.HIGHEST_PROTOCOL)
    '''

    arg='rm -r sng_tmp'
    os.system(arg)

    print '\nThe length of library: '+str(len(tmp_dic))
    time2=time()
    print 'Processing time: '+str(time2-time1)+'\n'
    print_date_time()

    return



def core_make(ln_mols,f_list,tmp_dic,id_list,afile):
    
    aidx=f_list.index(afile)
    e_flag=0
    try:
        mols = Chem.SDMolSupplier(afile)
    except:
        print('Error in RDKit')
        e_flag=1

    if(e_flag==0):
        mol_count=0
        for amol in mols:
            ln_2mols=len(mols)
            scaffold_list=[]
            try:
                #asf=Chem.MolToMolBlock(amol)
                #print asf
                token=Chem.MolToMolBlock(amol).split('\n')
                #print token
                #sys.exit(1)
            except:
                continue

            #sys.exit(1)
            #print token
            lid=token[0]
            #print '   Sub_processing....:'+str(mol_count+1)+'/'+str(ln_2mols)+' ,mol:'+lid
            mol_count+=1
            #print lid
            #sys.exit(1)
            scaffold_list = mol_scaffold_extract(lid,amol)
            #print scaffold_list
            #sys.exit(1)

            ln_scaffold_list=len(scaffold_list)
            # making dic
            if ln_scaffold_list>0:
                for a_sf in scaffold_list:
                    if a_sf in tmp_dic:
                        id_list=[]
                        id_list=tmp_dic[a_sf]
                        '''
                        if len(id_list)>0:
                            print('Binog')
                        '''
                        id_list.append(lid)
                        tmp_dic[a_sf]=id_list
                        #tmp_dic[a_sf].append(lid)
                    else:
                        id_list=[]
                        id_list.append(lid)
                        tmp_dic[a_sf]=id_list
            #print tmp_dic    
            #sys.exit(1)
    else:
        pass
    #print 
    #print len(tmp_dic),tmp_dic
    print 'Processing....:'+str(aidx+1)+'/'+str(ln_mols)+' ,mol:'+afile[:-4] 

    return


    '''
    # For scaffold smiles to sdf 
    st_dir='./Scaffolds_Out/'
    if not os.path.exists(st_dir):
        os.makedirs(st_dir)
    else:
        arg='rm '+st_dir+'*'
        os.system(arg)
        #shutil.rmtree(l_base)
    
    s_count=0
    ln_key=len(tmp_dic)
    fp_out_s_list=open('Scaffold_db_list.txt','w')
    tmp_str='SMILES\tLId\n'
    fp_out_s_list.write(tmp_str)
    for key, value in tmp_dic.iteritems():
        tmp_str=''
        res=",".join(value)
        tmp_str=key+'\t'+res+'\n'
        fp_out_s_list.write(tmp_str)
        
        # for scaffold sdf format
        try:
            amol=Chem.MolFromSmiles(key)
            AllChem.Compute2DCoords(amol)
            asdf=Chem.MolToMolBlock(amol)
            #sys.exit(1)
        except:
            continue

        sf_fname='sf_id_'+str(s_count)+'.sdf'
        gsf_fname=st_dir+'sf_id_'+str(s_count)+'.png'
        #Draw.MolToFile(asdf,gsf_fname)
        print 'Processing: '+str(s_count)+'/'+str(ln_key)+','+gsf_fname

        s_count+=1
        t_path=os.path.join(st_dir,sf_fname)
        fp_for_sdf=open(t_path,'w')
        fp_for_sdf.write(asdf+'$$$$\n')
        fp_for_sdf.close()

        arg='obabel '+t_path+' -O '+gsf_fname
        #print arg
        os.system(arg)

    #fp_for_out.close()
    fp_out_s_list.close()

    #print tmp_dic
    #save the dic
    with open('scaffold_db.pickle', 'wb') as handle:
        pickle.dump(tmp_dic,handle,protocol=pickle.HIGHEST_PROTOCOL)

    print '\nThe length of library: '+str(len(tmp_dic))
    time2=time()
    print 'Processing time: '+str(time2-time1)+'\n'
    print_date_time()
    '''

    return


#func=partial(core,Re_dic,mols,ln2_mols)
def core(db_dic,Re_dic,tmp_list,SMILES_dic,id_list,f_list,ln_f,amfile):

    tmp_list=[]
    aidx=f_list.index(amfile)
    #print amfile
    #print aidx

    try:
        mols = Chem.SDMolSupplier(amfile)
    except:
        print 'Error in reading file RDKit'
        return
    #print amol
    amol=mols[0]

    scaffold_list=[]
    try:
        token=Chem.MolToMolBlock(amol).split('\n')
    except:
        print 'Erro in parsing the RD object'
        return
    lid=token[0]
    #print 'Searching....:'+str(aidx+1)+'/'+str(ln_f)+' ,mol:'+lid
    #print lid
    #sys.exit(1)

    scaffold_list = mol_scaffold_extract(lid,amol)
    #print scaffold_list
    #return
    #sys.exit(1)

    ln_scaffold_list=len(scaffold_list)
    tmp_list.append(ln_scaffold_list)
    # making dic
    Re_dic[lid]=[]
    #print Re_dic
    #sys.exit(1)
    f_count=0
    tmp_lists2=[]
    tmp_lists3=[]

    #print type(SMILES_dic)
    #print type(id_list)

    if ln_scaffold_list>0:
        for a_sf in scaffold_list:
            if a_sf in db_dic:
                #print 'F',a_sf
                tmp_lists2.append(a_sf)
                f_count+=1

                if a_sf in SMILES_dic:
                    id_list=[]
                    id_list=SMILES_dic[a_sf]
                    if lid not in id_list:
                        id_list.append(lid)
                        SMILES_dic[a_sf]=id_list
                    else:
                        pass
                    
                else:
                    id_list=[]
                    id_list.append(lid)
                    SMILES_dic[a_sf]=id_list
                    #print SMILES_dic[a_sf] 
               

    tmp_list.append(f_count)
    tmp_list.append(tmp_lists2)
    Re_dic[lid]=tmp_list

    print 'Searching....:'+str(aidx+1)+'/'+str(ln_f)+' ,mol:'+lid+' ,Num. of scaffold:'+str(len(scaffold_list))+',Found Scaffold: '+str(f_count)
    #print Re_dic
    #sys.exit(1)
    
    return



def search_db(i_path):

    time1=time()

    # load scaffold_db
    with open('scaffold_db.pickle', 'rb') as handle:
        db_dic = pickle.load(handle)

    print 'Loading the scaffold db file'
    print 'The size of db :',len(db_dic),'\n'

    f_list=glob.glob(i_path+'*.sdf')
    f_list.sort()

    if len(f_list)==0:
        print 'No sdf files, check the path!'
        sys.exit(1)

    #print(f_list)
    #print(len(f_list))
    #sys.exit(1)
    ln_f=len(f_list)

    manager = Manager()
    Re_dic = manager.dict()
    tmp_list = manager.list()

    SMILES_dic = manager.dict()
    smi_list = manager.list()

    #print type(Re_dic)
    #print type(SMILES_dic)
    #print Re_dic2
    #sys.exit(1)
    
    Num_Of_CPU=multiprocessing.cpu_count()
    #Num_Of_CPU=2
    print Num_Of_CPU
    pool = multiprocessing.Pool(processes=(Num_Of_CPU-1))
    func=partial(core,db_dic,Re_dic,tmp_list,SMILES_dic,smi_list,f_list,ln_f)
    pool.map(func,f_list)
    pool.close()

    #print tmp_dic
    #print Re_dic
    #print SMILES_dic

    # Test Code
    '''
    smiles_d=dict(SMILES_dic)
    for key,values in smiles_d.iteritems():
        if len(values)>0:
            print key,values
    '''

    #sys.exit(1)

    #print Re_dic
    ###############################
    # For summary file output
    ###############################
    d=dict(Re_dic)
    #print 'The total inputed sdf is: ',len(Re_dic),'\n'
    print
    s_count=0
    f_count=0
    fp_for_out=open('Re_scaffold.txt','w')
    fp_for_out.write('Ligand ID\tNum. of Scaffold\tNum. of found scaffold\tSMILES'+'\n')
    for key,value  in d.iteritems():
        #print 'Ligand ID:',key,value,',The num of retrieval scaffold: ',str(len(value[1]))
        #print 'Ligand ID:',key,value,',The num of retrieval scaffold: ',str(len(value[1]))
        #fp_for_out.write(key+','+str(value[0])+','+str(value[1])+'\n')
        #print value[2]
        #res=",".join(s)
        if len(value[2])>0:
            res=",".join(value[2])
        else:
            res=''
        #print res
        #print 'Ligand ID: '+key+', Num. of Scaffold: '+str(value[0])+', Num. of found scaffold: '+str(value[1])+', Smiles: '+res
        fp_for_out.write(key+'\t'+str(value[0])+'\t'+str(value[1])+'\t'+res+'\n')
        if value[0]>0:
            f_count+=1
        if value[1]>0:
            s_count+=1
    fp_for_out.close()


    ##################################
    # For SMILES string file output
    #################################
    smiles_d=dict(SMILES_dic)
    fp_for_out=open('Re_scaffold_SMILE.txt','w')
    fp_for_out.write('SMILES\tNum. of ids\tLigand IDs'+'\n')
    for key,value  in smiles_d.iteritems():
        if len(value)>0:
            res=",".join(value)
        else:
            res=''
        fp_for_out.write(key+'\t'+str(len(value))+'\t'+res+'\n')
    fp_for_out.close()

    print '\nThe size of library: ',len(db_dic)
    print 'The total inputed sdf: ',len(Re_dic)
    print 'The num. for the input having scaffold: ',f_count 
    print 'The num. for the input matching scaffold of library: ',s_count,'('+str(float(s_count)/float(f_count)*100),'%)','\n'
    
    time2=time()
    print 'Processing time: '+str(time2-time1)
    print_date_time()
    print

    '''
    #save the dic
    with open('scaffold_db.pickle', 'wb') as handle:
        pickle.dump(tmp_dic,handle,protocol=pickle.HIGHEST_PROTOCOL)
    '''

    return

################################################################################
def main():

    '''
    #python Make_Scaffold.M.v1.py -t c -d ../Data/Input/
    parser=argparse.ArgumentParser()
    #parser.add_argument('-t',required=True, choices=['c','s'], help='to ceate scaffold db, \'c\' or to search the db, \'s\'')
    parser.add_argument('-t',required=True, choices=['c'], help='to ceate scaffold db, \'c\' or to search the db, \'s\'')
    parser.add_argument('-d',required=True,help='to target fold')
    args=parser.parse_args()

    t_path='../Data/Input/'

    if(args.t=='c'):
        #print args.t
        #print args.d
        make_db(args.d)
    '''
    t_path='../Data/Input/'
    make_db(t_path)
    '''    
    if(args.t=='s'):
        #print args.t
        #print args.d
        search_db(args.d)
    '''
if __name__=="__main__":

    main()
