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

# Collect the folder names
folder_names=()
for directory in "${directories[@]}"; do
  if [[ -d "$directory" ]]; then
    folder_name=$(basename "$directory")
    folder_names+=("$folder_name")
  fi
done

# Print the folder names
for folder_name in "${folder_names[@]}"; do
  echo "$folder_name"
done
