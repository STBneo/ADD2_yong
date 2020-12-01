import sys,os

pdb_path = '../Data/Dic_Lib_Output_PDB/'
pdb_ls = os.listdir(pdb_path)
pid_set = set()

for pdb in pdb_ls:
    pid = pdb[:-4]
    pid_set.add(pid)

table_path = '../Data/Annotation/'
fr = open(table_path+'results.table.id', 'r')
fw = open(table_path+'results.table.id.flt', 'w')
cnt = 0
while True:
    cnt += 1
    line = fr.readline()
    if not line: break
    
    if cnt == 1:
        pass
    else:
        zid = line.split('\t')[0]
        if zid in pid_set:
            fw.write(line)
fr.close()
fw.close()
