#!/bin/sh
#SBATCH --account=def-hanganua
#SBATCH --mem=8G
#SBATCH --time=20:00:00
#SBATCH --output=/scratch/hanganua/database_loni_run_20200810.out

cd /home/$USER

./miniconda3/bin/python3.7 database_management/loni/unzip_rezip_individual.py

