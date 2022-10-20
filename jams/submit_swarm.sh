inp=$1

swarm -g 246 -t 56 --time=24:00:00 --module R,samtools --partition=norm,ccr --gres=lscratch:400 -f "$1"
