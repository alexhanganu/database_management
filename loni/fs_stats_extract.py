#!/bin/python
#2020 06 13

'''
extract stats
zip subjects in subjects_processed
after that is necessary to zip the processed_fs_stats and move it to the corresponding
storage folder (i.e., for ADNI is beluga../projects/../adni)
'''
from os import listdir, system, mkdir, path, chdir
import shutil, getpass

username = getpass.getuser()


path_proj = path.join('/home',username,'projects','def-hanganua')
path_scratch = path.join('/scratch',username)
path_processed = path.join(path_proj,'subjects_processed')

dir_stats = 'processed_fs_stats'
zip_f = dir_stats+'_20200609_1500.zip'
path_stats = path.join(path_scratch,dir_stats)


chdir(path_processed)

if not path.exists(path_stats):
    mkdir(path_stats)

stats_dirs = listdir(path_stats)

for subDIR in listdir(path_processed):
    if path.isdir(path.join(path_processed, subDIR)) and subDIR not in stats_dirs:
        print('extracting stats')
        mkdir(path_stats+'/'+subDIR)
        shutil.copytree(path.join(path_processed,subDIR,'stats'),path.join(path_stats,subDIR,'stats'))
        print('archiving ',subDIR)
        system('zip -q -r -m '+subDIR+'.zip '+subDIR)
    elif not path.isdir(path.join(path_processed, subDIR)):
        print(subDIR, ' not a directory')

chdir(path_scratch)
system('zip -q -r -m '+zip_f+' '+dir_stats)
shutil.move(path.join(path_scratch,zip_f), path.join(path_stats,zip_f))
