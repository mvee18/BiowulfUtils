import argparse
import os
from os.path import abspath, basename
from typing import List, Tuple


def pair_files(args) -> List[Tuple[str, str]]:
    """Find and pair the paired-end reads."""
    print("Input dir: ", args.input)
    paired_files = []
    files = os.listdir(args.input)
    files = [abspath(os.path.join(args.input, file))
             for file in files if file.endswith(args.extension)]
    files.sort()

    print(files)
    # Group every adjacent pair of files
    for i in range(0, len(files), 2):
        paired_files.append((files[i], files[i+1]))

    return paired_files


def make_output_dirs(args) -> Tuple[str, str]:
    k2_output = abspath(os.path.join(args.output, 'k2_outputs'))
    k2_reports = abspath(os.path.join(args.output, 'k2_reports'))

    if not os.path.exists(k2_output):
        os.makedirs(k2_output)

    if not os.path.exists(k2_reports):
        os.makedirs(k2_reports)

    return k2_output, k2_reports


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="Input directory with reads.", type=str, required=True)
    parser.add_argument(
        '-o', '--output', help="Output directory for swarm file.", type=str, required=True)
    parser.add_argument('-e', '--extension', type=str, help="Extension (fastq, fastq.gz, etc.)",
                        default='fastq')
    parser.add_argument('-d', '--database', type=str, help="Path to database.",
                        default="$KRAKEN_DB/standard")
    parser.add_argument('-t', '--threads', type=int,
                        help="Number of threads.", default=32)
    args = parser.parse_args()

    output_path = abspath(os.path.join(args.output, 'kraken.swarm'))
    output_submit = abspath(os.path.join(args.output, 'submit_kraken.sh'))

    k2_output, k2_reports = make_output_dirs(args)

    with open(output_path, 'w') as out:
        for f1, r1 in pair_files(args):
            print(basename(f1), basename(r1))

            f1_base = basename(f1).split('.')[0]

            print(k2_output, k2_reports)
            output_joined = os.path.join(k2_output, f1_base + '_output.txt')
            report_joined = os.path.join(k2_reports, f1_base + '_report.txt')

            out.write(f"kraken2 --db \"{args.database}\" "
                      "--confidence 0.1 "
                      f"--threads {args.threads} "
                      "--use-names "
                      f"--output {output_joined} "
                      f"--report {report_joined} "
                      f"--paired {f1} {r1}")

    with open(output_submit, 'w') as out:
        out.write(
            f"swarm -f {output_path} -g 256 -t {args.threads} --time 16:00:00 --module kraken")

    os.chmod(output_submit, 0o744)
