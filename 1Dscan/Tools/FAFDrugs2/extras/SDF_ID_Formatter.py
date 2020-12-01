#! /usr/bin/env python

import sys
import cPickle
import os



def get_pos_sdf(file,tag):

    """
    Creating the index of starting and ending positions of each ligand in
    a (.sdf) file. The index contains {ID_Number:(start,stop)}.

    """
    fh=open(file)
    pos = fh.tell()
    line = fh.readline()
    flag = 0
    dic_pos = {}
    while line != '':

        line = line[:-1]
        
        if flag == 0:
            
            start = pos
            pos = fh.tell()
            line = fh.readline()
            flag = 1
            

        else:
            
            if line[:(len(tag))] == tag:
                ID = fh.readline()[:-1]
                pos = fh.tell()                

            if line == '$$$$':
                stop = pos
                
                flag = 0
                dic_pos[ID]=(start,stop)
                pos = fh.tell()

            else:
                pos = fh.tell()
        line = fh.readline()

    fh.close()
    return dic_pos


def get_listID(file,tag):
    
    """
    Reading the input (.sdf) file, get the ID_numbers and keep them in a list

    """
    fh = open(file,'r')
    listID = []
    line = fh.readline()    
    while line != '':
        
        line = line[:-1]
        if line[:(len(tag))] == tag:
            ID = fh.readline()[:-1]
            listID.append(ID)
            print ID
        line = fh.readline()

    fh.close()
    return listID


if __name__ == '__main__':
    
    tag_id = sys.argv[1]
    file = sys.argv[2]

    list_ID = get_listID(file,tag_id)
        
    file_out = file[:-4] + '_formatted' + '.sdf'
    fho = open(file_out,'w')
    
    dict = get_pos_sdf(file,tag_id)
    file_dict_dump = file[:-4] + '.dump'
    dict_dump = open(file_dict_dump,'w')
    cPickle.dump(dict,dict_dump)
    dict_dump.close()
    fh_dump = open(file_dict_dump,'r')
    dump = cPickle.load(fh_dump)
    
    fhi = open(file)
    for ID in list_ID:                    
        fho.write(ID)
        fho.write('\n')
        start,stop = dump[ID]      
        fhi.seek(start)            
        pos = fhi.tell()                    
        line = fhi.readline()
        while pos != stop:
            
            line = fhi.readline()
            fho.write(line) 
            pos = fhi.tell()
        fho.write('\n')
        fho.write('$$$$')
        fho.write('\n')
            
    fh_dump.close()
    fho.close()
    fhi.close()
    os.system("rm "+ file_dict_dump)
