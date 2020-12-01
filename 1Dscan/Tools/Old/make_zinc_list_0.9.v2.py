import sys,os

sdf_ls = os.listdir('../../PASS')
fw = open('zid_list.txt', 'w')
for sdf in sdf_ls:
    zid = sdf[:-4]
    fw.write(zid+'\n')
fw.close()
