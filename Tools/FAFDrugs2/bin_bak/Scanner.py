#! /usr/bin/env python


import pybel
import popen2
import os


################################################################## 
def Desalting(output,molecule):
    """
    Reading and if necessary remove salts in file_in and write a
    new file_out .sdf with pybel module StripSalts() from OBMol class
    """
    i = 0
    if molecule.OBMol.StripSalts():
        i = 1
        output.write(molecule)
    else:
        output.write(molecule)

    return i
        

        
##################################################################         
def DoubleRemove(sdfFileName,sdfout):

    molecules = pybel.readfile('sdf',sdfFileName)
    Output = pybel.Outputfile('sdf',sdfout,'overwrite=True')
    dico_smi = {}
    i = 0
    for mols in molecules:
        #print(mols)
        smi = mols.write().split()[0]
        if dico_smi.has_key(smi):
            i = i+1
            pass
        else:
            dico_smi[smi] = mols.write().split()[1]
            Output.write(mols)
    print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'        
    print '     ---------> ',i,'duplicates found in this database....'
    print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
    Output.close()
    
    del molecules
    return i


##################################################################
def get_pos_sdf(file):
 
    """
    Creating the index of starting and ending positions of each ligand in
    a (.sdf) file. The index contains {ID_Number:(start,stop)}.

    """
    fh = open(file)
    pos = fh.tell()
    line = fh.readline()
    flag = 0
    dic_pos = {}

    while line != '':
        line = line[:-1]
        if flag == 0:
            start = pos
            pos = fh.tell()
            ID = line
            line = fh.readline()
            flag = 1
    
        else:
            if line == '$$$$':
                stop = pos
                flag = 0
                dic_pos[ID]=(start,stop)
                pos = fh.tell()
                line = fh.readline()
            else:
                pos = fh.tell()
                line = fh.readline()
                
    fh.close()
    return dic_pos


##################################################################
def get_params(fhi):
 
    dic_param = {}

    for elem in fhi.readlines():
        #print(elem)
        temp_split = elem.split()
        #print(temp_split) #['inf_sc', '=', '-2']
        if len(temp_split) > 1:
            if temp_split[0] == 'file':
                dic_param['filein'] = temp_split[2]
            elif temp_split[0] == 'max_lipinski':
                dic_param['max_lipinski'] = int(temp_split[2])    
            elif temp_split[0] == 'inf_mw':
                dic_param['inf_mw'] = float(temp_split[2])
            elif temp_split[0] == 'sup_mw':
                dic_param['sup_mw'] = float(temp_split[2])
            elif temp_split[0] == 'inf_hbd':
                dic_param['inf_hbd'] = int(temp_split[2])
            elif temp_split[0] == 'sup_hbd':
                dic_param['sup_hbd'] = int(temp_split[2])
            elif temp_split[0] == 'inf_hba':
                dic_param['inf_hba'] = int(temp_split[2])
            elif temp_split[0] == 'sup_hba':
                dic_param['sup_hba'] = int(temp_split[2])
            elif temp_split[0] == 'inf_hva':
                dic_param['inf_hva'] = int(temp_split[2])
            elif temp_split[0] == 'sup_hva':
                dic_param['sup_hva'] = int(temp_split[2])
            elif temp_split[0] == 'inf_nbb':
                dic_param['inf_nbb'] = int(temp_split[2])
            elif temp_split[0] == 'sup_nbb':
                dic_param['sup_nbb'] = int(temp_split[2])
            elif temp_split[0] == 'inf_nrb':
                dic_param['inf_nrb'] = int(temp_split[2])
            elif temp_split[0] == 'sup_nrb':
                dic_param['sup_nrb'] = int(temp_split[2])
            elif temp_split[0] == 'inf_nc':
                dic_param['inf_nc'] = int(temp_split[2])
            elif temp_split[0] == 'sup_nc':
                dic_param['sup_nc'] = int(temp_split[2])
            elif temp_split[0] == 'max_ring':
                dic_param['max_ring'] = int(temp_split[2])
            elif temp_split[0] == 'inf_psa':
                dic_param['inf_psa'] = float(temp_split[2])
            elif temp_split[0] == 'sup_psa':
                dic_param['sup_psa'] = float(temp_split[2])
            elif temp_split[0] == 'xscore':
                dic_param['xscore'] = temp_split[2]
            elif temp_split[0] == 'gnuplot':
                dic_param['plotting'] = temp_split[2]
            elif temp_split[0] == 'xscore_path':
                dic_param['xscore_path'] = temp_split[2]    
            elif temp_split[0] == 'inf_logp':
                dic_param['inf_logp'] = float(temp_split[2])
            elif temp_split[0] == 'sup_logp':
                dic_param['sup_logp'] = float(temp_split[2])
            elif temp_split[0] == 'inf_cf':
                dic_param['inf_cf'] = int(temp_split[2])
            elif temp_split[0] == 'sup_cf':
                dic_param['sup_cf'] = int(temp_split[2])
            elif temp_split[0] == 'inf_sc':
                dic_param['inf_sc'] = int(temp_split[2])
            elif temp_split[0] == 'sup_sc':
                dic_param['sup_sc'] = int(temp_split[2])
            elif temp_split[0] == 'inf_c':
                dic_param['inf_c'] = int(temp_split[2])
            elif temp_split[0] == 'inf_h':
                dic_param['inf_h']= int(temp_split[2])
            elif temp_split[0] == 'inf_r':
                dic_param['inf_r'] = float(temp_split[2])
            elif temp_split[0] == 'sup_r':
                dic_param['sup_r'] = float(temp_split[2])
                
            elif temp_split[0] == 'group_param_file':
                dic_param['group_param_file'] = temp_split[2]
                
    return dic_param



##################################################################
def GetListGroups2Filter(group_param):
    
    fh_group_param = open(group_param)
    list_groups2filter = []
    
    for line in fh_group_param:
        if line[0] != '#':
            list_groups2filter.append((line.split()[0],line.split()[1]))
            
    return list_groups2filter



##################################################################
def write_toxic(fhi,dump,fho_toxic,ID):

    start,stop = dump[ID]
    fhi.seek(start)
    pos = fhi.tell()                    
    line = fhi.readline()
    while pos != stop:
        fho_toxic.write(line)   
        line = fhi.readline()
        pos = fhi.tell()
        
    fho_toxic.write(line)   
    fho_toxic.write('$$$$')
    fho_toxic.write('\n')
    

        
##################################################################
def write_non_toxic(fhi,dump,fho_nontoxic,ID):

    start,stop = dump[ID]
    fhi.seek(start)
    pos = fhi.tell()                    
    line = fhi.readline()
    while pos != stop:
        fho_nontoxic.write(line)    
        line = fhi.readline()
        pos = fhi.tell()
    fho_nontoxic.write('\n')
    fho_nontoxic.write('$$$$')
    fho_nontoxic.write('\n')

##################################################################
def analyse(bank,toxic,nontoxic):

    cmd = "grep -wc '$$$$' "

    fhin,fhout = popen2.popen2(cmd+toxic)
    for line in fhin:
        nb_toxic = line[:-1]
        
    fhin,fhout = popen2.popen2(cmd+nontoxic)
    for line in fhin:
        nb_nontoxic = line[:-1]

    fhin,fhout = popen2.popen2(cmd+bank)
    for line in fhin:
        nb_total = line[:-1]
        
    print "\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
    print " Number of TOXIC molecules = "+nb_toxic
    print " Number of NON TOXIC molecules = "+nb_nontoxic
    print " Number of molecules processed = "+nb_total
    print "\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
    
