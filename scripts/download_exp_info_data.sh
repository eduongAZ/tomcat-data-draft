#!/bin/bash

# SSH connection details
remote_host="gauss"
data_location="/space/eduong/exp_info"
data_output_dir="../data/raw/info"

# More details on folders to sync and SSH conection
source ../.env

source="$REMOTE_USER@$remote_host:$data_location/"
destination="$data_output_dir/$folder"

mkdir -p "$destination"

echo "Syncing $source to $destination"
rsync -avP "$source" "$destination"
