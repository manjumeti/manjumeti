#!/bin/bash

# Source file to copy
SOURCE_FILE="Configurations-Base.zip"

# Destination path on remote servers
DEST_PATH="/tmp"

# Remote user
USER="sccStudent"

# List of servers
SERVERS=(
    "xxx.xxx.xxx.xxx"  # Server 1
)

# Copy file to each server
for SERVER in "${SERVERS[@]}"
do
    echo "Copying file to $SERVER ..."
    
    scp "$SOURCE_FILE" "${USER}@${SERVER}:${DEST_PATH}"

    if [ $? -eq 0 ]; then
        echo "Successfully copied to $SERVER"
    else
        echo "Failed to copy to $SERVER"
    fi
done