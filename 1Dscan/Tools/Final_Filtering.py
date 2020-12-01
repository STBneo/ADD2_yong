import os,sys
import multiprocessing

###########################################################################
# python Select_RO5_ID.v2.py {RO5_y/n} {MW_min} {MW_max} {LogP_max} {HBD_mas} {HBA_max} {RO5_max} {FDA_min}
# python Select_RO5_ID.v2.py n
# python Select_RO5_ID.v2.py y 0 500 5 10 5 0 0.5 
###########################################################################

def copy(zid):
    os.system('cp ../Data/Dic_Lib_Output_SDF/All/'+zid+'.sdf ../Data/PASS')

def RO5(MW_min=0,MW_max=500,LogP_max=5,HBD_max=5,HBA_max=10,RO5_max=0,FDA_min=0.5):
    fr = open('../Data/Annotation/results.table.id', 'r')
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
                RO5 = int(line[-6])
                FDA = float(line[-1])
                #print(zid)
                #print(mw)
                #print(RO5)
                #sys.exit(1)

                if MW_min<=MW<=MW_max and LogP<=LogP_max and HBD<=HBD_max and HBA<=HBA_max and RO5<=RO5_max and FDA>=FDA_min:
                    #print(zid)
                    zid_ls.append(zid)

            if not line or line=='': break
    fr.close()

    n_cpu = multiprocessing.cpu_count()-1
    pool = multiprocessing.Pool(processes=n_cpu)
    pool.map(copy, zid_ls)
    pool.close()
    pool.join()

def main():
    os.system('rm -r ../Data/PASS')
    os.system('mkdir ../Data/PASS')

    RO5_para = sys.argv[1]

    if RO5_para == 'n' or RO5_para == 'N':
        RO5()

    elif RO5_para == 'y' or RO5_para == 'Y':
        MW_min = float(sys.argv[2])
        MW_max = float(sys.argv[3])
        LogP_max = float(sys.argv[4])
        HBD_max = float(sys.argv[5])
        HBA_max = float(sys.argv[6])
        RO5_max = int(sys.argv[7])
        FDA_min = float(sys.argv[8])
        RO5(MW_min,MW_max,LogP_max,HBD_max,HBA_max,RO5_max,FDA_min)

if __name__ == '__main__':
    main()
