#!/bin/bash

# SSH connection details
remote_user="eduong"
remote_host="gauss"
data_location="/tomcat/data/raw/LangLab/experiments/study_3_pilot/group"
data_output_dir="../data/raw/tasks"

# List of folders to sync
source ../.env

# Iterate through the list of folders
for folder in "${FOLDERS[@]}"; do
    source="$remote_user@$remote_host:$data_location/$folder/baseline_tasks/"
    destination="$data_output_dir/$folder"

    mkdir -p "$destination"

    echo "Syncing $source to $destination"
    rsync -avP "$source" "$destination"
done
