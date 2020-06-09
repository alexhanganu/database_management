#!/bin/python

'''
extract stats
zip subjects in subjects_processed
after that is necessary to zip the processed_fs_stats and move it to the corresponding
storage folder (i.e., for ADNI is beluga../projects/../adni)
'''

pproj = '/home/hanganua/projects/def-hanganua'
pscratch = '/scratch/hanganua'
path_processed = pproj+'/subjects_processed'
path_stats = pscratch+'/processed_fs_stats'

from os import listdir, system, mkdir, path, chdir
import shutil

chdir(path_processed)

if not path.exists(path_stats):
    mkdir(path_stats)

stats_dirs = listdir(path_stats)

for subDIR in listdir(path_processed):
    if subDIR not in stats_dirs:
        print('extracting stats')
        mkdir(path_stats+'/'+subDIR)
        shutil.copytree(path_processed+'/'+subDIR+'/stats',path_stats+'/'+subDIR+'/stats')
    print('archiving ',subDIR)
    system('zip -q -r -m '+subDIR+'.zip '+subDIR)

