#!/bin/bash

module load bowtie

bowtie2 -p 16 -x /data/TBHD_share/valencia/pipelines/woltka_db/databases/bowtie2/WoLr1 -1 /data/TBHD_share/cami_data/gitract/S1_GItract_HiSeq_cami_R1.fastq.gz -2 /data/TBHD_share/cami_data/gitract/S1_GItract_HiSeq_cami_R2.fastq.gz --very-sensitive --no-head --no-unal -k 16 --np 1 --mp "1,1" --rdg "0,1" --rfg "0,1" --score-min "L,0,-0.05" | cut -f1-9 | sed 's/$/\t*\t*/' | gzip > output.S1.sam.gz

bowtie2 -p 16 -x /data/TBHD_share/valencia/pipelines/woltka_db/databases/bowtie2/WoLr1 -1 /data/TBHD_share/cami_data/gitract/S2_GItract_HiSeq_cami_R1.fastq.gz -2 /data/TBHD_share/cami_data/gitract/S2_GItract_HiSeq_cami_R2.fastq.gz --very-sensitive --no-head --no-unal -k 16 --np 1 --mp "1,1" --rdg "0,1" --rfg "0,1" --score-min "L,0,-0.05" | cut -f1-9 | sed 's/$/\t*\t*/' | gzip > output.S2.sam.gz
