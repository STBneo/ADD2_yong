#! /usr/bin/env python

"""
Module containing the eMolecule Class Constructor of the objects ligands to
filter, and the their filtering rules methods.
"""

import os
from subprocess import Popen
import pybel
from pybel import Outputfile
from pybel import Smarts
import SmartsCodes  ## Module containing the smarts dics for the groups filtering.
import GetRings     ## Module containing the Rings routines modules
import openbabel as ob

class eMolecule:

    def __init__(self,sdf=None,id=None):

        self.molecule = sdf
        self.toxic = 'Non Toxic'
        self.id = id
        self.mw = None
        self.logp = None
        self.psa = None
        self.heavy_atoms = None
        self.rotatable = None
        self.hbd = None
        self.lipinski_violations = None
        self.Veber = False
        self.Egan = False
        self.atomic = None
        self.formal_charge = None
        self.total_charge =None
        self.rigid_bond = None
        self.ring = None
        self.ring_size = None
        self.n_carbon = None
        self.n_hetero = None
        self.ratio = None
        self.amide_bond = None
        self.criterion = []
        self.SystemRingsAmount = None
        self.SizeOfMaxSystemRing = None
        self.groups_tested = {}
        self.functionnal_group = False

        
###################################################################
###################################################################
###################################################################
########                                                   ########
########     #######   #     # #      ######  #######      ########
########     #      #  #     # #      #        #           ########
########     #      #  #     # #      #         #          ########
########     #######   #     # #      ####        #        ########
########     #     #   #     # #      #            #       ########
########     #      #  #     # #      #             #      ########      
########     #       # ####### ###### ######  #######      ########
########                                                   ########
###################################################################
###################################################################
###################################################################
        
        
# -1- ###########
    def Atom_Filter(self):
        """
        Remove molecules with non allowed atoms.
        atoms is a method of the object from pybel linked to OBAtom class.
        GetAtomicNum is a method of the OBAtom class.
        Uses the list_non_allowed_atoms from SmartsCodes module.
        """

        list_atoms = self.molecule.atoms
        list_atomic = []
        for atom in list_atoms:
            num_atomic = atom.OBAtom.GetAtomicNum()
            list_atomic.append(num_atomic)
        for non_allowed_atom in SmartsCodes.list_non_allowed_atoms:
            current_count = list_atomic.count(non_allowed_atom)
            if current_count != 0:
                self.toxic = 'Toxic'
                self.criterion.append('Atom Not Allowed')
                return self.toxic
                            
        return self.toxic


# -2- ###########
    def MolecularWeight(self,inf_mw,sup_mw):
        """
        Computes Molecular Weight.
        The molwt method came from pybel module.
        """
        mw = self.molecule.molwt
        self.mw = mw
        if mw < inf_mw or mw > sup_mw:
            self.criterion.append('MW')
            self.toxic = 'Toxic'

        return self.toxic,self.mw



# -3- ###########
    def LogP(self,inf_logp,sup_logp):
        """
        Get the value of key 'LogP' from calcdesc dictionary.
        """
        current_dict = self.molecule.calcdesc()
        logp = current_dict['LogP']
        self.logp = logp
        if logp < inf_logp or logp > sup_logp:
            self.criterion.append('LogP')
            self.toxic = 'Toxic'
        del current_dict
        return self.toxic,self.logp

    def Xscore_LogP(self,mol2,xscore_path,inf_logp,sup_logp):
        """
        Compute the LogP value using the extra software X-Score
        Copyright of the X-Score program belongs to the University of Michigan.
        Renxiao Wang, Ph.D.
        Research Investigator
        Department of Internal Medicine, Hematology/Oncology Division
        University of Michigan Medical School
        Medical Science Building I, Room 2423
        1150 W. Medical Center Drive, Ann Arbor, MI 48109, U.S.A.
        Tel: (734)764-2449 Fax: (734)764-2532
        E-mail: renxiao@med.umich.edu
        """
        
        work_path = os.getcwd()
        os.chdir(xscore_path)
        output = pybel.Outputfile('mol2',mol2,'overwrite=True')
        output.write(self.molecule)
        output.close()
        
        inter_fixed = mol2[:-5]+"_fixed.mol2"
        inter_fixed_txt = mol2[:-5]+"_fixmol2.txt"
        logp_res = mol2[:-5]+"_logp_res.txt"
        os.system("xscore -fixmol2 " + mol2 + " " + inter_fixed + " > " + inter_fixed_txt)
        os.system("xscore -logp "+ inter_fixed + " " + " > " + logp_res)
        

        fi = open(logp_res)
        for lines in fi:
            s = lines.split()
            if s != [] and s[0] == "Molecule:":
                xlogp = float(s[6])
                self.logp = xlogp
                if xlogp < inf_logp or xlogp > sup_logp:
                    self.criterion.append('LogP')
                    self.toxic = 'Toxic'
                if len(s)== 7 and s[0] == '0' and s[1] == 'molecules':
                    self.logp = 'None'

        os.system(("rm %s %s %s %s")%(mol2,inter_fixed,inter_fixed_txt,logp_res))
        os.chdir(work_path)
        return self.toxic,self.logp

                     
# -4- ###########
    def HBD(self,inf_hbd,sup_hbd):
        """
        Computes Hydrogen Bond Donors number.
        Uses the SMARTS pattern methods from pybel and the Pattern_HBD from
        SmartsCodes module.
        """
        match = SmartsCodes.Pattern_HBD.findall(self.molecule)
        HDonors = len(match)
        self.hbd = HDonors
        
        if HDonors < inf_hbd or HDonors > sup_hbd:
            self.criterion.append('H-Bond Donors')
            self.toxic = 'Toxic'
        return self.toxic,self.hbd




# -5- ###########
    def HBA(self,inf_hba,sup_hba):
        """
        Computes Hydrogen Bond Acceptors number.
        Uses the SMARTS pattern methods from pybel and the Pattern_HBA from
        SmartsCodes module.
        """
        match = SmartsCodes.Pattern_HBA.findall(self.molecule)
        HAcceptors = len(match)
        self.hba = HAcceptors
        
        if HAcceptors < inf_hba or HAcceptors > sup_hba:
            self.criterion.append('H-Bond Acceptors')
            self.toxic = 'Toxic'
        return self.toxic,self.hba


# -6- ###########
    def PSA(self,inf_psa,sup_psa):
        """
        Compute the tPSA value.
        This method uses the values of atomic contributions to Polar Surface Area
        from the published method of Ertl et al (Ertl P., Rohde R., Selzer P.,
        J. Med. Chem. 2000, 43, 3714-3717).
        """
        atoms = self.molecule.atoms
        rings = self.molecule.OBMol.GetSSSR()
        psa = 0.
        bonds = self.molecule.OBMol.NumBonds()
        dicobonds = {}
        i = 0
        while i < bonds:
            dicobonds[i] = (self.molecule.OBMol.GetBond(i).GetBeginAtom().GetIdx(),self.molecule.OBMol.GetBond(i).GetEndAtom().GetIdx())
            i = i+1
        
        dicoatoms = {}
        
        for atom in self.molecule.atoms:
            Idx = atom.OBAtom.GetIdx()
            listbonds = []
            for bond in dicobonds.keys():
                start,stop = dicobonds[bond]
                if Idx == start or Idx == stop:
                    listbonds.append(bond)
            dicoatoms[Idx] = listbonds
        
        i = 0
        while i < len(atoms):
            atom = atoms[i]
            atom2test = atom.OBAtom.GetIdx()
            atomic = atom.OBAtom.GetAtomicNum()
            hcount = atom.OBAtom.ExplicitHydrogenCount()
        
            if atomic == 8 or atomic == 7 or atomic == 15 or atomic == 16:
                atom_charge = atom.OBAtom.GetFormalCharge()
                isAromatic = atom.OBAtom.IsAromatic()
     
            isIn3ring = 0 
            for ring in rings :
                if ring.Size() > 3 :
                    break
                if ring.IsInRing(i):
                    isIn3ring = 1
                    break
                if isIn3ring :
                    break
            neighbours = 0 
            nsingle = ndouble = ntriple = naromatic = 0
            bonds2test = dicoatoms[atom2test]
            for bond in bonds2test :
                neighbours += 1
                if self.molecule.OBMol.GetBond(bond).IsSingle():
                    nsingle += 1
                elif self.molecule.OBMol.GetBond(bond).IsDouble():
                    ndouble += 1
                elif self.molecule.OBMol.GetBond(bond).IsTriple():
                    ntriple += 1
                else :
                    naromatic += 1
        

            # finding the psa contribution for this fragment (atom with hydrogens)
            p = -1
            if atomic == 7 :
                if neighbours == 1 :
                    if hcount == 0 and ntriple == 1 and atom_charge == 0 :
                        p = 23.79 # N#
                    elif hcount == 1 and ndouble == 1 and atom_charge == 0 :
                        p = 23.85 # [NH]=
                    elif hcount == 2 and nsingle == 1 and atom_charge == 0 :
                        p = 26.02 # [NH2]-
                    elif hcount == 2 and ndouble == 1 and atom_charge == 1 :
                        p = 25.59 # [NH2+]=
                    elif hcount == 3 and nsingle == 1 and atom_charge == 1 :
                        p = 27.64 # [NH3+]-
                elif neighbours == 2 :
                    if hcount == 0 and nsingle == 1 and ndouble == 1 and atom_charge == 0 :
                        p = 12.36 # =N-
                    elif hcount == 0 and ntriple == 1 and ndouble == 1 and atom_charge ==0 :
                        p = 13.6 # =N#
                    elif hcount == 1 and nsingle == 2 and atom_charge == 0 and not isIn3ring :
                        p = 12.03 # -[NH]-
                    elif hcount == 1 and nsingle == 2 and atom_charge == 0 and isIn3ring :
                        p = 21.94 # -[NH]-r3
                    elif hcount == 0 and ntriple == 1 and nsingle == 1 and atom_charge == 1 :
                        p = 4.36 # -[N+]#
                    elif hcount == 1 and ndouble == 1 and nsingle == 1 and atom_charge == 1 :
                        p = 13.97 # -[NH+]=
                    elif hcount == 2 and nsingle == 2 and atom_charge == 1 :
                        p = 16.61 # -[NH2+]-
                    elif hcount == 0 and naromatic == 2 and atom_charge == 0 :
                        p = 12.89 # :[n]:
                    elif hcount == 1 and naromatic == 2 and atom_charge == 0 :
                        p = 15.79 # :[nH]:
                    elif hcount == 1 and naromatic == 2 and atom_charge == 1 :
                        p = 14.14 # :[nH+]:
                    
                elif neighbours == 3:
                
                    if hcount == 0 and nsingle == 3 and atom_charge == 0 and not isIn3ring :
                        p = 3.24 # -N(-)-
                    elif hcount == 0 and nsingle == 3 and atom_charge == 0 and isIn3ring :
                        p = 3.01 # -N(-)-r3
                    elif hcount == 0 and nsingle == 1 and ndouble == 2 and atom_charge == 0 :
                        p = 11.68 # -N(=)=
                    elif hcount == 0 and nsingle == 2 and ndouble == 1 and atom_charge == 1 :
                        p = 3.01 # =[N+](-)-
                    elif hcount == 1 and nsingle == 3 and atom_charge == 1 :
                        p = 4.44 # -[NH+](-)-
                    elif hcount == 0 and naromatic == 3 and atom_charge == 0 :
                        p = 4.41 # :[n](:):
                    elif hcount == 0 and nsingle == 1 and naromatic == 2 and atom_charge == 0 :
                        p = 4.93 # -:[n](:):
                    elif hcount == 0 and ndouble == 1 and naromatic == 2 and atom_charge == 0 :
                        p = 8.39 # =:[n](:):
                    elif hcount == 0 and naromatic == 3 and atom_charge == 1 :
                        p = 4.10 # :[n+](:):
                    elif hcount == 0 and nsingle == 1 and naromatic == 2 and atom_charge == 1 :
                        p = 3.88 # -:[n+](:):
                    elif hcount == 2 and nsingle == 3 and atom_charge == 0 :
                        p = 26.02 # [NH2]-
                    
                    elif hcount == 1 and nsingle == 3 and atom_charge == 0 and not isIn3ring : ################MODIF
                        p = 12.03 # -[NH]-
                        
                    elif hcount == 1 and naromatic == 2 and atom_charge == 0 :     ################MODIF
                        p = 15.79 # :[nH]:
                        
                elif neighbours == 4 :
                    if hcount == 0 and nsingle == 4 and atom_charge == 1 :
                        p = 0.0 # -[N+](-)(-)-

                if p < 0. : # N with non-standard valency
                    p = 30.5 - (neighbours * 8.2) + (hcount + 1.5)
                    if p < 0. :
                        p = 0.
            
            elif atomic == 8 :
                if neighbours == 1 :
                    if hcount == 0 and ndouble == 1 and atom_charge == 0 :
                        p = 17.07 # O=
                    elif hcount == 1 and nsingle == 1 and atom_charge == 0 :
                        p = 20.23 # [OH]-
                    elif hcount == 0 and nsingle == 1 and atom_charge == 1 :
                        p = 23.06 # [O-]-
                elif neighbours == 2 :
                    if hcount == 0 and nsingle == 2 and atom_charge == 0 and not isIn3ring :
                        p = 9.23 # -O-
                        
                    elif hcount == 1 and nsingle == 2 and atom_charge == 0 :################MODIF
                        p = 20.23 # [OH]-
                        
                    elif hcount ==0 and nsingle == 2 and atom_charge == 0 and isIn3ring :
                        p = 12.53 # -O-r3
                    elif hcount == 0 and naromatic == 2 and atom_charge == 0 :
                        p = 13.14 # :o:

                if p < 0. : # O with non-standard valency
                    p = 28.5 - (neighbours * 8.6) + (hcount * 1.5)
                    if p < 0. :
                        p = 0.
            
            elif atomic == 15 :
                if neighbours == 2 :
                    if hcount == 0 and ndouble == 1 and atom_charge == 0 :
                        p = 34.14 # [P](-*)=*
                    
                elif neighbours == 3 :
                    if hcount == 0 and nsingle == 3 and atom_charge == 0 and not isIn3ring :
                        p = 13.59 # -[P](-)-
                        
                elif neighbours == 4:
                    if hcount == 1 and ndouble == 1 and atom_charge == 0 and not isIn3ring :
                        p = 23.47 # [PH](-*)(-*)=*
                    elif hcount == 0 and ndouble == 1 and atom_charge == 0 and not isIn3ring :
                        p = 9.81 # [P](-*)(-*)(-*)=*

                if p < 0. : # O with non-standard valency
                    p = 28.5 - (neighbours * 8.6) + (hcount * 1.5)
                    if p < 0. :
                        p = 0.
            
            elif atomic == 16 :
                if neighbours == 1 :
                    if hcount == 0 and ndouble == 1 and atom_charge == 0 :
                        p = 32.09 # [S]=*
                    elif hcount == 1 and nsingle == 1 and atom_charge == 0 :
                        p = 38.30 # [SH]-*
                         
                elif neighbours == 2 :
                    if hcount == 0 and nsingle == 2 and atom_charge == 0 :
                        p = 25.30 # [S](-*)-*
                    elif hcount == 0 and naromatic == 2 and atom_charge == 0 :
                        p = 28.24 # :s:
                    
                elif neighbours == 3 :
                    if hcount == 0 and ndouble == 1 and atom_charge == 0 :
                        p = 19.21 # [S](-*)(-*)=*
                    elif hcount == 0 and ndouble == 1 and naromatic == 2 and atom_charge == 0 :
                        p = 21.70 # :s:

                elif neighbours == 4:
                    if hcount == 0 and ndouble == 2 and atom_charge == 0 :
                        p = 8.38 # [S](-*)(-*)=*
                if p < 0. : # O with non-standard valency
                    p = 28.5 - (neighbours * 8.6) + (hcount * 1.5)
                    if p < 0. :
                        p = 0.
                
            else:
                p = 0

            i = i +1

            psa +=p
        del dicoatoms
        del dicobonds
        self.psa = psa
        if self.psa < inf_psa or self.psa > sup_psa:
            self.criterion.append('PSA')
            self.toxic = 'Toxic'   
            
        return self.toxic,self.psa    


# -7- ###########
    def Num_Heavy_Atoms(self,inf_hva,sup_hva):
        """
        Computes heavy atoms number or the number of non-hydrogen atoms.
        OBMol is a class of the object molecule from pybel
        """
        heavy_atoms = self.molecule.OBMol.NumHvyAtoms()
        self.heavy_atoms = heavy_atoms
        
        if heavy_atoms < inf_hva or heavy_atoms > sup_hva:
            self.criterion.append('Heavy Atoms')
            self.toxic = 'Toxic'
            
        return self.toxic,self.heavy_atoms

    
# -8- ###########
    def RigidBonds(self,inf_nrb,sup_nrb):
        """
        Computes number of amide bonds and rigid bonds from pybel module
        OBMol is a class of the object molecule from pybel
        GetBond is a method of OBMol linked to the OBBond class
        IsAmide, IsInRing, IsDouble, IsTriple are methods of OBBond class.
        """ 
        
        i = 0
        nrb = 0
        n_amide = 0
        while i < self.molecule.OBMol.NumBonds():

            if self.molecule.OBMol.GetBond(i).IsAmide() and not self.molecule.OBMol.GetBond(i).IsInRing():
               n_amide =  n_amide +1
               
            if self.molecule.OBMol.GetBond(i).IsInRing():
                nrb = nrb +1
                
            if self.molecule.OBMol.GetBond(i).IsDouble() and not self.molecule.OBMol.GetBond(i).IsInRing():
                nrb = nrb +1
                
            if self.molecule.OBMol.GetBond(i).IsTriple() and not self.molecule.OBMol.GetBond(i).IsInRing():
                nrb = nrb +1
                
            i = i+1

        self.rigid_bond = nrb
        self.amide_bond = n_amide
        self.rigid_bond = self.rigid_bond + self.amide_bond
        if self.rigid_bond < inf_nrb or self.rigid_bond > sup_nrb:
            self.criterion.append('Rigid Bonds')
            self.toxic = 'Toxic'
    
        return self.toxic,self.rigid_bond,self.amide_bond

 

# -9- ###########
    def RotatableBonds(self,inf_nbb,sup_nbb):
        """
        Computes Rotatable Bonds number from pybel module
        OBMol is a class of the object molecule from pybel
        NumRotors is a method of OBMol linked to the OBBond class.
        """

        rotatable_bonds = self.molecule.OBMol.NumRotors()
        rotatable_bonds = rotatable_bonds - self.amide_bond
        if rotatable_bonds < 0:
            rotatable_bonds = 0
            
        self.rotatable = rotatable_bonds

        if rotatable_bonds < inf_nbb or rotatable_bonds > sup_nbb:
            self.criterion.append('Rotatable Bonds')
            self.toxic = 'Toxic'

        return self.toxic,self.rotatable



##################
    def Rings_Counter(self):
        """
        """

        AllRings = GetRings.CreateRings(self.molecule)
        if AllRings != []:
            AllBonds = self.molecule.OBMol.NumBonds()
            dico_rings = GetRings.CreateRingBonds(AllRings,AllBonds,self.molecule)
            dico_neighbour_ring , dico_bond_junct = GetRings.CreateNeighbourList(dico_rings)
            dico_cluster_global = GetRings.CreateClusterGlobal(dico_neighbour_ring,AllRings)
            dico_cluster_global = GetRings.Aggregates(dico_cluster_global)
            SystemRings, SystemRingsAmount = GetRings.GetItRight(dico_cluster_global)
            BondsInCluster = GetRings.CountNeighborBondsInCluster(dico_bond_junct, SystemRings)
            SizeOfMaxSystemRing, ID_cluster = GetRings.CalculateNbAtomsSystemRings(SystemRings,BondsInCluster,AllRings)
            del(AllBonds,dico_rings,dico_neighbour_ring,dico_cluster_global,SystemRings,BondsInCluster,ID_cluster)
        else:
            SystemRingsAmount = 0
            SizeOfMaxSystemRing = 0
            del(AllRings)

        self.SystemRingsAmount = SystemRingsAmount
        self.SizeOfMaxSystemRing = SizeOfMaxSystemRing
        return SystemRingsAmount,SizeOfMaxSystemRing


       
# -10- ###########
    def RuleOfRings(self,inf_nc,sup_nc,max_ring):
        """
        """
        if self.SystemRingsAmount <inf_nc or self.SystemRingsAmount > sup_nc:
            self.criterion.append('Ring Number')
            self.toxic = 'Toxic'
            
        if self.SizeOfMaxSystemRing > max_ring:
            self.criterion.append('Max Ring Size')
            self.toxic = 'Toxic'
            
        return self.toxic            


# -11- ###########    
    def Count_Charge(self,inf_cf,sup_cf):
        """
        Computes and count the formal charges in molecule
        atoms is a method of the object from pybel linked to OBAtom class
        GetFormalCharge is a method of the OBAtom class
        """

        list_of_atoms = self.molecule.atoms
        charge_counter = 0
        for atom in list_of_atoms:
            formal_charge = atom.OBAtom.GetFormalCharge()
            if formal_charge != 0:
                charge_counter = charge_counter+1

        self.formal_charge = charge_counter
        if self.formal_charge < inf_cf or self.formal_charge > sup_cf:
            self.criterion.append('Formal Charge')
            self.toxic = 'Toxic'

        return self.toxic,self.formal_charge
    


# -12- ###########
    def Total_Charge(self,inf_sc,sup_sc):
        """
        Computes charge of the molecule
        atoms is a method of the object from pybel linked to OBAtom class
        GetFormalCharge is a method of the OBAtom class
        """

        total_charge = 0
        for atom in self.molecule.atoms:
            current_charge = atom.OBAtom.GetFormalCharge()
            total_charge = total_charge + current_charge

        self.total_charge = total_charge
        if total_charge < inf_sc or total_charge > sup_sc:
            self.criterion.append('Total Charge')
            self.toxic = 'Toxic'

        return self.toxic,self.total_charge


# -13- ###########
    def Count_Atoms(self,inf_c,inf_h,inf_r,sup_r):
        """
        Computes the number of carbon atoms,the number of heteroatoms and calculates the ratio between hetero and carbon atoms
        atoms is a method of the object from pybel linked to OBAtom class
        IsHeteroatom and IsCarbon are methods of the OBAtom class"""

        n_carbon = 0
        n_hetero = 0
        for atom in self.molecule.atoms:
            if atom.OBAtom.IsCarbon():
                n_carbon = n_carbon+1
            elif not atom.OBAtom.IsHydrogen():
                n_hetero = n_hetero +1
                
        if n_carbon == 0:
            ratio = 0

        else:
            ratio = float(n_hetero)/float(n_carbon)

        self.n_carbon = n_carbon
        self.n_hetero = n_hetero
        self.ratio = ratio

        if n_carbon < inf_c or n_hetero < inf_h:
            self.criterion.append('Number of C or heteroatoms')
            self.toxic = 'Toxic'

        if ratio < inf_r or ratio > sup_r:
            self.criterion.append('Ratio H/C')
            self.toxic = 'Toxic'

        return self.toxic,self.n_carbon,self.n_hetero,self.ratio




###############################################################
###############################################################
###############################################################
#######                                                 #######
#######     ##### #  #    ##### ##### #####   #####     #######
#######     #        #      #   #     #    #  #         #######
#######     ###   #  #      #   ###   #####     #       #######
#######     #     #  #      #   #     #   #      #      #######
#######     #     #  #####  #   ##### #    #  #####     #######
#######                                                 #######
###############################################################
###############################################################
###############################################################    
    
# -14- ###########
    def Veber_Rule(self,sup_psa,sup_nbb):
        """
        Compute the extra rule from Veber et al.
        (D.F. Veber,S.R. Johnson,HY.Cheng,B.R. Smith,K.W. Ward,K.D. Kopple
        J. Med. Chem., 45 (12), 2615 -2623, 2002. 10.1021)
        """
        if sup_psa > 140 and sup_nbb > 10:
            return self.toxic,self.Veber
                    
        if self.psa > 140 or self.rotatable > 10:
            self.criterion.append('Veber violation')
            self.toxic = 'Toxic'
            self.Veber = True
            
        return self.toxic,self.Veber


# -15- ###########
    def Egan_Rule(self,sup_psa,sup_logp):
        """
        Compute the bioavailability measure according to Egan et al.
        (Egan WJ, Merz KM Jr, Baldwin JJ.
        J Med Chem. 2000 Oct 19;43(21):3867-77)
        """
        if sup_psa > 131.6 and sup_logp > 5.88:
            return self.toxic,self.Egan
        
        if self.psa > 131.6 or self.logp > 5.88:
            self.criterion.append('Egan violation')
            self.toxic = 'Toxic'
            self.Egan = True
            
        return self.toxic,self.Egan
    

# -16- ###########
    def Lipinski_Violations(self,max_lipinski):
        """
        Computes number of maximum violations of Lipinski's Rule of 5.
        """
        number_of_violations = 0
        if self.hbd > 5:
            number_of_violations = number_of_violations +1
            
        if self.hba > 10:
            number_of_violations = number_of_violations +1
            
        if self.mw > 500:
            number_of_violations = number_of_violations +1

        if self.logp > 5:
            number_of_violations = number_of_violations +1

        if number_of_violations > max_lipinski:
            self.criterion.append('Lipinski violations')
            self.toxic = 'Toxic'
            
        self.lipinski_violations = number_of_violations
        
        return self.toxic,self.lipinski_violations





###############################################################################
###############################################################################
###############################################################################
########                                                               ########
########      ####### #######   ####### #     # #######  ########      ########
########      #       #      #  #     # #     # #      # #             ########
########      # ##### #      #  #     # #     # #      #   #           ########
########      # #   # #######   #     # #     # #######      #         ########
########      #     # #     #   #     # #     # #              #       ######## 
########      ####### #      #  ####### ####### #        ########      ######## 
########                                                               ########
###############################################################################
###############################################################################
###############################################################################



    
# -17- ###########
    def Group_Filter_Warhead(self,list_Groups2Filter):
        '''
        Computes the filtering of the "Warheads" compounds from Rishton,
        "Rishton GM, Reactive compounds and in vitro false positives in HTS,
        DDT Vol.2,No.9 September 1997."
        Uses the dico_Warheads from SmartsCodes module, and the SMARTS pattern
        methods from pybel.
        '''
        for groups in list_Groups2Filter:
            rule,group = groups
            if SmartsCodes.dico_Warheads.has_key(group):
                current_pattern = Smarts(SmartsCodes.dico_Warheads[group])
                list_match = current_pattern.findall(self.molecule)
                amount = len(list_match)
                self.groups_tested[group]=amount

                if list_match != []:
                    self.criterion.append('Warhead '+group)
                    self.toxic = 'Toxic'
                    self.functionnal_group = True
                    
        return self.toxic,self.functionnal_group,self.groups_tested,self.criterion
                
 


# -18- ###########
    def Group_Filter_Frequent_Hitters(self,list_Groups2Filter):
        '''
        Computes the filtering of the "Frequents Hitters" compounds from Roche,
        "Roche O., Development of a Virtual Screening Method for Identification of
        Frequent Hitters in Compound Libraries, J.Med.Chem., 2002,45,137-142."
        Uses the dico_Frequent_Hitters from SmartsCodes module, and the SMARTS
        pattern methods from pybel.
        '''
        for groups in list_Groups2Filter:
            rule,group = groups
            if SmartsCodes.dico_Frequent_Hitters.has_key(group):
                current_pattern = Smarts(SmartsCodes.dico_Frequent_Hitters[group])
                list_match = current_pattern.findall(self.molecule)
                amount = len(list_match)
                self.groups_tested[group]=amount

                if list_match != []:
                    self.criterion.append('Frequent Hitter '+group)
                    self.toxic = 'Toxic'
                    self.functionnal_group = True
            
        return self.toxic,self.functionnal_group,self.groups_tested,self.criterion

# -20- ###########
    def Group_Filter_Aggregators(self,list_Groups2Filter):
        '''
        Computes the filtering of the "Aggregators" compounds from McGovern,
        "A Common Mechanism Underlying Promiscuous Inhibitors from Virtual and
        High-Troughput Screening, J.Med.Chem,2002,45,1712-1722."
        Uses the dico_Aggregators from SmartsCodes module, and the SMARTS pattern
        methods from pybel.
        '''
        for groups in list_Groups2Filter:
            rule,group = groups
            if SmartsCodes.dico_Aggregators.has_key(group):
                current_pattern = Smarts(SmartsCodes.dico_Aggregators[group])
                list_match = current_pattern.findall(self.molecule)
                amount = len(list_match)
                self.groups_tested[group]=amount

                if list_match != []:
                    self.criterion.append('Aggregator '+group)
                    self.toxic = 'Toxic'
                    self.functionnal_group = True
                               
        return self.toxic,self.functionnal_group,self.groups_tested,self.criterion


# -21- ###########
    def Group_Filter_Chemicals_Group(self,list_Groups2Filter):
        '''
        Computes the filtering of the others chemicals groups known to be toxic.
        Uses the dico_Chemicals_Groups from SmartsCodes module, and the SMARTS
        pattern methods from pybel.
        '''
        for groups in list_Groups2Filter:
            
            rule,group = groups
            rule = int(rule)
            if SmartsCodes.dico_Chemicals_Groups.has_key(group):
                current_pattern = Smarts(SmartsCodes.dico_Chemicals_Groups[group])
                list_match = current_pattern.findall(self.molecule)
                amount = len(list_match)
                self.groups_tested[group]=amount

                if amount > rule:
                    self.criterion.append('Chemical Group '+group)
                    self.toxic = 'Toxic'
                    self.functionnal_group = True
                                                    
        return self.toxic,self.functionnal_group,self.groups_tested,self.criterion
