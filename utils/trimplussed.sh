for f in *.fastq
do
	echo $f
	bn=$(basename "$f" .fastq)
	echo $bn
	new_name="${bn}_plus_removed.fastq"
	echo $new_name
	parent_dir="$(dirname $f)"
	echo $parent_dir
	new_fp="$parent_dir/$new_name"
	echo $new_fp
	sed 's/^\+.*/+/' > "$new_fp"
done
