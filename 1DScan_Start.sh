cd Tools

if [ $# -eq 0 ]
    then
        python what_time.py 'Start Automatic' 
        
        python what_time.py 'Generate key'
        rm -r ../Data/Key_Info ../Data/Table
        mkdir ../Data/Key_Info ../Data/Table
        python Key_gen.M.v2.db.py 5

        python what_time.py 'Make key table'
        bash Make_Key_Table.v3.sh

        python what_time.py 'Extract key from table'
        rm ../input.key.m.list.txt
        python Extrat_Key_from_Table.M.py

else
    python what_time.py 'Start Manual'

fi

cd ..

python ./Tools/what_time.py 'Find ZINC15 ID which has key'
python 1DScan_Only_Key.ZINC.list.FP.v6.db.py input.key.m.list.txt

cd Tools

python what_time.py 'Filt by 8 methods'
rm -r ../Data/Dic_Lib_Input
mkdir ../Data/Dic_Lib_Input
python Filter.re.ZINC.v2.db.FP.py

python what_time.py 'Extract SDF file'
python Extract_sdf_DB.v5.py

python what_time.py 'Annotate by RO5 and chemprop'
python Annotation_FAF_chemprop.v3.py

python what_time.py 'Filt by RO5 and chemprop'
python Final_Filtering.v2.py y 0 500 5 10 5 0 0.5

python what_time.py 'Extact PDB file'
python Final_Extract_PDB.v2.py n

python what_time.py 'End'
