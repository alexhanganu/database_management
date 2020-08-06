#!/bin/sh
#SBATCH --account=def-hanganua
#SBATCH --mem=8G
#SBATCH --time=12:00:00
#SBATCH --output=/scratch/hanganua/database_loni_run_20200805.out

cd /home/$USER

./miniconda3/bin/python3.7 database/loni/unzip_rezip_individual.py
