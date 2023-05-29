#!/bin/bash

# SSH connection details
remote_host="gauss"
data_location="/space/calebshibu/Neurips_new"
data_output_dir="../data/raw/physio_data"

# More details on folders to sync and SSH conection
source ../.env

# File extension to filter
file_extension="_filtered.csv"

# Iterate through the list of folders
for folder in "${FOLDERS[@]}"; do
    source="$REMOTE_USER@$remote_host:$data_location/$folder"
    destination="$data_output_dir/$folder"

    mkdir -p "$destination"

    echo "Syncing $source to $destination"
    rsync -avP --include="*/" --include="*$file_extension" --exclude="*" "$source" "$destination"
done
