#!/bin/sh
#SBATCH --account=def-hanganua
#SBATCH --mem=8G
#SBATCH --time=05:00:00
#SBATCH --output=/scratch/hanganua/fs_zip.out

cd /home/$USER
#hanganua

./miniconda3/bin/python3.7 projects/def-hanganua/scripts/fs_stats_extract.py
