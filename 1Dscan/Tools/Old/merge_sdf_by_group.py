import sys,os

os.system('rm ../Data/kinase.sdf')
path = '../Data/PASS/'
for i in range(0,10):
    for j in range(0,10):
        i = str(i)
        j = str(j)
        print(i+j)
        fname = 'ZINC00'+i+j+'*.sdf'
        #print(fname)
        os.system('cat '+path+fname+' >> ../Data/kinase.sdf')
