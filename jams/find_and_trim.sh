# This script will take a file extension (i.e., fastq) and create a template metadata file.

input=$1
output=$2
file_ext=$3

find "$input" -name "*.$file_ext" > "$output/names.tmp"
echo -e "Sample\tVariable" > "$output/metadata.tsv"
awk '{split($0, array, "/"); split(array[2], new_array, "."); print new_array[1]}' names.tmp >> "$output/metadata.tsv"
rm "$output/names.tmp"
