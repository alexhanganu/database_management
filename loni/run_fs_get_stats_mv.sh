#!/bin/sh
#SBATCH --account=def-hanganua
#SBATCH --mem=8G
#SBATCH --time=05:00:00
#SBATCH --output=/scratch/hanganua/fs_get_stats_move.out

cd /home/$USER

./miniconda3/bin/python3.7 projects/def-hanganua/scripts/fs_get_stats_mv2remote.py
