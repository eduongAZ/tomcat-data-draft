import os
from typing import TextIO

from .utils import check_file_exists, FileDoesNotExistError


def prepare_affective_task_team(path_to_task: str,
                                path_to_physio: str,
                                path_to_experiment_info: str,
                                experiment: str,
                                physio_type: str = "nirs",
                                output_file: TextIO | None = None) -> dict:
    # Create a dictionary and add info path
    output = {'info': os.path.join(path_to_experiment_info, experiment + "_info.json")}
    if not check_file_exists(output['info']):
        raise FileDoesNotExistError(output['info'])

    # Add task csv path
    task_csv_path = os.path.join(path_to_task, experiment, 'affective')
    # List all files in the directory
    files_in_directory = os.listdir(task_csv_path)
    # Filter out directories, leave only files
    only_files = [f for f in files_in_directory if os.path.isfile(os.path.join(task_csv_path, f))]
    # Filter to select only files with 'team' in their names
    team_files = [f for f in only_files if 'team' in f and 'csv' in f]
    # Assume there's only one 'team' file in the directory
    task_csv_file = team_files[0] if team_files else None
    if task_csv_file is None:
        raise FileDoesNotExistError(task_csv_path)
    task_csv_file_path = os.path.join(task_csv_path, task_csv_file)
    if not check_file_exists(task_csv_file_path):
        raise FileDoesNotExistError(task_csv_file_path)
    output['task_csv_path'] = os.path.join(task_csv_path, task_csv_file)

    # Add physio data paths
    physio_data_path = os.path.join(path_to_physio, experiment)
    physio_names_paths = {}
    computer_names = ["lion", "tiger", "leopard"]
    for computer_name in computer_names:
        physio_file = f"{computer_name}_{physio_type}_affective_task_team.csv"
        physio_name_path = os.path.join(physio_data_path, physio_file)
        if not check_file_exists(physio_name_path):
            if output_file is not None:
                output_file.write(f"{physio_name_path} does not exist\n")
            else:
                print(f"{physio_name_path} does not exist")
            continue
        physio_names_paths[computer_name] = physio_name_path
    output['physio_name_path'] = physio_names_paths

    return output
