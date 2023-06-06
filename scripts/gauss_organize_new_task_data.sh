#!/bin/bash

data_location="/space/calebshibu/Neurips_06_06_23_15"
original_data_location="/tomcat/data/raw/LangLab/experiments/study_3_pilot/group"
data_output_dir="/space/eduong/exp_tasks"

# More details on folders
source ../.env

echo "Organizing baseline tasks ..."

# Iterate through the list of folders
for folder in "${NEW_FOLDERS[@]}"; do
    # Get the new data
    source="$data_location/$folder/baseline_tasks/"
    destination="$data_output_dir/$folder/"

    mkdir -p "$destination"

    echo "Syncing $source to $destination"
    cp -r "$source"* "$destination"

    # Get task information from original location
    original_source="$original_data_location/$folder/baseline_tasks/"

    echo "Syncing $original_source to $destination"
    rsync -avm --include='*/' --include='metadata' "$original_source" "$dest"
done

echo "Organizing minecraft tasks ..."

# Iterate through the list of folders
for folder in "${NEW_FOLDERS[@]}"; do
    source="$original_data_location/$folder/minecraft/"
    destination="$data_output_dir/$folder/minecraft"

    mkdir -p "$destination"

    echo "Syncing $source to $destination"
    cp -r "$source"* "$destination"
done
