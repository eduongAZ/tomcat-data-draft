#!/bin/bash

# SSH connection details
remote_host="gauss"
data_location="/tomcat/data/derived/drafts/draft_2023_06_05_11"
data_output_dir="../data/gauss_processed"

# More details on folders to sync and SSH conection
source ../.env

# Getting NIRS data

# Iterate through the list of folders
for folder in "${FOLDERS[@]}"; do
    source="$REMOTE_USER@$remote_host:$data_location/nirs/$folder/"
    destination="$data_output_dir/nirs/$folder"

    mkdir -p "$destination"

    echo "Syncing $source to $destination"
    rsync -avP "$source" "$destination"
done

# Getting EEG data

# Iterate through the list of folders
for folder in "${FOLDERS[@]}"; do
    source="$REMOTE_USER@$remote_host:$data_location/eeg/$folder/"
    destination="$data_output_dir/eeg/$folder"

    mkdir -p "$destination"

    echo "Syncing $source to $destination"
    rsync -avP "$source" "$destination"
done
