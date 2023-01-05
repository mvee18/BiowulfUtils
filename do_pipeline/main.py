# This script will run all the pipelines for the given set of samples.
import argparse
import os
from os.path import abspath
from dataclasses import dataclass
from typing import List, Tuple

# <--- Global variables --->
debug_input = "/Volumes/TBHD_share/valencia/pipelines/microbio_spectrum/CLEANED/trimmedreads"
if not os.path.exists(debug_input):
    raise Exception("Input file directory does not exist")

debug_output = "/Volumes/TBHD_share/valencia/pipelines/microbio_spectrum/CLEANED/pipelines"


pipeline_names = ["jams", "bio4", "wgsa2", "woltka"]

# <--- Dataclass Definitions --->


@dataclass
class Pipeline:
    name: str
    output_dir: str

    def __post_init__(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        # Readd this later to warn the user if the output directory is not empty.
        # else:
        #     raise Exception(
        #         f"Output directory for {self.name} already exists!")


@dataclass
class Biobakery(Pipeline):
    def make_biobakery_input(self, input_dir: str, output_dir: str, ext: str, mem: int = 128, cpus: int = 64, time: int = 96):
        template = """#!/bin/bash

#SBATCH --mem={}gb
#SBATCH --cpus-per-task={}
#SBATCH --time={}:00:00

module load biobakery_workflows
biobakery_workflows wmgx --input {} --output {} --threads {} --input-extension {}""".format(mem, cpus, time, input_dir, output_dir, cpus, ext)

        # Write this to a file to test for now.
        with open(os.path.join(self.output_dir, "bio4.sh"), "w") as f:
            f.write(template)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", help="Input directory with QC-checked/trimmed reads with pairs containing .R1, .R2", required=True)
    parser.add_argument(
        "-e", "--ext", help="Extension of the input files (ex: fastq, fastq.gz)", required=True, default="fastq")
    parser.add_argument(
        "-o", "--output", help="Output directory", required=True)
    return parser.parse_args()

# First, we need to make the directories for the output. We will make a directory for each pipeline.


def make_classes(output_dir) -> Tuple[Biobakery]:
    ps = []
    for p in pipeline_names:
        if p == "bio4":
            ps.append(Biobakery(p, os.path.join(output_dir, p)))

    return ps[0]


if __name__ == "__main__":
    biobakery = make_classes(debug_output)
    print(biobakery)

    biobakery.make_biobakery_input(debug_input, biobakery.output_dir, "fastq")
