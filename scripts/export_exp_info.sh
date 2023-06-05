#!/bin/bash

# SSH connection details
remote_host="gauss"
data_location="/Users/ericduong/Documents/ToMCAT/tomcat-data-draft/data/organized/info/"
data_output_dir="/space/eduong/exp_info"

# More details on folders to sync and SSH conection
source ../.env

source="$data_location"
destination="$REMOTE_USER@$remote_host:$data_output_dir/$folder"

rsync -avP "$source" "$destination"
