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
    fw = open('../Data/Annotation/results.table.id.pass', 'w')
    zid_ls = []
    
    cnt = 0
    while True:
        line = fr.readline()
        if not line: break
        cnt += 1

        if cnt == 1:
            fw.write(line)

        else:
            line_sp = line.split('\t')
            zid = line_sp[0]
            MW = line_sp[1]
            LogP = line_sp[2]
            HBD = line_sp[6]
            HBA = line_sp[7]
            RO5 = line_sp[-6]
            FDA = line_sp[-1]
            #print(zid)
            #print(mw)
            #print(RO5)
            #sys.exit(1)

            if LogP == 'None':
                if MW_min<=float(MW)<=MW_max and float(HBD)<=HBD_max and float(HBA)<=HBA_max and int(RO5)<=RO5_max and float(FDA)>=FDA_min:
                    zid_ls.append(zid)
                    fw.write(line)
            else:
                if MW_min<=float(MW)<=MW_max and float(LogP)<=LogP_max and float(HBD)<=HBD_max and float(HBA)<=HBA_max and int(RO5)<=RO5_max and float(FDA)>=FDA_min:
                    zid_ls.append(zid)
                    fw.write(line)
    fw.close()
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
