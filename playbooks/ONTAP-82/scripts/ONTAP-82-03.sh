#!/bin/bash
################################################################################
#
# Title:        ONTAP-82-03.sh - Mount & Write
# Author:       NetApp Inc. (badrian)
# Initial 
# Create Date:  2024-11-04
# Description:  Anti-Ransomware
#               - Helper script to create test files in exports/shares
# 
################################################################################

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <target path> <file count>"
    exit 1
elif [ -d $1 ]; then
    echo "$1 does exist."
    exit 1
elif ! [ $2 =~ ^[0-9]+$ ]
    echo "Integer must be provided for file count. Got: $2"
    exit 1
fi

# Directory where the files will be created
target_path=$1

# Number of files to create
file_count=$2

# Size of each file in bytes (e.g., 1024 bytes = 1KB)
file_size=1024

for i in $(seq 1 $file_count); do
    # Generate a random file name
    file_name=$(printf "simdata%06d.txt" "$i")

    # Create a file with random content and specified size
    head -c $file_size /dev/urandom > "$target_path/$file_name"
done

echo "Done creating $file_count files in $target_path."