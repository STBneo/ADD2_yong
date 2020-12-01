import os, sys

path = '../Data/'
fnames = os.listdir(path)
R_ls = []

for fname in fnames:
    #print(fname)
    if(fname.endswith('R') and fname.startswith('1D_Out_')):
        R = fname.split('_')[-1]
        R_ls.append(R)

R_ls = sorted(R_ls)
#print(R_ls)
for R in R_ls:
    os.system('bash PHscan_1D.step3.sh '+R)
    os.system('bash PHscan_1D.step4.sh '+R)
