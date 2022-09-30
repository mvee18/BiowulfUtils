input=$1
output=$2

find "$input" -name "*.jams" > "$output/names.tmp"
echo -e "Sample\tVariable" > "$output/metadata.tsv"
awk '{split($0, array, "/"); split(array[2], new_array, "."); print new_array[1]}' names.tmp >> "$output/metadata.tsv"
rm "$output/names.tmp"
