# This script will run all the pipelines for the given set of samples.
import os  # nopep8
import sys  # nopep8
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  # nopep8

from wol.wol_bowtie import make_bowtie_swarm, get_paired_files
from wol.wol_classify import write_classify_swarm
from wol.wol_decontaminate import find_and_zip_files, write_decontaminate_swarm
import argparse
from os.path import abspath
from dataclasses import dataclass
from typing import List, Tuple
import subprocess

# from wol.wol_classify import make_classify_swarm


# <--- Global variables --->
# debug_input = "/Volumes/TBHD_share/valencia/pipelines/microbio_spectrum/CLEANED/trimmedreads"
# debug_input = "/data/TBHD_share/valencia/pipelines/microbio_spectrum/CLEANED/trimmedreads"
# if not os.path.exists(debug_input):
# raise Exception("Input file directory does not exist")

# debug_output = "/Volumes/TBHD_share/valencia/pipelines/microbio_spectrum/CLEANED/pipelines"
# debug_output = "/data/TBHD_share/valencia/pipelines/microbio_spectrum/CLEANED/pipelines"

# debug_extension = ".fastq"

jams_db_path = abspath("/data/TBHD_share/valencia/jams_db/JAMSdb202201")


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
    def make_input(self, input_dir: str, ext: str, mem: int = 128, cpus: int = 64, time: int = 96) -> None:
        template = """#!/bin/bash

#SBATCH --mem={}gb
#SBATCH --cpus-per-task={}
#SBATCH --time={}:00:00

module load biobakery_workflows
biobakery_workflows wmgx --input {} --output {} --threads {} --input-extension {}""".format(mem, cpus, time, input_dir, self.output_dir, cpus, ext)

        # Write this to a file to test for now.
        with open(os.path.join(self.output_dir, "bio4.sh"), "w") as f:
            f.write(template)


@dataclass
class JAMS(Pipeline):
    db_path: str

    def make_input(self, input_dir: str) -> None:
        # We will see if we can system call JAMSmakeswarm rather than rolling our own.
        jams_swarm_fp = os.path.join(self.output_dir, "JAMS.swarm")
        submit_fp = os.path.join(self.output_dir, "submit.sh")
        subprocess.run(["JAMSmakeswarm", "-r", input_dir,
                       "-o", self.output_dir, "-d", self.db_path, "-s", jams_swarm_fp])

        with open(submit_fp, 'w') as f:
            f.write(
                "swarm -g 246 -t 56 --time=24:00:00 --module R,samtools --gres=lscratch:400 -f JAMS.swarm")


def generate_sam_paths(paired_files: List[Tuple[str, str]], output_dir: str) -> List[str]:
    """
    Generates the path to the new sam.gz files with the desired prefix. Should be equivalent to the output of the bowtie pipeline.
    """
    sam_paths = []
    for pair in paired_files:
        prefix = pair[0].split("/")[-1].split("_")[0]
        sam_file_path = abspath(os.path.join(output_dir, prefix + ".sam.gz"))
        sam_paths.append(sam_file_path)

    return sam_paths


@dataclass
class Woltka(Pipeline):
    def make_bowtie(self, input_dir: str, ext: str, tasks: int = 16):
        make_bowtie_swarm(input_dir=input_dir,
                          output_dir=self.output_dir, extension=ext, tasks=tasks)

    def make_classify(self, input_dir: str, extension: str):
        # Make a new directory in the output directory for the classify.
        classify_dir = os.path.join(self.output_dir, "classify")
        if not os.path.exists(classify_dir):
            os.makedirs(classify_dir)

        # Get the paired files from the input directory.
        files = get_paired_files(input_dir=input_dir, extension=extension)
        sam_paths = generate_sam_paths(files, self.output_dir)

        write_classify_swarm(sam_files=sam_paths, output_dir=classify_dir)


# <--- Main --->


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", help="Input directory with QC-checked/trimmed reads with pairs containing _R1, _R2", required=True)
    parser.add_argument(
        "-e", "--ext", help="Extension of the input files (ex: fastq, fastq.gz)", required=True, default="fastq")
    parser.add_argument(
        "-o", "--output", help="Output directory", required=True)
    return parser.parse_args()

# First, we need to make the directories for the output. We will make a directory for each pipeline.


def make_classes(output_dir) -> Tuple[Biobakery, JAMS, Woltka]:
    bio = Biobakery(name="bio4", output_dir=abspath(
        os.path.join(output_dir, "bio4")))
    jams = JAMS(name="jams", output_dir=abspath(os.path.join(
        output_dir, "jams")), db_path=jams_db_path)
    woltka = Woltka(name="woltka", output_dir=abspath(
        os.path.join(output_dir, "woltka")))

    return bio, jams, woltka


if __name__ == "__main__":
    args = get_args()
    input_dir = abspath(args.input)
    output_dir = abspath(args.output)

    bio, jams, woltka = make_classes(args.output)

    # Now, we need to make the input files for each pipeline.
    bio.make_input(input_dir=input_dir, ext=args.ext)

    jams.make_input(input_dir=input_dir)

    woltka.make_bowtie(input_dir=input_dir, ext=args.ext)
    woltka.make_classify(input_dir=input_dir, extension=args.ext)
