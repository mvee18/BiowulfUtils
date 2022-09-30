#!/bin/bash

# Take the search text
read -p "Enter the search text:" search
# Take the replace text
read -p "Enter the replace text:" replace

# Rename all files that match with the pattern
echo $(rename "s/.$search/.$replace/" *)
echo "The files are renamed."
