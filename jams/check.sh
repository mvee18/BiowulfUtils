# Checks the directory for failed swarm jobs, then gets the lines from the JAMS.swarm file to make a resubmission script. 
# The new failed.swarm file will be placed in the same directory as the old swarm script.

Help()
{
   # Display Help
   echo "Generates a new swarm file from failed JAMS jobs"
   echo
   echo "Syntax: check.sh -i [input_dir] -s [swarm_file]"
   echo "options:"
   echo "h     Print this Help."
   echo "i     The input directory with the JAMS logs."
   echo "s     The JAMS.swarm file containing the jobs."
   echo
}

while getopts ":h:i:s:" option; do
   case $option in
      h) # display Help
         Help
         exit;;
      i) # Input Directory
	 input_dir=$(realpath $OPTARG);;
	 # input_dir=$OPTARG;;
      s) # Original SWARM file
	 swarm_file=$(realpath $OPTARG);;
	 # swarm_file=$OPTARG;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done

# Test that both the i and s options were passed.
if [ -z "$input_dir" ]
then
   Help
   exit
fi

if [ -z "$swarm_file" ]
then
   Help
   exit
fi

new_swarm=$(dirname $swarm_file)/failed.swarm
jams_success="Thank you for using JAMS. Use JAMSbeta to compare between JAMS samples."
# echo $new_swarm

# Check if the new swarm file exists, if so, then delete is since we are going to use append in the loop.
remove_old() {
	if [ -f "$new_swarm" ] ; then
		echo "Removing old failed.swarm file..."
		rm "$new_swarm"
	fi
}

# Make sure there are log files in the directory...
if [ "$(ls -A $input_dir/*.log)" ]; then
   echo "Found log files in $input_dir"
else
   echo "No log files found in $input_dir. Exiting..."
   exit 0
fi

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
	grep "$id" $swarm_file >> $new_swarm
done	

echo "Swarm file written to $new_swarm."
