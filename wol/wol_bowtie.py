import os
import argparse

# Parse the command line arguments
# We need one for input and one for output.
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, required=True)
parser.add_argument('-o', '--output', type=str, required=True)
parser.add_argument('-t', '--tasks', type=int, default=16)
args = parser.parse_args()

files = []
for file in os.listdir(args.input):
    if file.endswith(".fastq"):
        files.append(os.path.join(args.input, file))

files.sort()

# Make a list of tuples of the paired files.
paired_files = []
for i in range(0, len(files), 2):
    paired_files.append((files[i], files[i+1]))

# We need to make a bash script to run bowtie2 on all the files.
with open(os.path.join(args.output, "submit_bowtie.swarm"), "w") as f:
    # f.write("#!/bin/bash\n\n")
    # f.write("module load bowtie\n\n")
    f.write(f"#SWARM -t {args.tasks} -g 32 --time 08:00:00 --module bowtie\n")

    for pair in paired_files:
        prefix = pair[0].split("/")[-1].split("_")[0]
        line = """bowtie2 -p {} -x /data/TBHD_share/valencia/pipelines/woltka_db/databases/bowtie2/WoLr1 -1 {} -2 {} --very-sensitive --no-head --no-unal -k 16 --np 1 --mp "1,1" --rdg "0,1" --rfg "0,1" --score-min "L,0,-0.05" | cut -f1-9 | sed 's/$/\\t*\\t*/' | gzip > {}.sam.gz""".format(args.tasks, pair[0], pair[1], prefix)
        f.write(line + "\n")
