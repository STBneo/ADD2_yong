#! /usr/bin/env python




#################################
def CreateRings(mol):
    """
    Creates one list containing all identified rings by pybel module with SSSR algorithm.
    """
    
    rings = []
    listrings = mol.OBMol.GetSSSR()
    if listrings != []:
        for ring in listrings:
            rings.append(ring)

    return rings



#################################
def CreateRingBonds(rings,numbonds,mol):
    """
    Creates a dictionnary which contains {ringA:[bonds included in ringA]} for all rings
    """

    dico_rings = {}
    i = 0
    j = 0
    while j < len(rings):
        ring = rings[j]
        list_bond = []
        i = 0
        while i < numbonds:
            if ring.IsMember(mol.OBMol.GetBond(i)):
                list_bond.append(i)
            i = i+1
        dico_rings[j] = list_bond
        j = j+1
    return dico_rings



#################################
def CreateNeighbourList(dico_rings):
    """
    Creates two dictionnaries:
    1) dico_neighbour_ring, containing for each rings (key) a list (value) containing all the neightbors rings of the ring tested.
    {ringA:[ringB,ringC];ringB:[ringA];ringC:[ringA]}
    2) dico_bond_junct, containing for each bonds detected (key) a list (value) containing all the rings involved.
    {bondX:[ringA,ringB]}
    """
    
    dico_neighbour_ring = {}
    dico_bond_junct = {}

    for ring_i in range(0,len(dico_rings)):
        list_temp = []
        for ring_j in range(0,len(dico_rings)):
            if ring_i != ring_j:               
                for bond_i in dico_rings[ring_i]: 
                    for bond_j in dico_rings[ring_j]:
                        if bond_i == bond_j:  
                            list_temp.append(ring_j)
                            dico_bond_junct[bond_i] = [ring_i,ring_j] 
                            
        if list_temp != []:
            dico_neighbour_ring[ring_i] = list_temp 

    
    return dico_neighbour_ring,dico_bond_junct



#################################
def CreateClusterGlobal(dico_neighbour_ring,rings):
    """
    Creates a dictionnary of temporary clusters, e.g one cluster for one ring before fusion.
    """
    dico_cluster_global = {}
    for i in range(0,len(rings)): 
        dico_temp = {i:i} 
        if dico_neighbour_ring.has_key(i)!=0: 
            for elem in dico_neighbour_ring[i]: 
                dico_temp[elem] = elem   
            dico_cluster_global[i] = dico_temp  

        else:
            dico_temp[i] = i  
            dico_cluster_global[i] = dico_temp
    return dico_cluster_global 




################################
#################################        
def Fusion(dico1, dico2):
    """
    Clusters fusion.
    """


    dico = {}
    for elem1 in dico1:
        for elem2 in dico2:
            if not dico.has_key(elem2):
                dico[elem2] = dico2[elem2]
            if not dico.has_key(elem1):
                dico[elem1] = dico1[elem1]
    return dico


################################
def Aggregates(dico_cluster_global):
  
    signet = True
    dico_temp = dico_cluster_global
    if signet:
        for globali in range(0, len(dico_cluster_global)): 
            cluster =  dico_cluster_global[globali]
            dico_result = {}
            for ki in cluster: 
                for i in range(0,len(dico_cluster_global)): 
                    if i != ki: 
                        clusteri = dico_cluster_global[i]  
                        if clusteri.has_key(ki):
                            if cluster != clusteri:
                                dico_result[ki] =  Fusion(cluster, clusteri) 
            for k in range(0, len(dico_cluster_global)):
                if not dico_result.has_key(k):
                    dico_result[k] =  dico_cluster_global[k]
            dico_cluster_global = dico_result

        if dico_cluster_global != dico_temp:
            dico_cluster_global = Aggregates(dico_cluster_global)
        else:
            signet == False
    return dico_cluster_global


################################
def GetItRight(dico_cluster_global):
    """
    Get the number of systems rings.
    """

    
    length = len(dico_cluster_global)
    liste = []
    for dur in dico_cluster_global:
        liste.append(dico_cluster_global[dur].values())
    liste.sort()
    cluster   = liste[0]
    r = 0
    ll = 1
    while r < length:
        p = ll
        while p < length:
            try:
                cluster_p = liste[p]
            except:
                break
            if cluster_p == cluster:
                liste.remove(cluster_p)
            else:
                p = p + 1
        r = r + 1
        ll = ll + 1
        try:
            cluster = liste[r]
        except:
            break

    return liste, len(liste)



###################################
def CountNeighborBondsInCluster(dico_bond_junct, SystemRings):
    """
    Get the number of bonds involved in a cluster.
    """

    counter_list = {} 

    for i in range(0, len(SystemRings)):
        counter = 0
        for j in SystemRings[i]:
            for k in SystemRings[i]:
                if k > j:
                    list_temp = []
                    list_temp.append(j)
                    list_temp.append(k)
                    list_temp.sort()
                    for r in dico_bond_junct:
                        pair = dico_bond_junct[r]
                        pair.sort()
 
                        if list_temp == pair:
                            counter = counter + 1
                            break
        counter_list[i] = counter
    return counter_list


###################################
def CalculateNbAtomsSystemRings(SystemRings, dico_cluster_length, rings):
    """
    Get the number of atoms involved in a system ring.
    """
    
    MAX = 0
    for i in range(0, len(SystemRings)):
        Nb_in_clustI = 0
        liste = SystemRings[i]
        for elem in liste:
            Nb_in_clustI = Nb_in_clustI + rings[elem].Size()
        tot_non_redodnt_atoms = Nb_in_clustI -dico_cluster_length[i] -len(liste) + 1
        if tot_non_redodnt_atoms > MAX:
            MAX = tot_non_redodnt_atoms
            MAX_elem = i
    return MAX, i
