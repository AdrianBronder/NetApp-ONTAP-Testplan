#!/bin/bash
################################################################################
#
# Title:        ONTAP-write_files-82.sh - Write Files
# Author:       NetApp Inc. (badrian)
# Initial 
# Create Date:  2025-08-04
# Description:  Global Namespace
#               - Helper script to create test files in exports/shares
# 
################################################################################

if [[ "$#" -ne 2 ]]; then
    echo "Usage: $0 <target path> <file count>"
    exit 1
elif ! [[ -d $1 ]]; then
    echo "$1 does not exist"
    exit 1
elif ! [[ $2 =~ ^[0-9]+$ ]]; then
    echo "Integer must be provided for file count. Got: $2"
    exit 1
fi

# Directory where the files will be created
target_path=$1

# Number of files to create
file_count=$2

# Size of each file in bytes (e.g., 1024 bytes = 1KB)
file_size=1048576

for i in $(seq 1 $file_count); do
    # Generate a random file name
    file_name=$(printf "gnsdata%06d.txt" "$i")
    # Create a file with random content and specified size
    head -c $file_size /dev/urandom > "$target_path/$file_name"
#    sleep 1
done

echo "Done creating $file_count files in $target_path."