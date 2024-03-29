#!/bin/bash

####### Reserve computing resources #############
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=12:00:00
#SBATCH --mem=32G
#SBATCH --partition=gpu
#SBATCH --gpus-per-node=1

source ~/software/init-conda
conda activate chris_env
python "/home/christian.valdez/DI-Automated-Scripts/core/3d_cnn.py"
conda deactivate