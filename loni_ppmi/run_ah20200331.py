import os.path
import pandas as pd

# import db_definitions_ppmi as db

path_main = [p for p in (os.environ['HOME'],'C:/Users/samue',
                         'J:', os.path.expanduser('~')) if os.path.exists(p)][0] + '/Dropbox'

file = path_main+'/lab/databases/ppmi/ppmi_database_2019_05_22.xlsx' #variable créée à retirer si ça ne fonctionne pas
sheet_BL = 'PPMI_Baseline_Data_02Jul2018'
sheet_gds = 'behav_depresssion_GDS_short' #variable créée à retirer si ça ne fonctionne pas
sheet_moca = 'cog_MOCA' #variable créée à retirer si ça ne fonctionne pas

# file_GDS = path_main+'/lab/samuel/ppmi/behavior/ppmi_database_2019_05_22_GDS.xlsx'
# file_MCA = path_main+'/lab/samuel/ppmi/behavior/ppmi_database_2019_05_22_MCA.xlsx'
#df_depression = pd.read_excel(file_GDS)
#df_perf_cog = pd.read_excel(file_MCA)


#df pour 1 mesure de NPS et 1 mesure de performance cognitive
df_bl = pd.read_excel(file, sheet_BL)
df_gds = pd.read_excel(file, sheet_gds)
df_moca = pd.read_excel(file, sheet_moca)

#Trier le df pour retirer APPRDX = 3 (SWEDD)
APPRDX_index = df_bl[df_bl['APPRDX'] == 3].index
df_bl.drop(APPRDX_index, inplace = True)


def get_nr_participants(col):
    ls_patno = list()
    for val in col:
        if val not in ls_patno: ls_patno.append(val)
    return ls_patno

print('baseline db has {} unique participants out of {} recordings'.format(len(get_nr_participants(df_bl.PATNO)), df_bl.PATNO.shape[0]))
print('gds db has {} unique participants out of {} recordings'.format(len(get_nr_participants(df_gds.PATNO)), df_gds.PATNO.shape[0]))
print('moca db has {} unique participants out of {} recordings'.format(len(get_nr_participants(df_moca.PATNO)), df_moca.PATNO.shape[0]))


# Extracting the data only for the participants from the BL database

ls_participants = df_bl.columns.tolist()


