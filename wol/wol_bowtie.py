import os
import argparse
from typing import List, Tuple


def parse_args() -> argparse.Namespace:
    # Parse the command line arguments
    # We need one for input and one for output.
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    parser.add_argument('-t', '--tasks', type=int, default=16)
    parser.add_argument('-e', '--extension', type=str, default=".fastq")
    args = parser.parse_args()

    return args


def get_paired_files(input_dir: str, extension: str) -> List[Tuple[str, str]]:
    files = []
    for file in os.listdir(input_dir):
        if file.endswith(extension):

            files.append(os.path.join(input_dir, file))

    files.sort()

    # Make a list of tuples of the paired files.
    paired_files = []
    for i in range(0, len(files), 2):
        paired_files.append((files[i], files[i+1]))

    return paired_files

def generate_prefixes(paired_files: List[Tuple[str, str]]) -> List[str]:
    prefixes = []
    for pair in paired_files:
        prefixes.append(pair[0].split("/")[-1].split("_")[0])

    return prefixes

def make_bowtie_swarm(input_dir: str, output_dir: str, tasks: int, extension: str) -> None:
    paired_files = get_paired_files(input_dir, extension)
    # We need to make a bash script to run bowtie2 on all the files.
    with open(os.path.join(output_dir, "submit_bowtie.swarm"), "w") as f:
        # f.write("#!/bin/bash\n\n")
        # f.write("module load bowtie\n\n")
        f.write(
            f"#SWARM -t {tasks} -g 32 --time 08:00:00 --module bowtie\n\n")

        for pair in paired_files:
            prefix = pair[0].split("/")[-1].split("_")[0]
            line = """bowtie2 -p {} -x /data/TBHD_share/valencia/pipelines/woltka_db/databases/bowtie2/WoLr1 -1 {} -2 {} --very-sensitive --no-head --no-unal -k 16 --np 1 --mp "1,1" --rdg "0,1" --rfg "0,1" --score-min "L,0,-0.05" | cut -f1-9 | sed 's/$/\\t*\\t*/' | gzip > {}.sam.gz""".format(
                tasks, pair[0], pair[1], prefix)
            f.write(line + "\n")


if __name__ == "__main__":
    args = parse_args()

    make_bowtie_swarm(args.input, args.output, args.tasks, args.extension)
