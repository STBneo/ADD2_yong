import sys, os
def make_clustered_sdf_list():
    with open('ligand.0.7.chembl.clustered.out.txt', 'r') as f:
        lines = f.readlines()

    fw = open('clustered_sdf.txt', 'w')
    for line in lines:
        if '#' in line:
            pass
    
        else:
            line = line.strip().split('\t')
            #print(line)
            nmem = line[1]
            mems = line[2:]
            #print(mems)
            
            if int(nmem) != 1:
                for mem in mems:
                    mem = mem.replace("'",'')
                    fw.write(mem+'.sdf\n')
                fw.write('$$$\n')
    fw.close()

def select_not_clustered_sdf():
    with open('ligand.0.7.chembl.clustered.out.txt', 'r') as f:
        lines = f.readlines()
    os.system('mkdir not_clustered_sdf')
    #fw = open('not_clustered.txt', 'w')
    #mem_ls = []
    for line in lines:
        if 'Total' in line: pass
        else:
            line = line.split('\t')
            #print(line)
            nmem = line[1]
            mem = line[2]
            #print(nmem)
            #print(mem)

            if int(nmem) == 1:
                #mem = mem.replace("'",'').strip()
                mem = mem.replace("'",'').strip().split('.')[0]
                for memm in mem.split(','):
                    memm = memm.strip()
                    #print(memm)
                    #mem_ls.append(memm)
                    #fw.write(memm+'.sdf\n')
                    print('cp ./sdf/'+memm+'.sdf not_clustered_sdf/'+memm+'.sdf')
                    os.system('cp ./sdf/'+memm+'.sdf not_clustered_sdf/'+memm+'.sdf')
    #fw.close()

    #print(mem_ls)
    #print(len(mem_ls))
    #return(mem_ls)

def main():
   make_clustered_sdf_list()
   select_not_clustered_sdf()

if __name__ == "__main__":
    main()
