#!/bin/bash

#SBATCH --mem=128gb
#SBATCH --cpus-per-task=64
#SBATCH --time=96:00:00

module load biobakery_workflows
biobakery_workflows wmgx --input /gpfs/gsfs12/users/TBHD_share/valencia/pipelines/scripts/do_pipeline/testfiles/READS --output /gpfs/gsfs12/users/TBHD_share/valencia/pipelines/scripts/do_pipeline/testfiles/bio4 --threads 64 --input-extension fastq