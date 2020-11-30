import os, sys
import multiprocessing
from datetime import datetime

os.chdir('../Data')
os.chdir('./Annotation')

R_ls = os.listdir('../Dic_Lib_Output_PDB/')
for R in R_ls:
    os.system('cp -r ../Dic_Lib_Output_PDB/'+R+'/SDF .')
    os.system('mv SDF/* .')
    os.system('rm -r SDF')
