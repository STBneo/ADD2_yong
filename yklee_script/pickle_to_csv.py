import pandas as pd
import glob,os

if __name__ == "__main__" :
	pkl_list = sorted(glob.glob('*.pkl'))
	for i in pkl_list:
		fn = i.split('.')[0]
		if os.path.exists('CSV_DIR/' + fn + '.csv'):
			pass
		else:
			print(i)
			df = pd.read_pickle(i)
			df.to_csv('CSV_DIR/' + fn + '.csv',index=False)
