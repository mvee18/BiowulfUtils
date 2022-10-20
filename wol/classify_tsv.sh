#!/bin/bash
# SBATCH --mem=64gb
# SBATCH --cpus-per-task=16

id="S2"

woltka classify -i "align/output.${id}.sam.gz" --to-tsv -o "${id}_classify" -r genus,species --map /gpfs/gsfs12/users/TBHD_share/valencia/pipelines/woltka/db/taxonomy/taxid.map --nodes /gpfs/gsfs12/users/TBHD_share/valencia/pipelines/woltka/db/taxonomy/nodes.dmp --names /gpfs/gsfs12/users/TBHD_share/valencia/pipelines/woltka/db/taxonomy/names.dmp
