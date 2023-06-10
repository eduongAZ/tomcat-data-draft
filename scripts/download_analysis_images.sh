#!/bin/bash

# SSH connection details
remote_host="gauss"
data_location="/work/eduong/Projects/tomcat-data-draft/code/code_outputs"
data_output_dir="../data/plotted_images/"

# More details on folders to sync and SSH conection
source ../.env

source="$REMOTE_USER@$remote_host:$data_location/"
destination="$data_output_dir"

mkdir -p "$destination"

echo "Syncing $source to $destination"
rsync -avP "$source" "$destination"
