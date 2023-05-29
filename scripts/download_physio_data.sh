#!/bin/bash

# SSH connection details
remote_user="eduong"
remote_host="gauss"
data_location="/space/calebshibu/Neurips"
data_output_dir="../data/raw/physio_data"

# List of folders to sync
FOLDERS=(
  "exp_2022_10_14_10"
  "exp_2022_10_18_10"
)

# File extension to filter
file_extension="_filtered.csv"

# Iterate through the list of folders
for folder in "${FOLDERS[@]}"; do
    source="$remote_user@$remote_host:$data_location/$folder"
    destination="$data_output_dir/$folder"

    mkdir -p "$destination"

    echo "Syncing $source to $destination ..."
    rsync -avP --include="*/" --include="*$file_extension" --exclude="*" "$source" "$destination"
done
