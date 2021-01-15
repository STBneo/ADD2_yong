import os,sys,glob,subprocess,apsw
import multiprocessing
from multiprocessing import Manager,Process
from functools import partial
import pandas as pd
from sqlite3 import Error
import sqlite3
import time
from datetime import datetime

def load_FG(): # checkmol output code - R Group Name
	tmp_dic={'000000T2': 'cation', '000000T1': 'anion', 'C2O10000': 'carbonyl_compound', 'C2O1H000': 'aldehyde', 'C2O1C000': 'ketone', \
	'C2S10000': 'thiocarbonyl_compound', 'C2S1H000': 'thioaldehyde', 'C2S1C000': 'thioketone', 'C2N10000': 'imine', 'C2N1N000': 'hydrazone', \
	'C2NNC4ON': 'semicarbazone', 'C2NNC4SN': 'thiosemicarbazone', 'C2N1OH00': 'oxime', 'C2N1OC00': 'oxime_ether', 'C3OC0000': 'ketene', \
	'C3OCC000': 'ketene_acetal_derivative', 'C2O2H200': 'carbonyl_hydrate', 'C2O2HC00': 'hemiacetal', 'C2O2CC00': 'acetal', 'C2NOHC10': 'hemiaminal',\
	'C2N2CC10': 'aminal', 'C2NSHC10': 'thiohemiaminal', 'C2S2CC00': 'thioacetal', 'C2CNH000': 'enamine', 'C2COH000': 'enol', 'C2COC000': 'enolether',\
	'O1H00000': 'hydroxy_compound', 'O1H0C000': 'alcohol', 'O1H1C000': 'prim_alcohol', 'O1H2C000': 'sec_alcohol', 'O1H3C000': 'tert_alcohol',\
	'O1H0CO1H': '1_2-diol', 'O1H0CN1C': '1_2-aminoalcohol', 'O1H1A000': 'phenol', 'O1H2A000': '1_2-diphenol', 'C2COH200': 'enediol', 'O1C00000': 'ether',\
	'O1C0CC00': 'dialkylether', 'O1C0CA00': 'alkylarylether', 'O1C0AA00': 'diarylether', 'S1C00000': 'thioether', 'S1S1C000': 'disulfide',\
	'O1O1C000': 'peroxide', 'O1O1H000': 'hydroperoxide', 'N1N10000': 'hydrazine_derivative', 'N1O1H000': 'hydroxylamine', 'N1C00000': 'amine',\
	'N1C10000': 'prim_amine', 'N1C1C000': 'prim_aliphat_amine', 'N1C1A000': 'prim_aromat_amine', 'N1C20000': 'sec_amine', 'N1C2CC00': 'sec_aliphat_amine',\
	'N1C2AC00': 'sec_mixed_amine_aryl_alkyl', 'N1C2AA00': 'sec_aromat_amine', 'N1C30000': 'tert_amine', 'N1C3CC00': 'tert_aliphat_amine',\
	'N1C3AC00': 'tert_mixed_amine', 'N1C3AA00': 'tert_arom_amine', 'N1C400T2': 'quaternary_ammonium_salt', 'N0O10000': 'N-oxide',\
	'XX000000': 'halogen_deriv', 'XX00C000': 'alkyl_halide', 'XF00C000': 'alkyl_fluoride', 'XC00C000': 'alkyl_chloride', 'XB00C000': 'alkyl_bromide',\
	'XI00C000': 'alkyl_iodide', 'XX00A000': 'aryl_halide', 'XF00A000': 'aryl_fluoride', 'XC00A000': 'aryl_chloride', 'XB00A000': 'aryl_bromide',\
	'XI00A000': 'aryl_iodide', '000000MX': 'organometallic_compound', '000000ML': 'organolithium_compound', '000000MM': 'organomagnesium_compound',\
	'C3O20000': 'carboxylic_acid_deriv', 'C3O2H000': 'carboxylic_acid', 'C3O200T1': 'carboxylic_acid_salt', 'C3O2C000': 'carboxylic_acid_ester',\
	'C3O2CZ00': 'lactone', 'C3ONC000': 'carboxylic_acid_imide', 'C3ONC100': 'carboxylic_acid_prim_amide', 'C3ONC200': 'carboxylic_acid_sec_amide',\
	'C3ONC300': 'carboxylic_acid_tert_amide', 'C3ONCZ00': 'lactam', 'C3ONN100': 'carboxylic_acid_hydrazide', 'C3ONN200': 'carboxylic_acid_azide',\
	'C3ONOH00': 'hydroxamic_acid', 'C3N2H000': 'carboxylic_acid_amidine', 'C3NNN100': 'carboxylic_acid_amidrazone', 'C3N00000': 'nitrile',\
	'C3OXX000': 'acyl_halide', 'C3OXF000': 'acyl_fluoride', 'C3OXC000': 'acyl_chloride', 'C3OXB000': 'acyl_bromide', 'C3OXI000': 'acyl_iodide', \
	'C2OC3N00': 'acyl_cyanide', 'C3NOC000': 'imido_ester', 'C3NXX000': 'imidoyl_halide', 'C3SO0000': 'thiocarboxylic_acid_deriv', \
	'C3SOH000': 'thiocarboxylic_acid', 'C3SOC000': 'thiocarboxylic_acid_ester', 'C3SOCZ00': 'thiolactone', 'C3SNH000': 'thiocarboxylic_acid_amide', \
	'C3SNCZ00': 'thiolactam', 'C3NSC000': 'imidothioester', 'C3ONAZ00': 'oxohetarene', 'C3SNAZ00': 'thioxohetarene', 'C3NNAZ00': 'iminohetarene', \
	'C3O30000': 'orthocarboxylic_acid_deriv', 'C3O3C000': 'carboxylic_acid_orthoester', 'C3O3NC00': 'carboxylic_acid_amide_acetal', \
	'C3O2C3O2': 'carboxylic_acid_anhydride', 'C3ONCH10': 'carboxylic_acid_unsubst_imide', 'C3ONCC10': 'carboxylic_acid_subst_imide', \
	'C4000000': 'CO2_deriv_(general)', 'C4O30000': 'carbonic_acid_deriv', 'C4O3C100': 'carbonic_acid_monoester', 'C4O3C200': 'carbonic_acid_diester', \
	'C4O3CX00': 'carbonic_acid_ester_halide', 'C4SO0000': 'thiocarbonic_acid_deriv', 'C4SOC100': 'thiocarbonic_acid_monoester', \
	'C4SOC200': 'thiocarbonic_acid_diester', 'C4SOX_00': 'thiocarbonic_acid_ester_halide', 'C4O2N000': 'carbamic_acid_deriv', \
	'C4O2NH00': 'carbamic_acid', 'C4O2NC00': 'carbamic_acid_ester_urethane', 'C4O2NX00': 'carbamic_acid_halide', \
	'C4SN0000': 'thiocarbamic_acid_deriv', 'C4SNOH00': 'thiocarbamic_acid', 'C4SNOC00': 'thiocarbamic_acid_ester', \
	'C4SNXX00': 'thiocarbamic_acid_halide', 'C4O1N200': 'urea', 'C4N2O100': 'isourea', 'C4S1N200': 'thiourea', 'C4N2S100': 'isothiourea', \
	'C4N30000': 'guanidine', 'C4ON2N00': 'semicarbazide', 'C4SN2N00': 'thiosemicarbazide', 'N4N20000': 'azide', 'N2N10000': 'azo_compound', \
	'N3N100T2': 'diazonium_salt', 'N3C10000': 'isonitrile', 'C4NO1000': 'cyanate', 'C4NO2000': 'isocyanate', 'C4NS1000': 'thiocyanate', \
	'C4NS2000': 'isothiocyanate', 'C4N20000': 'carbodiimide', 'N2O10000': 'nitroso_compound', 'N4O20000': 'nitro_compound', 'N3O20000': 'nitrite', \
	'N4O30000': 'nitrate', 'S6O00000': 'sulfuric_acid_deriv', 'S6O4H000': 'sulfuric_acid', 'S6O4HC00': 'sulfuric_acid_monoester', \
	'S6O4CC00': 'sulfuric_acid_diester', 'S6O3NC00': 'sulfuric_acid_amide_ester', 'S6O3N100': 'sulfuric_acid_amide', 'S6O2N200': 'sulfuric_acid_diamide', \
	'S6O3XX00': 'sulfuryl_halide', 'S5O00000': 'sulfonic_acid_deriv', 'S5O3H000': 'sulfonic_acid', 'S5O3C000': 'sulfonic_acid_ester', \
	'S5O2N000': 'sulfonamide', 'S5O2XX00': 'sulfonyl_halide', 'S4O20000': 'sulfone', 'S2O10000': 'sulfoxide', 'S3O00000': 'sulfinic_acid_deriv', \
	'S3O2H000': 'sulfinic_acid', 'S3O2C000': 'sulfinic_acid_ester', 'S3O1XX00': 'sulfinic_acid_halide', 'S3O1N000': 'sulfinic_acid_amide', \
	'S1O00000': 'sulfenic_acid_deriv', 'S1O1H000': 'sulfenic_acid', 'S1O1C000': 'sulfenic_acid_ester', 'S1O0XX00': 'sulfenic_acid_halide', \
	'S1O0N100': 'sulfenic_acid_amide', 'S1H10000': 'thiol', 'S1H1C000': 'alkylthiol', 'S1H1A000': 'arylthiol', 'P5O0H000': 'phosphoric_acid_deriv', \
	'P5O4H200': 'phosphoric_acid', 'P5O4HC00': 'phosphoric_acid_ester', 'P5O3HX00': 'phosphoric_acid_halide', 'P5O3HN00': 'phosphoric_acid_amide', \
	'P5O0S000': 'thiophosphoric_acid_deriv', 'P5O3SH00': 'thiophosphoric_acid', 'P5O3SC00': 'thiophosphoric_acid_ester', 'P5O2SX00': 'thiophosphoric_acid_halide', \
	'P5O2SN00': 'thiophosphoric_acid_amide', 'P4O30000': 'phosphonic_acid_deriv', 'P4O3H000': 'phosphonic_acid', 'P4O3C000': 'phosphonic_acid_ester', \
	'P3000000': 'phosphine', 'P2O00000': 'phosphinoxide', 'B2O20000': 'boronic_acid_deriv', 'B2O2H000': 'boronic_acid', 'B2O2C000': 'boronic_acid_ester', \
	'000C2C00': 'alkene', '000C3C00': 'alkyne', '0000A000': 'aromatic_compound', '0000CZ00': 'heterocyclic_compound', 'C3O2HN1C': 'alpha-aminoacid', \
	'C3O2HO1H': 'alpha-hydroxyacid'}
	return tmp_dic

def sql_connection():
	try:
		con = apsw.Connection(':memory:')
		return con
	except Error:
		print(Error)

def sql_create_table(con):
	cursorObj = con.cursor()
	cursorObj.execute("CREATE TABLE R_Table(Rgroup txt PRIMARY KEY, ZID text)")
	return

def sql_insert(con,rid,zids,sub_dict):
	cursorObj = con.cursor()
	try:
		query = 'INSERT INTO R_Table(Rgroup,zid) VALUES(?,?)'
		cursorObj.execute(query,(rid,zids))
		#cursorObj.execute("INSERT INTO R_Table(Rgroup,zid) VALUES(?,?)",entities)
		return 1
	except :
		print(rid)
		sub_dict[rid] = zids_string
		return 0

def sql_update(con,entities):
	cursorObj = con.cursor()
	try:
		cursorObj.execute('UPDATE R_Table SET zid=? WHERE Rgroup=?',entities)
	except:
		sys.exit()

def temp_DB_connection(a):
	try :
		con = apsw.Connection(a)
		return con
	except Error:
		print(Error)
	return
def temp_DB_work(a,rgroup):
	id_list = Manager().list()
	con = temp_DB_connection(a)
	cursorObj = con.cursor()
	query = "SELECT * FROM R_Table WHERE Rgroup LIKE \'%s\'"%rgroup
	cursorObj.execute(query)
	rows = cursorObj.fetchall()
	con.close()
	if not rows:
		pass

	else :
		zids_str = unicode.encode(rows[0][1],'utf-8')
		zids_list = list(set(zids_str.split(',')))
		Ncpu = multiprocessing.cpu_count()
		pool = multiprocessing.Pool(Ncpu -1)
		func = partial(multi_work,lili=id_list)
		pool.map(func,zids_list)
		pool.close()
		pool.join()

		zids_set = set(id_list)

		return zids_set


def multi_work(a,lili):
	if '_' in a:
		print(a)
		pass
	else:
		lili.append(a)
def memoryDB2diskDB(con,DB_name): # memory DB to Disk DB
	dest = apsw.Connection(DB_name)
	with dest.backup('main',con,'main') as backup:
		backup.step()
	dest.close()

if __name__ == "__main__" :

	R_dic = load_FG()
	con_main = sql_connection()
	sql_create_table(con_main)
	main_dict = {}
	sub_dict = {}


	d_list = sorted([d for d in os.listdir('.') if not os.path.isfile(d)])
	for key in R_dic.k:
			passeys():
		fg = R_dic[key]
		zids_set = set()
		print(fg)
		for d in d_list:
			print(d)
			d_db = d + '/final_inte.db'
			temp_set = temp_DB_work(d_db,fg)
			if not temp_set:
				pass
			else:
				zids_set = zids_set | temp_set
		if not zids_set
		else:
			zids_list = list(zids_set)
			print(len(zids_list))
			zids_string = ','.join(zids_list)
			sql_insert(con_main,fg,zids_string,sub_dict)


	memoryDB2diskDB(con_main,'test.db')
	#tmpdf = pd.DataFrame.from_dict(main_dict,orient='index').reset_index().rename(columns={'index':'Rgroup'})
	subdf = pd.DataFrame.from_dict(sub_dict,orient='index').reset_index().rename(columns={'index':'Rgroup'})
	#print(tmpdf.columns)
	#con = sqlite3.connect('test1.db')
	#tmpdf.to_sql('R_Table',con,index=False)
	subdf.to_pickle('subname.pkl')
