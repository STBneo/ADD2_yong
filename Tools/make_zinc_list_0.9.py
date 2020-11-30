import sys

R = sys.argv[1]
fr = open('../../Dic_Lib_Input/All.f.final_re.'+R+'.csv', 'r')
fw = open('zid_list_'+R+'.txt', 'w')
cnt = 0

lines = fr.readlines()
#print(lines)
for line in lines:
    zid = line.split(',')[0]
    zid = 'ZINC00'+zid
    fw.write(zid+'\n')
    
fr.close()
fw.close()
