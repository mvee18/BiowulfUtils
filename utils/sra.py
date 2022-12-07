import argparse
import os
from typing import List

def read_input(fp: str) -> List[str]:
    """Reads input file and returns list of lines corresponding to the SRA numbers."""
    with open(fp, "r") as f:
        return f.read().splitlines()

def write_swarm(fp: str, output_dir: str, sra_list: List[str]) -> None:
    """Writes a swarm file that can be used to download the SRA files."""
    with open(fp, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("#SWARM -t 8 -g 16 --time 04:00:00 --module sratoolkit --gres=lscratch:200\n\n")
        for sra in sra_list:
            f.write(f"fasterq-dump -t /lscratch/$SLURM_JOBID -O {output_dir} {sra}\n")

def parse_args() -> argparse.Namespace:
    """Parses command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, help="Input file containing SRA numbers, one per line.")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output directory for SRA files.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    sra_list = read_input(args.input)
    output_dir = os.path.abspath(args.output)
    print("Writing swarmfile to {}.".format(output_dir))
    os.makedirs(output_dir, exist_ok=True)
    write_swarm(os.path.join(output_dir, "sra.swarm"), output_dir, sra_list)
