#!/bin/bash

# Specify the path
path="/tomcat/data/derived/drafts/draft_2023_06_05_11/nirs"
nirs_report_src_dir="/space/calebshibu/Neurips_06_03_23_11"

# Check if the path exists and is a directory
if [[ ! -d "$path" ]]; then
    echo "Invalid path or directory does not exist."
    exit 1
fi

# Retrieve a list of directory names
directories=("$path"/*)

# Collect the folder names
folder_names=()
for directory in "${directories[@]}"; do
    if [[ -d "$directory" ]]; then
        folder_name=$(basename "$directory")
        folder_names+=("$folder_name")
    fi
done

# Print the folder names
for folder_name in "${folder_names[@]}"; do
    # For Lion
    lion_src_path="$nirs_report_src_dir/$folder_name/lion/NIRS_channel_quality.csv"
    lion_dst_path="$path/$folder_name/report/lion_NIRS_channel_quality.csv"

    # Make sure source file exists
    if [[ ! -f "$lion_src_path" ]]; then
        echo "Source file does not exist: $lion_src_path"
    else
        cp "$lion_src_path" "$lion_dst_path"
    fi

    # For Tiger
    tiger_src_path="$nirs_report_src_dir/$folder_name/tiger/NIRS_channel_quality.csv"
    tiger_dst_path="$path/$folder_name/report/tiger_NIRS_channel_quality.csv"

    # Make sure source file exists
    if [[ ! -f "$tiger_src_path" ]]; then
        echo "Source file does not exist: $tiger_src_path"
    else
        cp "$tiger_src_path" "$tiger_dst_path"
    fi

    # For Leopard
    leopard_src_path="$nirs_report_src_dir/$folder_name/leopard/NIRS_channel_quality.csv"
    leopard_dst_path="$path/$folder_name/report/leopard_NIRS_channel_quality.csv"

    # Make sure source file exists
    if [[ ! -f "$leopard_src_path" ]]; then
        echo "Source file does not exist: $leopard_src_path"
    else
        cp "$leopard_src_path" "$leopard_dst_path"
    fi
done
