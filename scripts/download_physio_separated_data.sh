#!/bin/bash

# SSH connection details
remote_host="gauss"
data_location="/space/rchamplin/Neurips/new_pipeline_2023_06_05"
data_output_dir="../data/raw/physio/nirs"

# More details on folders to sync and SSH conection
source ../.env

# Iterate through the list of folders
for folder in "${FOLDERS[@]}"; do
    source="$REMOTE_USER@$remote_host:$data_location/$folder/"
    destination="$data_output_dir/$folder"

    mkdir -p "$destination"

    echo "Syncing $source to $destination"
    rsync -avP --include="*_nirs_*" --exclude="*" "$source" "$destination"
done
