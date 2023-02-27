import os
import argparse
from typing import List


def parse_args() -> argparse.Namespace:
    # Parse arguments for input and output.
    parser = argparse.ArgumentParser(description='Classify WOL data.')
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='Input file.')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='Output dir.')
    args = parser.parse_args()

    return args


def get_files(input_dir: str) -> List[str]:
    sam_files = []
    for file in os.listdir(input_dir):
        if file.endswith(".sam.gz"):
            sam_files.append(os.path.join(input_dir, file))

    return sam_files


def write_classify(sam_files: List[str], output_dir: str, mem: int = 64, cpus: int = 16) -> None:
    line = """woltka classify -i {} --to-tsv -o {}_classify -r genus,species --map /gpfs/gsfs12/users/TBHD_share/valencia/pipelines/woltka_db/taxonomy/taxid.map --nodes /gpfs/gsfs12/users/TBHD_share/valencia/pipelines/woltka_db/taxonomy/nodes.dmp --names /gpfs/gsfs12/users/TBHD_share/valencia/pipelines/woltka_db/taxonomy/names.dmp"""

    with open("submit_classify.sh", "w") as f:
        f.write("#!/bin/bash\n\n")
        f.write(f"#SBATCH --mem={mem}gb\n")
        f.write(f"#SBATCH --cpus-per-task={cpus}\n\n")

        for file in sam_files:
            print(file)
            id = file.split("/")[-1].split(".")[0]
            # print(id)
            output = os.path.join(output, id)
            # print("output: ", output, "\n")
            new_line = line.format(file, output)
            # print(new_line)
            f.write(new_line + "\n")


def write_classify_swarm(sam_files: List[str], output_dir: str, mem: int = 64, cpus: int = 16) -> None:
    line = """woltka classify -i {} --to-tsv -o {}_classify -r genus,species --map /gpfs/gsfs12/users/TBHD_share/valencia/pipelines/woltka_db/taxonomy/taxid.map --nodes /gpfs/gsfs12/users/TBHD_share/valencia/pipelines/woltka_db/taxonomy/nodes.dmp --names /gpfs/gsfs12/users/TBHD_share/valencia/pipelines/woltka_db/taxonomy/names.dmp"""
    with open(os.path.join(output_dir, "submit_classify.swarm"), "w") as f:
        f.write(f"#SWARM -t {cpus} -g {mem} --time 08:00:00\n\n")

        for file in sam_files:
            print(file)
            id = file.split("/")[-1].split(".")[0]
            # print(id)
            output = os.path.join(output_dir, id)
            # print("output: ", output, "\n")
            new_line = line.format(file, output)
            # print(new_line)
            f.write(new_line + "\n")


if __name__ == "__main__":
    args = parse_args()

    print(os.listdir(args.input))

    sam_files = get_files(args.input)
    write_classify_swarm(sam_files, args.output)
