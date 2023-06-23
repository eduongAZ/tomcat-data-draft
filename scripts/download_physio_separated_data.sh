#!/bin/bash

# SSH connection details
remote_host="gauss"
data_location="/space/rchamplin/Neurips/rerun_filtered_2023_06_22"
data_output_dir="../data/raw/physio"

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
