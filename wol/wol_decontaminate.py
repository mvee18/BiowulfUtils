import argparse
import os
from os.path import abspath
from typing import List, Tuple


def parse_arguments() -> argparse.Namespace:
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser(
        description='Creates a swarmfile to decontaminate reads using KneadData.')
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='Input directory containing files to be decontaminated.')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='Output dir.')
    parser.add_argument('-e', '--extension', type=str, default='fastq',
                        help="The file extension of the input files.")
    parser.add_argument('-t', '--tasks', type=int, default=16,
                        help="Number of cpus to use.")
    args = parser.parse_args()
    return args


line = """kneaddata --i {} --i {} --output {} --reference-db /fdb/kneaddata/Homo_sapiens_Bowtie2_v0.1/ -p {} -t {}\n"""


def find_and_zip_files(dir_fp: str, ext: str) -> List[Tuple[str, str]]:
    files = os.listdir(dir_fp)
    files = [f for f in files if f.endswith(f".{ext}")]
    files.sort()

    paired_files = []
    for i in range(0, len(files), 2):
        paired_files.append((abspath(os.path.join(dir_fp, files[i])), abspath(
            os.path.join(dir_fp, files[i+1]))))

    return paired_files


def main():
    args = parse_arguments()
    input_abs = abspath(args.input)
    output_abs = abspath(args.output)

    paired_files = find_and_zip_files(input_abs, args.extension)

    with open(os.path.join(output_abs, "submit_decontaminate.swarm"), "w") as f:
        f.write(
            f"#SWARM -t {args.tasks} -g 64 --time 04:00:00 --module kneaddata\n")

        for (r1, r2) in paired_files:
            formatted_line = line.format(
                r1, r2, output_abs, args.tasks, args.tasks*2)
            f.write(formatted_line)


if __name__ == '__main__':
    main()
