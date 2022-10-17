inp=$1
out=$2

grep -E "(s__)|(taxonomy)" "$1"  > "$2"
