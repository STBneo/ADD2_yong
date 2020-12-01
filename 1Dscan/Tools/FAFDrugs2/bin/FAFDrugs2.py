#! /usr/bin/env python

"""
This is the main of the ADME-tox package.
Command line : FAFDrugs2.py <'file.param'>
"""
'''
print '\n\n'
print '\t\t####################################'
print '\t\t##                                ##'
print '\t\t##          FAF-Drugs2            ##'
print '\t\t##             -----              ##'
print '\t\t##    Written By David Lagorce    ##'
print '\t\t##             -----              ##'
print '\t\t##           July 2008            ##'
print '\t\t##                                ##'
print '\t\t####################################'
print '\n\n\n'
'''

##################
import CreateMol
import Scanner
import sys
import os
import os.path
import shutil
import cPickle
import SmartsCodes
import time
import Plotting
import time
import pybel

##########################
def logp_method(xscore,amount):

    logp_method = None
    if amount <= 10000:
        if xscore == 'off':
            #print ' -----> Xscore param is off. LogP will be calculated by OpenBabel method.\n'
            logp_method = 'pybel'
        elif xscore == 'on':
            #print ' -----> Xscore param is on. LogP will be calculate by Xscore method.\n        Be sure you have the X-Score licence in your home directory !!\n        Otherwise close the application and lock off this param to prevent a program failure.\n'
            logp_method = 'xscore'
        else:
            #print ' -----> param.file problem. Edit file and check <xscore> value ("on" or "off")\n'
            sys.exit(1)

    else:
        if xscore == 'off':
            #print ' -----> Xscore param is off. LogP will be calculate by OpenBabel method.\n'
            #print '        But, your database exceed 10000 molecules. With large database you may have a program failure due to memory leak.'
            #print '        Hence, the program will be stopped. Go to UserGuide to see how to obtain X-Score application.\n'
            sys.exit(1)
        elif xscore == 'on':
            #print ' -----> Xscore param is on. LogP will be calculate by Xscore method.\n'
            #print '        Be sure you have the X-Score licence in your home directory !!'
            #print '        Otherwise close the application and lock off this param to prevent a program failure.'
            logp_method = 'xscore'
        else:
            #print ' -----> <file.param> problem. Edit file and check <xscore> value ("on" or "off")\n'
            sys.exit(1)

    return logp_method



##########################
def timing(process):
    try:
        hours = str(processing/60.0).split('.')[0]
        min = '0.'+str(processing/60.0).split('.')[1]
        newmin = str(float(min)*60).split('.')[0]
        timing = '----------->  Filtering done in '+hours+' hours and '+newmin+' minutes.'
    except:
        hours = str(processing/60)
        timing = '----------->  Filtering done in '+hours+' hours.'

    return timing



#####################################################
#####################################################
#####################################################
########                                      #######
########     ##     ## ######## # ##     #    #######
########     # #   # # #      #   # #    #    #######
########     #  # #  # #      # # #  #   #    #######
########     #   #   # ######## # #   #  #    #######
########     #       # #      # # #    # #    #######
########     #       # #      # # #     ##    #######      
########     #       # #      # # #     ##    #######
########                                      #######
#####################################################
#####################################################
#####################################################




if __name__ == '__main__':

    start = time.time()
    

    try:
        fh_param = open(sys.argv[1])
    
    except IOError,error:
        print error
    
    params = Scanner.get_params(fh_param)
    
    #filein = params['filein']
    filein = sys.argv[2]
    
    group_param = params['group_param_file']
    list_Groups2Filter = Scanner.GetListGroups2Filter(group_param)
    ext = filein[-3:]
    file_out_NoSalts = filein[:-4]+'_Nosalts.sdf'

    #time_split1 = time.asctime().split()
    #time_split2 = time_split1[3].split(':')
    #output_dir = 'FAFDrugs2_OUTPUT_'+time_split1[1]+'_'+time_split1[2]+'_'+time_split1[4]+'_'+time_split2[0]+'h'+time_split2[1]+'m'+time_split2[2]
    output_dir = filein.split('.')[0]
    os.mkdir(output_dir+'/')
    
    file_toxic = filein[:-4]+'_toxic.sdf'
    file_non_toxic = filein[:-4]+'_non_toxic.sdf'

    fho_toxic = open(file_toxic,'w')
    fho_nontoxic = open(file_non_toxic,'w')
#################################
#################################
#####  DUPLICATES REMOVING ######

    file_without_duplicates = filein[:-4]+'_without_duplicates.sdf'    

    #print '\n\n'
    #print '----> Removing duplicates ....\n'
    flag = Scanner.DoubleRemove(filein,file_without_duplicates)
    if flag == 0:
        #print '\n---------> the original file "',filein,'" will be processed....\n'
        os.remove(file_without_duplicates)
    else:
        filein = file_without_duplicates
    #print '\n'
#################################
#################################
########### DESALTING ###########
    #print '----> Reading Bank File ....\n'
    pybel_file = CreateMol.ReadSDF(ext,filein)
       
    #print '----> Removing Salts ......\n'
    output = pybel.Outputfile('sdf',file_out_NoSalts,overwrite=True)
    ligand_amount = 0
    salts_amount = 0
    for molecule in pybel_file:
        ligand_amount = ligand_amount+1
        res_salt = Scanner.Desalting(output,molecule)
        if res_salt == 1:
            salts_amount = salts_amount+1
    #print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'        
    #print '     ---------> ',salts_amount,'molecules with salts found in this database....'
    #print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n'
            
    output.close()
    #print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@' 
    #print '     --------->  Your database contains',ligand_amount,'ligands to filter .....'
    #print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
#################################
#################################
########## PARSING ##############
    #print '\n----> Dumping the bank....\n'
    dic_positions = Scanner.get_pos_sdf(filein)
    file_dict_dump = filein[:-4] + '.dump'
    dict_dump = open(file_dict_dump,'w')
    cPickle.dump(dic_positions,dict_dump)
    dict_dump.close()



#################################
#################################
########## FILTERING ############
    del(pybel_file)
    pybel_filtering_file = CreateMol.ReadSDF(ext,file_out_NoSalts)
    
    fh_dump = open(file_dict_dump,'r')
    dump = cPickle.load(fh_dump)
    fhi = open(filein)

    ###########################
    ###    RESULTS TABLE    ###
    file_table = filein[:-4]+'_'+'results.table'
    #print(file_table)
    if os.path.isfile(file_table):
        os.remove(file_table)
    fh_table = open(file_table,'w')
    #columns = 'Ligand\tID\tMW\tLogP\tPSA\tRotatableB\tRigidB\tHBD\tHBA\tRings\tMaxSizeRing\tCharge\tTotal Charge\tHeavyAtoms\tCarbonAtoms\tHeteroAtoms\tratioH/C\tLipinski_Violation\tVeber_Violation\tEgan_Violation\tFunctionnal_Group\tToxicity'
    columns = 'ID\tMW\tLogP\tPSA\tRotatableB\tRigidB\tHBD\tHBA\tRings\tMaxSizeRing\tCharge\tTotal Charge\tHeavyAtoms\tCarbonAtoms\tHeteroAtoms\tratioH/C\tLipinski_Violation\tVeber_Violation\tEgan_Violation\tFunctionnal_Group\tToxicity'
    #columns = 'Ligand\tID\tMW\tLogP\tHBD\tHBA\tLipinski_Violation\tFunctionnal_Group\tToxicity'
    #fh_table.write(columns)
    #fh_table.write('\n')
    
    ###########################
    ###   GROUPS   TABLE    ###
    file_grouptable = filein[:-4]+'_groups.table'
    if os.path.isfile(file_grouptable):
        os.remove(file_grouptable)
    fh_grouptable = open(file_grouptable,'w')
    fh_fafinfo = open(filein[:-4]+'_summary.txt','w')
    group_columns = 'ID\t'
    for group in list_Groups2Filter:
        group_columns += (group[1]+'\t')
    group_columns += '\n'
    fh_grouptable.write(group_columns)

    xscore = params['xscore']
    logp_method = logp_method(xscore,ligand_amount)
    
    #print '----> Filtering in progress....\n'

    i = 1
    for lig in pybel_filtering_file:
        ligand = CreateMol.Create_Ligand(lig)
        
        dico_groups = {}
        id = ligand.id
        
        # -1- #
        toxic,groups,dico_group_tested,criterion = ligand.Group_Filter_Warhead(list_Groups2Filter)
        
        # -2- #
        toxic,groups,dico_group_tested,criterion = ligand.Group_Filter_Frequent_Hitters(list_Groups2Filter)
        
        # -3- #
        toxic,groups,dico_group_tested,criterion = ligand.Group_Filter_Aggregators(list_Groups2Filter)
        
        # -4- #
        toxic,groups,dico_group_tested,criterion = ligand.Group_Filter_Chemicals_Group(list_Groups2Filter)
        
        
        ligand.molecule.OBMol.DeleteHydrogens()
        
        ligand.molecule.OBMol.AddHydrogens(bool(0),bool(0))
        

        # -5- #
        toxic = ligand.Atom_Filter()
        
        # -6- #
        toxic,mw = ligand.MolecularWeight(params['inf_mw'],params['sup_mw'])
        
        # -7- #
        if mw > 5000:
            logp=None
            #print '\n----> Molecular weight for the molecule',id,'is > 5000, XlogP can not be computed and is setting to None ...\n'
        else:
            logp = None
            if logp_method == 'pybel':
                toxic,logp = ligand.LogP(params['inf_logp'],params['sup_logp'])
  
            elif logp_method == 'xscore':
                mol2file = 'current_ligand_from_'+filein[:-3]+'mol2'
                xscore_path = params['xscore_path']
                toxic,logp = ligand.Xscore_LogP(mol2file,xscore_path,params['inf_logp'],params['sup_logp'])
        # -8- #
        toxic,HBDonors = ligand.HBD(params['inf_hbd'],params['sup_hbd'])
        
        # -8- #
        toxic,HBAcceptors = ligand.HBA(params['inf_hba'],params['sup_hba'])
        
        # -10- ##
        toxic,psa = ligand.PSA(params['inf_psa'],params['sup_psa'])
                
        # -11- ##
        toxic,heavy_atoms = ligand.Num_Heavy_Atoms(params['inf_hva'],params['sup_hva'])
        
        # -12- ##
        toxic,rigid_bonds,amide_bonds = ligand.RigidBonds(params['inf_nrb'],params['sup_nrb'])
        
        # -13- ##
        toxic,rotatable_bonds = ligand.RotatableBonds(params['inf_nbb'],params['sup_nbb'])
        
        # -14- ##
        SystemRing,SizeSystem = ligand.Rings_Counter()
        toxic = ligand.RuleOfRings(params['inf_nc'],params['sup_nc'],params['max_ring'])

        ligand.molecule.OBMol.DeleteHydrogens()
        ligand.molecule.OBMol.AddHydrogens()
        
        # -15- ##
        toxic,formal_charge = ligand.Count_Charge(params['inf_cf'],params['sup_cf'])
        
        # -16- ##
        toxic,total_charge = ligand.Total_Charge(params['inf_sc'],params['sup_sc'])
        
        # -17- ##
        toxic,n_carbon,n_hetero,ratioH_C = ligand.Count_Atoms(params['inf_c'],params['inf_h'],params['inf_r'],params['sup_r'])

        # -18- ##
        toxic,veber = ligand.Veber_Rule(params['sup_psa'],params['sup_nbb'])

        # -19- ##
        toxic,egan = ligand.Egan_Rule(params['sup_psa'],params['sup_logp'])

        toxic,lipinski_violations = ligand.Lipinski_Violations(params['max_lipinski'])


        #new_line = ('%i\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%3s\t%s\t%s\t%s\t%5.5s\t%s\t%s\t%s\t%s\t%s')%(i,id,mw,logp,psa,rotatable_bonds,rigid_bonds,HBDonors,HBAcceptors,SystemRing,SizeSystem,formal_charge,total_charge,heavy_atoms,n_carbon,n_hetero,ratioH_C,lipinski_violations,veber,egan,groups,toxic)
        new_line = ('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%3s\t%s\t%s\t%s\t%5.5s\t%s\t%s\t%s\t%s\t%s')%(id,mw,logp,psa,rotatable_bonds,rigid_bonds,HBDonors,HBAcceptors,SystemRing,SizeSystem,formal_charge,total_charge,heavy_atoms,n_carbon,n_hetero,ratioH_C,lipinski_violations,veber,egan,groups,toxic)
        #new_line = ('%i\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s')%(i,id,mw,logp,HBDonors,HBAcceptors,lipinski_violations,groups,toxic)

        dico_groups[id] = dico_group_tested


        line = id+'\t'
        for test in list_Groups2Filter:
            grp2test = test[1]
            if dico_group_tested.has_key(grp2test):
                line += str(dico_group_tested[grp2test])+'\t'
        line += '\n'
        fh_grouptable.write(line)
        
        fh_table.write(new_line)
        fh_table.write('\n')
    
        if toxic == 'Toxic':
            Scanner.write_toxic(fhi,dump,fho_toxic,id)
        if toxic == 'Non Toxic':
            Scanner.write_non_toxic(fhi,dump,fho_nontoxic,id)

        if i%100 == 0:
            #print '----->',i,'molecules processed of',ligand_amount
            pass

        i = i+1
        smile = lig.write()
        fh_fafinfo.write(id+'\t'+smile+'\t')
        line_criterion = ''
        if criterion !=[]:
            for crit in criterion:
                line_criterion+= crit+','
            line_criterion = line_criterion[:-1]
        else:
            line_criterion+= 'PASS'
        fh_fafinfo.write(line_criterion+'\n')
        del(lig,ligand,id,toxic,mw,HBDonors,HBAcceptors)
                  
    fh_dump.close()
    fhi.close()
    fho_toxic.close()
    fho_nontoxic.close()
    fh_table.close()
    fh_grouptable.close()
    fh_fafinfo.close()
    os.remove(file_dict_dump)
    
    Scanner.analyse(filein,file_toxic,file_non_toxic)
    
    shutil.move(file_toxic,output_dir)
    shutil.move(file_non_toxic,output_dir)
    shutil.move(file_out_NoSalts,output_dir)
    shutil.move(file_table,output_dir)
    shutil.move(file_grouptable,output_dir)
    #faf_param_move = sys.argv[1]+'_used'
    #shutil.copy(sys.argv[1],faf_param_move)
    #shutil.move(faf_param_move,output_dir)
    #group_param_move = group_param+'_used'
    #shutil.copy(group_param,group_param_move)
    #shutil.move(group_param_move,output_dir)
    
    try:
        shutil.move(file_without_duplicates,output_dir)
        
    except:
        pass

    shutil.move(filein[:-4]+'_summary.txt',output_dir)
    
    path = os.getcwd()
    os.chdir(output_dir)
    
    end = time.time()
    processing = (end - start)/60
    #print timing(processing)
    #print "\n"

    gnuplot = params['plotting']
    if gnuplot == 'on':
        #print '\n------------> Histograms have been computed by GnuPlot\n'
        Plotting.logp_parsing(ligand_amount)
        Plotting.mw_parsing(ligand_amount)
        Plotting.psa_parsing(ligand_amount)
        Plotting.rigid_parsing(ligand_amount)
        Plotting.rotatable_parsing(ligand_amount)
        Plotting.HBD_parsing(ligand_amount)
        Plotting.HBA_parsing(ligand_amount)
        Plotting.Rings_parsing(ligand_amount)
        os.chdir(path)
