# Checks the directory for failed swarm jobs, then gets the lines from the JAMS.swarm file to make a resubmission script. 
# The new failed.swarm file will be placed in the same directory as the old swarm script.
input_dir=$(realpath $1)
swarm_file=$(realpath $2)
new_swarm=$(dirname $swarm_file)/failed.swarm

jams_success="Thank you for using JAMS. Use JAMSbeta to compare between JAMS samples."
echo $new_swarm

# Check if the new swarm file exists, if so, then delete is since we are going to use append in the loop.
remove_old() {
	if [ -f "$new_swarm" ] ; then
		echo "Removing old failed.swarm file..."
		rm "$new_swarm"
	fi
}

# Check the number of jobs that failed using grep and wc.
n_failed=$(grep -L "$jams_success" $input_dir/*.log | wc -l)
# echo "failed: $n_failed"
if [ "$n_failed" == "0" ]; then
	echo "Everything seems to have succeeded. Exiting..."
	exit 0 
fi

# Else, we generate the new swarm with failed files.
remove_old
grep -L "$jams_success" $input_dir/*.log | while read -r line ; do
	# Need to get sampleID from the filepath.
	id=$(basename $line | cut -f 1 -d "." | cut -f 1 -d "_")	
	echo "Writing: $id"
	grep "$id" $2 >> $new_swarm
done	

echo "Swarm file written to $new_swarm."
