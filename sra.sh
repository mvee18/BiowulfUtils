#!/bin/bash 
#SBATCH --mem=128gb
#SBATCH --cpus-per-task=16
#SBATCH --gres=lscratch:150

sra_num=$1
out_dir=$2

mkdir -p  /data/$USER/sra
module load sratoolkit
fasterq-dump -t /lscratch/$SLURM_JOBID -O $out_dir $sra_num
