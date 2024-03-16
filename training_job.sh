#!/bin/bash
#SBATCH --gpus-per-node=1
#SBATCH --cpus-per-task=6
#SBATCH --mem=8000M               # memory per node
#SBATCH --time=0-03:00
#SBATCH --time=02:45:00
#SBATCH --account=rstegman
module load python/3.11
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate
pip install --no-index --upgrade pip
pip install --no-index -r requirements.txt
python3 TrainScript.py