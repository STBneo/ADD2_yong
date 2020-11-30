import os,sys

merge_sdf_path = '../Data/Imaged_SDF/'
sdf_path = '../Data/Imaged_SDF_Split/'
os.system('rm -r '+sdf_path)
os.system('mkdir '+sdf_path)

merge_sdf_ls = os.listdir(merge_sdf_path)
zid_set = set()
for merge_sdf in merge_sdf_ls:
    fr = open(merge_sdf_path+merge_sdf, 'r')
    while True:
        line = fr.readline()
        if 'ZINC' in line:
            zid = line.rstrip()
            
            if zid not in zid_set:
                zid_set.add(zid)
                fw = open(sdf_path+zid+'.sdf', 'w')
                fw.write(line)

                while True:
                    line = fr.readline()
                    fw.write(line)

                    if '$$$$' in line: break

                    if not line: break
            else: 
                #print(zid)
                pass

        if not line: break
