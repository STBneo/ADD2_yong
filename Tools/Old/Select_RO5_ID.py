import os,sys
import multiprocessing

###########################################################################
# python Select_RO5_ID.py {RO5_Y/N} {MW_max} {LogP_max} {HBD_mas} {HBA_max}
# python Select_RO5_ID.py Y
# python Select_RO5_ID.py N 500 5 10 5
###########################################################################

RO5_para = sys.argv[1]

os.system('rm -r ../Data/PASS')
os.system('mkdir ../Data/PASS')
'''
R_ls = os.listdir('../Data/Dic_Lib_Output_PDB')
for R in R_ls:
    os.system('cp -r ../Data/Dic_Lib_Output_PDB/'+R+'/SDF ../Data/Annotation')
    os.system('mv ../Data/Annotation/SDF/* ../Data/Annotation')
    os.system('rm -r ../Data/Annotation/SDF')
'''

fr = open('../Data/Annotation/results.table.id', 'r')
fw = open('../Data/Annotation/RO5_pass_ID.txt', 'w')
zid_ls = []
while True:
    line = fr.readline()
    if not line: break
    
    while True:
        line = fr.readline()
        #print(line.split('\t'))
        #sys.exit(1)

        if line != '':
            line = line.split('\t')
            zid = line[0]
            MW = float(line[1])
            LogP = float(line[2])
            HBD = float(line[6])
            HBA = float(line[7])
            RO5 = line[-4]
            #print(zid)
            #print(mw)
            #print(RO5)
            #sys.exit(1)

            if RO5_para=='Y' or RO5_para=='y':
                if RO5=='False':
                    fw.write(zid)
                    zid_ls.append(zid)

            elif RO5_para=='N' or RO5_para=='n':  
                if RO5=='False' or RO5=='True':
                    MW_max = float(sys.argv[2])
                    LogP_max = float(sys.argv[3])
                    HBD_max = float(sys.argv[4])
                    HBA_max = float(sys.argv[5])
                    if MW<=MW_max and LogP<=LogP_max and HBD<=HBD_max and HBA<=HBA_max:
                        fw.write(zid)
                        zid_ls.append(zid)

        if not line or line=='': break
fr.close()

def copy(zid):
    os.system('cp ../Data/Annotation/'+zid+'.sdf ../Data/PASS')

n_cpu = multiprocessing.cpu_count()-1
pool = multiprocessing.Pool(processes=n_cpu)
pool.map(copy, zid_ls)
pool.close()
pool.join()
