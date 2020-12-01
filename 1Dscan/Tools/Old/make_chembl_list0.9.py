import sys

R = sys.argv[1]
fr = open('../../../Data/Dic_Lib_Input/All.f.final_re.'+R+'.csv', 'r')
fw = open('chembl_list.'+R+'.txt', 'w')
cid_ls = set()
cnt = 0

lines = fr.readlines()
#print(lines)
for line in lines:
    line = line.strip()
    if "Chembl_ID" not in line:
        cid = line.split(',')[0]
        if cid not in cid_ls:
            cnt += 1
            cid_ls.add(cid)
            fw.write(cid+'\n')
            #if cnt == 1100: break
        else: pass
    
fr.close()
fw.close()
