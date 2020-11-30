import os, sys

print('Copy')
kinase = sys.argv[1]
os.system('rm -r ../Data/PASS_ML')
os.mkdir('../Data/PASS_ML')
fr = open('../Data/Output_ML/kinase_'+kinase+'_ML.csv', 'r')
while True:
    line = fr.readline()
    if not line: break

    line_sp = line.split('\t')
    zid = line_sp[0]
    score = line_sp[-1].rstrip()

    if float(score) == 1:
        sdf = zid+'.sdf'
        #print(sdf)

        os.system('cp ../Data/PASS/'+sdf+' ../Data/PASS_ML')
        #sys.exit(1)

print('Merge')
os.system('rm ../Data/kinase_'+kinase+'.sdf')
path = '../Data/PASS_ML/'
for i in range(0,10):
    for j in range(0,10):
        i = str(i)
        j = str(j)
        print(i+j)
        fname = 'ZINC00'+i+j+'*.sdf'
        #print(fname)
        os.system('cat '+path+fname+' >> ../Data/kinase_'+kinase+'.sdf')
