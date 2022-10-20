#!/bin/bash

#SBATCH --mem=64gb
#SBATCH --cpus-per-task=16
#SBATCH --time=96:00:00

module load biobakery_workflows
biobakery_workflows wmgx --input gitract --output bio4 --threads 16
