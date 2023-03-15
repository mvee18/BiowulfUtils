#!/bin/bash
#SBATCH --cpus-per-task=32
#SBATCH --mem=128g
#SBATCH --time=12:00:00
#SBATCH --gres=lscratch:400

# source ~/.bash_profile
# getsunbeam
sunbeam run -- --configfile sunbeam_config.yml all_classify --cores 32
