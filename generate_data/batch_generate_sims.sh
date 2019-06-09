#!/bin/bash
#SBATCH -N1
#SBATCH -n 1
#SBATCH -p cca
#SBATCH --array=0-9
#SBATCH --exclusive
#SBATCH --constraint=skylake
#SBATCH --time=3-00:00:00


#--gres=gpu:1
#--constraint=v100
#--constraint=p100
#-p gpu
#--mem 500000
#--constraint=v100
#--gres=gpu:4
#--exclusive
#-t 0-10:00
#--mem 500000
#-p bnl
#python run_hdbscan_like_enlink.py 100 140
#10 nodes, 40 tasks/node - use this to cut it up!

#echo ${SLURM_ARRAY_TASK_ID}
#python run_hdbscan_batch.py ${SLURM_ARRAY_TASK_ID} 4 1

srun bash -c 'echo $(hostname) $SLURM_PROCID && $HOME/miniconda3/envs/main/bin/python try_running_resonant.py ${SLURM_ARRAY_TASK_ID}'
