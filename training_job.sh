#!/bin/bash
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:v100:1 # you can atry p100 as well
#SBATCH --mem=8G # you can also try 16G 
#SBATCH --time=12:00:00
#SBATCH --account=def-skremer
#SBATCH --mail-user=rstegman@uoguelph.ca
#SBATCH --mail-type=ALL
module load python/3.11
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate
pip install --no-index --upgrade pip
pip install --no-index -r requirements.txt
module load cuda cudnn
export XLA_FLAGS=--xla_gpu_cuda_data_dir=$CUDA_HOME
python3 TrainScript.py