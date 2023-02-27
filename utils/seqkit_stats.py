# This script will make a swarm file to run seqkit stats on all the fastq files in a directory.

import os
from os.path import exists, abspath
from dataclasses import dataclass
from typing import List
import argparse


@dataclass
class Data:
    name: str
    path: str

    def __post_init__(self):
        if not exists(self.path):
            raise FileNotFoundError(f"Path {self.path} does not exist.")


# Define your data paths here.
# <-- Could write a parser for a separate input file to make this more flexible. But that's someone else's problem. -->
bmock12 = Data(
    name="bmock12", path="/data/TBHD_share/valencia/pipelines/bmock12/data/subs")
camisim = Data(
    name="camisim", path="/data/TBHD_share/cami_data/gitract/QC/fastp/CLEANREADS")
tourlousse = Data(name="tourlousse",
                  path="/data/TBHD_share/valencia/pipelines/microbio_spectrum/CLEANED/trimmedreads")
amos_hilo = Data(name="amos_hilo",
                 path="/data/TBHD_share/valencia/pipelines/amos/nibsc/hilo/data/fastp_cutbases")
amos_mixed = Data(name="amos_mixed",
                  path="/data/TBHD_share/valencia/pipelines/amos/nibsc/mixed/data/fastp")
nist = Data(name="nist",
            path="/data/TBHD_share/valencia/pipelines/NIST/fqfiles/fastp/CLEANREADS")
hmp_gut = Data(name="hmp_gut",
               path="/data/TBHD_share/valencia/pipelines/HMP/gut/trim_reads/READS")

data_list = [bmock12, camisim, tourlousse,
             amos_hilo, amos_mixed, nist, hmp_gut]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Make a swarm file to run seqkit stats on all the fastq files in a directory.")
    parser.add_argument(
        "-o", "--output", help="Where the output files should be created.", required=True)
    parser.add_argument(
        "-e", "--extension", help="The extension of the input files, default to fastq.", default="fastq")
    return parser.parse_args()


def make_seqtk_line(file, output_file) -> str:
    return f"seqkit stats {file} >> {output_file}\n"


def make_seqtk_swarm(data_list: List[Data], output_dir: str, ext: str) -> None:
    # Open the overall swarm file.
    with open("seqkit_stats.swarm", "w") as swarm:
        swarm.write(
            f"#SWARM -t {2} -g 8 --time 04:00:00 --module seqkit --partition quick\n")
        # For each data set...
        for d in data_list:
            # Make a separate output file...
            output_file = abspath(os.path.join(output_dir, f"{d.name}.out"))

            fastq_files = list(
                filter(lambda x: x.endswith(ext), os.listdir(d.path)))

            print(f"{len(fastq_files)} samples in {d.name}")

            # Then, for each file in the directory that ends with the extension...
            for f in fastq_files:
                # print(f)
                # Add a line to the swarm file to run seqkit stats on that file and append its output to the output_file above.
                swarm.write(make_seqtk_line(
                    abspath(os.path.join(d.path, f)), output_file))


if __name__ == "__main__":
    args = parse_args()

    make_seqtk_swarm(data_list=data_list,
                     output_dir=args.output, ext=args.extension)
