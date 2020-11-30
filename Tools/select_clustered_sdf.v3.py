import sys,os

fr = open('../Data/Table/l_cluster_DBSCAN1.txt', 'r')
al_sdf = fr.read()
fr.close()
al_sdf_ls = al_sdf.split('$$$\n')
#print(al_sdf_ls)
one_sdf_ls = []
fw = open('../Data/Table/l_cluster_DBSCAN1.txt', 'w')
for sdf_ls in al_sdf_ls:
    #print(sdf_ls)
    #print(sdf_ls.count('.sdf'))
    if sdf_ls.count('.sdf') == 1:
        sdf = sdf_ls.split('\n')[0]
        #print(sdf)
        one_sdf_ls.append(sdf)
    elif sdf_ls.count('.sdf') >= 2:
        fw.write(sdf_ls)
        fw.write('$$$\n')
#print(one_sdf_ls)
fw.close()

path = '../Data/DBSCAN/'
os.system('rm -r '+path)
os.system('mkdir '+path)
for one_sdf in one_sdf_ls:
    os.system('cp ../Data/Input/'+one_sdf+' '+path)
