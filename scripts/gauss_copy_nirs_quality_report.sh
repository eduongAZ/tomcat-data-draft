#!/bin/bash

# Specify the path
path="/path/to/directory"

# Check if the path exists and is a directory
if [[ ! -d "$path" ]]; then
  echo "Invalid path or directory does not exist."
  exit 1
fi

# Retrieve a list of directory names
directories=("$path"/*)

# Iterate through the list and extract the folder names
for directory in "${directories[@]}"; do
  if [[ -d "$directory" ]]; then
    folder_name=$(basename "$directory")
    echo "$folder_name"
  fi
done
