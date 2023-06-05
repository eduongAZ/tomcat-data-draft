#!/bin/bash

data_location="/tomcat/data/raw/LangLab/experiments/study_3_pilot/group"
data_output_dir="/space/eduong/exp_tasks"

# More details on folders
source ../.env

echo "Organizing baseline tasks ..."

# Iterate through the list of folders
for folder in "${FOLDERS[@]}"; do
    source="$data_location/$folder/baseline_tasks/"
    destination="$data_output_dir/$folder/"

    mkdir -p "$destination"

    echo "Syncing $source to $destination"
    cp -r "$source"* "$destination"
done

echo "Organizing minecraft tasks ..."

# Iterate through the list of folders
for folder in "${FOLDERS[@]}"; do
    source="$data_location/$folder/minecraft/"
    destination="$data_output_dir/$folder/minecraft"

    mkdir -p "$destination"

    echo "Syncing $source to $destination"
    cp -r "$source" "$destination"
done
