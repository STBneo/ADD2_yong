import os,sys,glob,subprocess,apsw,itertools,argparse
import multiprocessing
from multiprocessing import Manager,Process
from functools import partial
import pandas as pd
from sqlite3 import Error
import sqlite3
import time
from datetime import datetime

def pos_dic():
    temp_dic = {'CDK7': ['ZINC000000101319', 'ZINC000077485665', 'ZINC000004192450', 'ZINC000033278339', 'ZINC000467398634','ZINC000095526640'], \
    'FLT3':['ZINC000000008662', 'ZINC000058014319', 'ZINC000005814210', 'ZINC000006448596','ZINC000012322830', 'ZINC000096221013', \
    'ZINC000100498577', 'ZINC000013126934', 'ZINC000000575002', 'ZINC000009245306','ZINC000013148149', 'ZINC000217901089', \
    'ZINC000000057655', 'ZINC000000210268', 'ZINC000023334750', 'ZINC000000248216','ZINC000001001156', 'ZINC000000435149', \
    'ZINC000006508912', 'ZINC000015843244', 'ZINC000021114661', 'ZINC000057964036','ZINC000004137279', 'ZINC000019702144', \
    'ZINC000079020838', 'ZINC000000111962', 'ZINC000078733090', 'ZINC000075144163','ZINC000097201518', 'ZINC000065272148', \
    'ZINC000072404457', 'ZINC000085391937', 'ZINC000001075920', 'ZINC000000060207','ZINC000075544404'], \
    'EGFR':['ZINC000001076595', 'ZINC000217912735', 'ZINC000085877625', 'ZINC000020827506', 'ZINC000217901089','ZINC000001068379', \
    'ZINC000009281884', 'ZINC000249700260', 'ZINC000009059860'], \
    'ERBB4':['ZINC000096396694', 'ZINC000032751234', 'ZINC000101747211', 'ZINC000089977150', 'ZINC000033260731','ZINC000072333497']}
    return temp_dic

def load_FG():  # checkmol output code - R Group Name
    tmp_dic = {'000000T2': 'cation', '000000T1': 'anion', 'C2O10000': 'carbonyl_compound', 'C2O1H000': 'aldehyde','C2O1C000': 'ketone', \
               'C2S10000': 'thiocarbonyl_compound', 'C2S1H000': 'thioaldehyde', 'C2S1C000': 'thioketone','C2N10000': 'imine', 'C2N1N000': 'hydrazone', \
               'C2NNC4ON': 'semicarbazone', 'C2NNC4SN': 'thiosemicarbazone', 'C2N1OH00': 'oxime','C2N1OC00': 'oxime_ether', 'C3OC0000': 'ketene', \
               'C3OCC000': 'ketene_acetal_derivative', 'C2O2H200': 'carbonyl_hydrate', 'C2O2HC00': 'hemiacetal','C2O2CC00': 'acetal', 'C2NOHC10': 'hemiaminal', \
               'C2N2CC10': 'aminal', 'C2NSHC10': 'thiohemiaminal', 'C2S2CC00': 'thioacetal', 'C2CNH000': 'enamine','C2COH000': 'enol', 'C2COC000': 'enolether', \
               'O1H00000': 'hydroxy_compound', 'O1H0C000': 'alcohol', 'O1H1C000': 'prim_alcohol','O1H2C000': 'sec_alcohol', 'O1H3C000': 'tert_alcohol', \
               'O1H0CO1H': '1_2-diol', 'O1H0CN1C': '1_2-aminoalcohol', 'O1H1A000': 'phenol', 'O1H2A000': '1_2-diphenol','C2COH200': 'enediol', 'O1C00000': 'ether', \
               'O1C0CC00': 'dialkylether', 'O1C0CA00': 'alkylarylether', 'O1C0AA00': 'diarylether','S1C00000': 'thioether', 'S1S1C000': 'disulfide', \
               'O1O1C000': 'peroxide', 'O1O1H000': 'hydroperoxide', 'N1N10000': 'hydrazine_derivative','N1O1H000': 'hydroxylamine', 'N1C00000': 'amine', \
               'N1C10000': 'prim_amine', 'N1C1C000': 'prim_aliphat_amine', 'N1C1A000': 'prim_aromat_amine','N1C20000': 'sec_amine', 'N1C2CC00': 'sec_aliphat_amine', \
               'N1C2AC00': 'sec_mixed_amine_aryl_alkyl', 'N1C2AA00': 'sec_aromat_amine', 'N1C30000': 'tert_amine','N1C3CC00': 'tert_aliphat_amine', \
               'N1C3AC00': 'tert_mixed_amine', 'N1C3AA00': 'tert_arom_amine', 'N1C400T2': 'quaternary_ammonium_salt','N0O10000': 'N-oxide', \
               'XX000000': 'halogen_deriv', 'XX00C000': 'alkyl_halide', 'XF00C000': 'alkyl_fluoride','XC00C000': 'alkyl_chloride', 'XB00C000': 'alkyl_bromide', \
               'XI00C000': 'alkyl_iodide', 'XX00A000': 'aryl_halide', 'XF00A000': 'aryl_fluoride','XC00A000': 'aryl_chloride', 'XB00A000': 'aryl_bromide', \
               'XI00A000': 'aryl_iodide', '000000MX': 'organometallic_compound', '000000ML': 'organolithium_compound','000000MM': 'organomagnesium_compound', \
               'C3O20000': 'carboxylic_acid_deriv', 'C3O2H000': 'carboxylic_acid', 'C3O200T1': 'carboxylic_acid_salt','C3O2C000': 'carboxylic_acid_ester', \
               'C3O2CZ00': 'lactone', 'C3ONC000': 'carboxylic_acid_imide', 'C3ONC100': 'carboxylic_acid_prim_amide','C3ONC200': 'carboxylic_acid_sec_amide', \
               'C3ONC300': 'carboxylic_acid_tert_amide', 'C3ONCZ00': 'lactam', 'C3ONN100': 'carboxylic_acid_hydrazide','C3ONN200': 'carboxylic_acid_azide', \
               'C3ONOH00': 'hydroxamic_acid', 'C3N2H000': 'carboxylic_acid_amidine','C3NNN100': 'carboxylic_acid_amidrazone', 'C3N00000': 'nitrile', \
               'C3OXX000': 'acyl_halide', 'C3OXF000': 'acyl_fluoride', 'C3OXC000': 'acyl_chloride','C3OXB000': 'acyl_bromide', 'C3OXI000': 'acyl_iodide', \
               'C2OC3N00': 'acyl_cyanide', 'C3NOC000': 'imido_ester', 'C3NXX000': 'imidoyl_halide','C3SO0000': 'thiocarboxylic_acid_deriv', \
               'C3SOH000': 'thiocarboxylic_acid', 'C3SOC000': 'thiocarboxylic_acid_ester', 'C3SOCZ00': 'thiolactone','C3SNH000': 'thiocarboxylic_acid_amide', \
               'C3SNCZ00': 'thiolactam', 'C3NSC000': 'imidothioester', 'C3ONAZ00': 'oxohetarene','C3SNAZ00': 'thioxohetarene', 'C3NNAZ00': 'iminohetarene', \
               'C3O30000': 'orthocarboxylic_acid_deriv', 'C3O3C000': 'carboxylic_acid_orthoester','C3O3NC00': 'carboxylic_acid_amide_acetal', \
               'C3O2C3O2': 'carboxylic_acid_anhydride', 'C3ONCH10': 'carboxylic_acid_unsubst_imide','C3ONCC10': 'carboxylic_acid_subst_imide', \
               'C4000000': 'CO2_deriv_(general)', 'C4O30000': 'carbonic_acid_deriv','C4O3C100': 'carbonic_acid_monoester', 'C4O3C200': 'carbonic_acid_diester', \
               'C4O3CX00': 'carbonic_acid_ester_halide', 'C4SO0000': 'thiocarbonic_acid_deriv','C4SOC100': 'thiocarbonic_acid_monoester', \
               'C4SOC200': 'thiocarbonic_acid_diester', 'C4SOX_00': 'thiocarbonic_acid_ester_halide','C4O2N000': 'carbamic_acid_deriv', \
               'C4O2NH00': 'carbamic_acid', 'C4O2NC00': 'carbamic_acid_ester_urethane','C4O2NX00': 'carbamic_acid_halide', \
               'C4SN0000': 'thiocarbamic_acid_deriv', 'C4SNOH00': 'thiocarbamic_acid','C4SNOC00': 'thiocarbamic_acid_ester', \
               'C4SNXX00': 'thiocarbamic_acid_halide', 'C4O1N200': 'urea', 'C4N2O100': 'isourea','C4S1N200': 'thiourea', 'C4N2S100': 'isothiourea', \
               'C4N30000': 'guanidine', 'C4ON2N00': 'semicarbazide', 'C4SN2N00': 'thiosemicarbazide','N4N20000': 'azide', 'N2N10000': 'azo_compound', \
               'N3N100T2': 'diazonium_salt', 'N3C10000': 'isonitrile', 'C4NO1000': 'cyanate', 'C4NO2000': 'isocyanate','C4NS1000': 'thiocyanate', \
               'C4NS2000': 'isothiocyanate', 'C4N20000': 'carbodiimide', 'N2O10000': 'nitroso_compound','N4O20000': 'nitro_compound', 'N3O20000': 'nitrite', \
               'N4O30000': 'nitrate', 'S6O00000': 'sulfuric_acid_deriv', 'S6O4H000': 'sulfuric_acid','S6O4HC00': 'sulfuric_acid_monoester', \
               'S6O4CC00': 'sulfuric_acid_diester', 'S6O3NC00': 'sulfuric_acid_amide_ester','S6O3N100': 'sulfuric_acid_amide', 'S6O2N200': 'sulfuric_acid_diamide', \
               'S6O3XX00': 'sulfuryl_halide', 'S5O00000': 'sulfonic_acid_deriv', 'S5O3H000': 'sulfonic_acid','S5O3C000': 'sulfonic_acid_ester', \
               'S5O2N000': 'sulfonamide', 'S5O2XX00': 'sulfonyl_halide', 'S4O20000': 'sulfone', 'S2O10000': 'sulfoxide','S3O00000': 'sulfinic_acid_deriv', \
               'S3O2H000': 'sulfinic_acid', 'S3O2C000': 'sulfinic_acid_ester', 'S3O1XX00': 'sulfinic_acid_halide','S3O1N000': 'sulfinic_acid_amide', \
               'S1O00000': 'sulfenic_acid_deriv', 'S1O1H000': 'sulfenic_acid', 'S1O1C000': 'sulfenic_acid_ester','S1O0XX00': 'sulfenic_acid_halide', \
               'S1O0N100': 'sulfenic_acid_amide', 'S1H10000': 'thiol', 'S1H1C000': 'alkylthiol','S1H1A000': 'arylthiol', 'P5O0H000': 'phosphoric_acid_deriv', \
               'P5O4H200': 'phosphoric_acid', 'P5O4HC00': 'phosphoric_acid_ester', 'P5O3HX00': 'phosphoric_acid_halide','P5O3HN00': 'phosphoric_acid_amide', \
               'P5O0S000': 'thiophosphoric_acid_deriv', 'P5O3SH00': 'thiophosphoric_acid','P5O3SC00': 'thiophosphoric_acid_ester', 'P5O2SX00': 'thiophosphoric_acid_halide', \
               'P5O2SN00': 'thiophosphoric_acid_amide', 'P4O30000': 'phosphonic_acid_deriv','P4O3H000': 'phosphonic_acid', 'P4O3C000': 'phosphonic_acid_ester', \
               'P3000000': 'phosphine', 'P2O00000': 'phosphinoxide', 'B2O20000': 'boronic_acid_deriv','B2O2H000': 'boronic_acid', 'B2O2C000': 'boronic_acid_ester', \
               '000C2C00': 'alkene', '000C3C00': 'alkyne', '0000A000': 'aromatic_compound','0000CZ00': 'heterocyclic_compound', 'C3O2HN1C': 'alpha-aminoacid', \
               'C3O2HO1H': 'alpha-hydroxyacid'}
    return tmp_dic

def load_FG2():
    with open('FG_combination.code.yklee.marshal','rb') as F:
        didi = marshal.load(F)
    return didi
def sql_connection_IDR():
    try :
        con = apsw.Connection('./Data/DB_Table/ZINC_IDR.db')
        return con
    except Error:
        print(Error)
        sys.exit(1)
        return

def sql_connection():
    try :
        con = apsw.Connection(':memory:')
        return con
    except Error:
        print(Error)
        sys.exit(1)
        return
def sql_create_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE R2_Table(R2group txt PRIMARY KEY, ZID text)")
    return
def sql_insert(con,entities):
    cursorObj = con.cursor()
    try:
        query = 'INSERT INTO R2_Table(R2group,zid) VALUES(?,?)'
        cursorObj.execute(query,entities)
        # cursorObj.execute("INSERT INTO R_Table(Rgroup,zid) VALUES(?,?)",entities)
        return 1
    except:
        print(rid)
        return 0


def sql_update(con, entities):
    cursorObj = con.cursor()
    try:
        cursorObj.execute('UPDATE R2_Table SET zid=? WHERE R2group=?', entities)
    except:
        except_update(entities)
        pass
        #sys.exit()
def sql_connection_R2():
    try :
        con = apsw.Connection('/ssd/yklee/1D_Scan.v2/Data/DB_Table/ZINC_R2.db')
        return con
    except Error:
        print(Error)
        sys.exit(1)
        return

def Key_dic_load():
    didi = {}
    with open('/ssd/yklee/1D_Scan.v2/Result_CDK7_input.dat','r') as F:
        for i in marshal.load(F):
            didi[i[0]]= i[1]
    print("Key Load OK")
    return didi

def SCF_result_load():
    lili = []
    with open('/devc24/swshin/1D_Scan.v2/Data/1D_Out_SCF/SCF_Out.list.Per.SMILES.txt','r') as F:
        for line in F.readlines():
            lili.append(line.strip())

    print("SCF results Load OK")
    return lili
def KR_result_analysis(k_set,mlist):
    Ncpu = multiprocessing.cpu_count()

    with open('../Data/FLT3_input_Temp_SCF/SCF_Out.list.Per.SMILES.txt','r') as F:
        a = 0
        b = 0
        #print(F.readlines()[:10])
        flines = F.readlines()
        lend = len(flines)//100
        print(lend)
        lili = list(divide_list(flines,lend))
        for li in lili:
            for line in li:#F.readlines():

                tline = line.strip().split(',')
                zid = tline[2]
                p_set = find_zid_IDR(zid)
                Key_dics[zid] = [p_set,tline]
            b +=1
            pool = multiprocessing.Pool(Ncpu-2)
            func = partial(SCF_result_analysis_core,k_set=k_set,mlist=mlist,Key_dics=Key_dics)
            pool.map(func,Key_dics.keys())
            pool.close()
            pool.join()
            with open('result_%s.txt'%str(b),'w') as W:
                for line2 in mlist:
                    W.write(line2 + '\n')
            mlist[:] = Manager().list()

def divide_list(ls,n):
    #n = 25
    for i in range(0,len(ls),n):
        yield l[i:i+n]

def find_zid(alp):
    query = 'SELECT * FROM R2_Table WHERE R2group=\'%s\''%(alp)
    conR2cursor.execute(query)
    rows = conR2cursor.fetchall()
    if not rows:
        pass
    else:
        ppp = unicode.encode(rows[0][1],'utf-8')
        p_set = set(ppp.split(','))
        print("Find R2 %s ID set OK"%alp)
        return p_set

def find_zid_IDR(alp):
    cursorObj = con.cursor()
    query = "SELECT * FROM IDR_Table WHERE Zid=\'%s\'"%(alp)
    cursorObj.execute(query)
    rows = cursorObj.fetchall()
    cursorObj.close()
    if not rows:
        pass
    else:
        ppp = unicode.encode(rows[0][1],'utf-8')
        p_set = set(ppp.split(','))
        return p_set

def SCF_to_Key(zid,mlist,id_sets,plist,pos_list):
    zzid = zid.split(',')[2]
    for id_set in id_sets:
        if zzid in id_set:
            mlist.append(zid)
            if zzid in pos_list:
                plist.append(zid)
            else:
                pass
        else:
            pass

def memoryDB2diskDB(con, DB_name):  # memory DB to Disk DB
    dest = apsw.Connection(DB_name)
    with dest.backup('main', con, 'main') as backup:
        backup.step()
    dest.close()

def checkmol_activation(afile, tmp_dic, con, zid_list, dup_zid_list):
    with open(afile, 'r') as F:
        zinc_id = F.readlines()[0].strip()
    try:
        # re_checkmol = subprocess.check_output('/lwork01/yklee_temp/zinc_work/zinc_split/checkmol -cs %s'%afile,stderr=subprocess.STDOUT,shell=True)
        re_checkmol = subprocess.check_output('/lwork01/swshin/1D_Scan*/Tools/checkmol -cs %s'%afile,stderr=subprocess.STDOUT,shell=True)
        #re_checkmol = subprocess.check_output('/lwork02/yklee/temp_dir/yklee_work/checkmol -cs %s' % afile,stderr=subprocess.STDOUT, shell=True)
    except:
        print 'Some Error in tmp.sdf'
        return

    re_checkmol = re_checkmol.strip()
    re_checkmol = re_checkmol.decode('ascii')
    token = re_checkmol.split(';')[:-1]
    a = 0
    if len(token) == 0 or len(token) == 1:
        dup_zid_list[zinc_id] = 0
        pass
    else:
        strtokens = []
        for i in token:
            strtokens.append(tmp_dic[i])

        try:
            if zid_list[zinc_id] == 1:
                pass
        except:
            for rgroup in itertools.combinations(strtokens,2):
                zid_list[zinc_id] = 1
                cursorObj = con.cursor()
                rgroup = '^^'.join(sorted(list(rgroup)))
                if not rgroup in set(plist.keys()):
                    t = 1
                else:
                    t = plist[rgroup]
                    t += 1
                plist[rgroup] = t

                query = "SELECT * FROM R2_Table WHERE R2group LIKE \'%s\'" % rgroup

                cursorObj.execute(query)
                rows = cursorObj.fetchall()
                cursorObj.close()
                if not rows:
                    entities = (rgroup, zinc_id)
                    sql_insert(con, entities)

                else:
                    ppp = unicode.encode(rows[0][1], 'utf-8') + ',' + zinc_id
                    entities = (ppp, rows[0][0])
                    sql_update(con, entities)

def input_Temp_R2(input_dir,FG_dic,FG_dic2):
    con = sql_connection()
    sql_create_table(con)
    os.chdir(input_dir)
    input_sdfs = sorted(glob.glob('*.sdf'))
    zid_list = {}
    dup_zid_list = {}
    for i in input_sdfs:
        checkmol_activation(i,FG_dic,con,zid_list,dup_zid_list,FG_dic2)
    cursorObj = con.cursor()
    query = cursorObj.execute('SELECT * FROM R2_Table')
    cols = [column[0] for column in query.description]
    df = pd.DataFrame.from_records(data=query.fetchall(),columns=cols)
    os.chdir('../../')
    return df

def searching_part1(zid,mlist):
    zzid = zid.split(',')[2]
    if zzid in tset:
        mlist[zid] = 1
    else:
        pass
def dropop(i):
    df1 = tdf[tdf[0] == i]
    df2 = df1.drop_duplicates()
    return df2

def input_analysis():
    ppp = sorted(list(set(plist.values())),reverse=True)
    ttt = {}
    lll = []
    for i,j in zip(range(0,len(ppp)),ppp):
        ttt[j] = i
    pdf = pd.DataFrame.from_dict(plist,orient='index').reset_index().rename(columns={'index':'Rgroup',0:'Freq'}).sort_values(by='Freq',ascending=False).reset_index(drop=True)
    cdf = pd.DataFrame.from_dict(clist,orient='index').reset_index().rename(columns={'index':'Rgroup',0:'Freq'}).sort_values(by='Freq',ascending=False).reset_index(drop=True)
    for i in pdf['Freq']:
        lll.append(ttt[i])
    pdf['Rank'] = lll
    lili = []
    all_p = float(pdf['Rank'].max())
    for i in pdf['Rank']:
        t_p = (float(i)/all_p)*100
        print(t_p)
        lili.append('{:.3f}'.format(t_p))
    pdf['Percent'] = pd.DataFrame(lili).astype(float)
    print(pdf)
    return pdf,cdf
def analysis_R2(df,top_p,mins):
    outdf = df[df['Percent'] <= float(top_p)][df['Freq'] >= int(mins)]
    return outdf

def make_directory(a):
    try:
        if os.path.exists(a):
            os.chdir(a)
        else:
            os.mkdir(a)
            os.chdir(a)
    except:
        print('DIR make Error')

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('-top_p',required=True, default=100, help='Select the top X percent of R Group frequency.')
    parser.add_argument('-mins',required=True, default=1, help='The minimum number of R Group.')
    args=parser.parse_args()

    print(os.getcwd())
    conR2 = sql_connection_R2()
    conR2cursor = conR2.cursor()
    mlist = Manager().list()
    plist = Manager().dict()
    Ncpu = multiprocessing.cpu_count()
    tset = set()
    global conR2cursor
    global tset
    global plist
    FG_dic = load_FG()
    FG_dic2 = load_FG2()
    scf_list = SCF_result_load()
    input_df = input_Temp_R2('/ssd/swshin/1D_Scan.v2/Data/Input_CDK7_270/',FG_dic)#'/ssd/yklee/1D_Scan.v2/Data/Input/',FG_dic)
    pdf = input_analysis()
    odf = analysis_R2(pdf,args.top_p,args.mins)
    a = 0
    os.chdir('/lwork01/yklee/')
    try :
        if os.path.exists('Key_R2_search'):
            os.chdir('Key_R2_search')
            print('True')
            pass
        else:
            os.mkdir('Key_R2_search')
            os.chdir('Key_R2_search')
    except:
        print('Error')

    pdf.to_csv('Input_Temp_Freq.csv',index=False)
    odf.to_csv('Activate_Input.csv',index=False)
    odf['Rgroup']
    KR_result_analysis(k_set,mlist)
    txts = sorted(glob.glob('tmp_*.txt'))
    dfs = []
    for i in txts:
        df = pd.read_csv(i,header=None)
        dfs.append(df)
    tdf = pd.concat(dfs)
    global tdf
    lili = []
    for i in sorted(df[0].drop_duplicates()):
        df1 = dropop(i)
        lili.append(df1)

    df_fin = pd.concat(lili)
    df_fin.to_csv('SKR_filt.result.csv',index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-top_p', required=True, default=100, help='Select the top X percent of R Group frequency.')
    parser.add_argument('-mins', required=True, default=1, help='The minimum number of R Group.')
    args = parser.parse_args()

    print(os.getcwd())
    conR2 = sql_connection_R2()
    conR2cursor = conR2.cursor()
    mlist = Manager().list()
    plist = Manager().dict()
    clist = Manager().dict()
    Ncpu = multiprocessing.cpu_count()
    tset = set()
    global conR2cursor
    global tset
    global plist
    global clist
    FG_dic = load_FG()
    FG_dic2 = load_FG2()
    scf_list = SCF_result_load()
    input_df = input_Temp_R2('/ssd/swshin/1D_Scan.v2/Data/Input_CDK7_270/', FG_dic)  # '/ssd/yklee/1D_Scan.v2/Data/Input/',FG_dic)
    pdf = input_analysis()
    odf = analysis_R2(pdf, args.top_p, args.mins)
    a = 0
    os.chdir('/lwork01/yklee/')
    pdf.to_csv('Input_Temp_Freq.csv',index=False)
    odf.to_csv('Activate_Input.csv',index=False)
    iR2 = odf['Rgroup']
