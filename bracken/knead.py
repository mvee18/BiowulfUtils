import argparse
import os
from typing import List, Tuple


def pair_files(args) -> List[Tuple[str, str]]:
    """Find and pair the paired-end reads."""
    print("Input dir: ", args.input)
    paired_files = []
    files = os.listdir(args.input)
    files = [os.path.abspath(os.path.join(args.input, file))
             for file in files if file.endswith(args.extension)]
    files.sort()

    print(files)

    # Group every adjacent pair of files
    for i in range(0, len(files), 2):
        paired_files.append((files[i], files[i+1]))

    return paired_files


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="Input directory with reads.", type=str, required=True)
    parser.add_argument(
        '-o', '--output', help="Output directory for swarm file.", type=str, required=True)
    parser.add_argument('-e', '--extension', type=str, help="Extension (fastq, fastq.gz, etc.)",
                        default='fastq')
    parser.add_argument('-d', '--database', type=str, help="Path to database.",
                        default="$KNEADDATA_DB/Homo_sapiens_Bowtie2_v0.1/Homo_sapiens")
    parser.add_argument('-t', '--threads', type=int,
                        help="Number of threads.", default=16)
    args = parser.parse_args()

    files = pair_files(args)

    # New swarm file.
    output_path = os.path.abspath(os.path.join(args.output, 'kneaddata.swarm'))
    output_submit = os.path.abspath(
        os.path.join(args.output, 'kneaddata_submit.sh'))

    with open(output_path, 'w') as out:
        for f1, r1 in files:
            out.write(f"kneaddata --i {f1} --i {r1} --output {os.path.abspath(args.output)} --reference-db {args.database} --remove-intermediate-output -t 8 -p 2 --trimmomatic-options \"SLIDINGWINDOW:4:20\" --trimmomatic-options \"MINLEN:90\"")

    with open(output_submit, 'w') as out:
        out.write(
            f"swarm -f {output_path} -g 128 -t {args.threads} --time 16:00:00 --module kneaddata")

    # Change permissions to 644.
    os.chmod(output_submit, 0o744)
