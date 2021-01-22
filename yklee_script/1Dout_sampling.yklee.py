import pandas as pd
import os,sys,glob

def pos_dic():
    temp_dic = {'CDK7':['STK-376446031456-A1','STK-26629259461-A1','STK-152706924212-A1','STK-19872284772-A1','ZINC000467398634','STK-29419266085-A1'],\
                'FLT3':['STK-104792343581-A1','STK-338967584352-A1','STK-129392591749-A1','STK-244697288077-A1','STK-13636493024-A1','STK-246153985853-A1',\
                        'STK-80969256480-A1','STK-102230801700-A1','STK-113703177344-A1','STK-60238427861-A1','STK-113703177344-A1','STK-246043080221-A1',\
                        'STK-104816419125-A1','STK-113792065920-A1','STK-357424032416-A1','STK-166761762084-A1','STK-75975397536-A1','STK-75122599797-A1',\
                        'STK-366178474613-A1','STK-109960042197-A1','STK-124462869812-A1','STK-488248697949-A1','STK-136889514596-A1','STK-196699720397-A1',\
                        'STK-364407386637-A1','STK-102760891117-A1','STK-335901123965-A1','STK-487906208416-A1','STK-332371952676-A1','STK-14970553696-A1',\
                        'STK-186157279924-A1','STK-123554127456-A1','STK-135985165405-A1','STK-112883773397-A1','STK-55180211968-A1'],\
                'EGFR':['STK-177298426368-A1','STK-246043817908-A1','STK-245902935637-A1','STK-74390016832-A1','STK-246043080221-A1','STK-135312497885-A1',\
                        'STK-134884161844-A1','STK-231452937316-A1','ZINC000009059860'],\
                'ERBB4':['STK-25355881653-A1','STK-277116816032-A1','STK-101589425764-A1','STK-309085593012-A1','ZINC000033260731','STK-47553346496-A1']}
    return temp_dic

def ra_work(afile,ra_list):
    with open(afile + '_ra.txt','w') as W:
        for line in ra_list:
            W.write(line + '\n')

def right_answer(afile,df,input):
    R_name = afile.split('.')[-2]
    Pos_dic = pos_dic()
    pos_list = Pos_dic[input]
    ra_list = []
    for i in pos_list:
        idx = df[df['ZINC_ID']==i][:1].reset_index()['index']
        if idx.empty:
            pass
        else:
            print("Right Answer ... %s %s %s"%(i,R_name,''.join(idx.values.astype(str))))
            ra_list.append('\t'.join([i,R_name,''.join(idx.values.astype(str))]))
    ra = '\n'.join(ra_list)
    return ra

def Only_remain_table(afile):
    R_name = afile.split('.')[-2]
    with open(f,'r') as F:
        set1 = set(F.readlines())
        set1.discard('ZINC_ID,Main_Key_ID,Main_Key_freq,Sub_Key,Sub_Key_freq\n')
        flines = ''.join(set1).strip().split('\n')
    df = pd.DataFrame(flines)
    df['ZINC_ID'] = df[0].str.split(',').str[0]
    df['Freq'] = df[0].str.split(',').str[1].astype(int)
    df['Round'] = R_name
    df2 = df.sort_values(by=['Freq'],ascending=False).reset_index().drop([0,'index'],axis=1)
    return df2


if __name__ == "__main__":
    input_name = sys.argv[1]
    f_list = sorted(glob.glob('140K_%s_1DOUT/*/All.f.final_re.*'%(input_name)))
    n = int(sys.argv[2])
    n_samp = int(n)//int(len(f_list))
    df_list = []
    ra_list = []
    for f in f_list:
        df = Only_remain_table(f)
        #df_list.append(df[:n_samp])
        ra_list.append(right_answer(f,df,input_name))
        df_list.append(df[:n_samp].reset_index().drop('index',axis=1))
    ra_work(input_name,ra_list)
    adf = pd.concat(df_list)
    adf.to_csv(input_name + '_total_' + str(n) + '.txt',sep='\t',index=False)
