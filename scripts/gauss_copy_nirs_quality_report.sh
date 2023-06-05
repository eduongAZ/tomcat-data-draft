#!/bin/bash

# Specify the path
path="/tomcat/data/derived/drafts/draft_2023_06_05_11/nirs"

# Check if the path exists and is a directory
if [[ ! -d "$path" ]]; then
  echo "Invalid path or directory does not exist."
  exit 1
fi

# Retrieve a list of directory names
directories=("$path"/*)

# Iterate through the list and print each directory name
for directory in "${directories[@]}"; do
  if [[ -d "$directory" ]]; then
    echo "$directory"
  fi
done
