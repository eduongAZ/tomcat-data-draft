import os


def prepare_affective_task_team(path_to_task: str,
                                path_to_physio: str,
                                path_to_experiment_info: str,
                                experiment: str,
                                physio_type: str = "nirs") -> dict:
    # Create a dictionary and add info path
    output = {'info': os.path.join(path_to_experiment_info, experiment + "_info.json")}

    # Add task csv path
    task_csv_path = os.path.join(path_to_task, experiment, 'affective')
    # List all files in the directory
    files_in_directory = os.listdir(task_csv_path)
    # Filter out directories, leave only files
    only_files = [f for f in files_in_directory if os.path.isfile(os.path.join(task_csv_path, f))]
    # Filter to select only files with 'team' in their names
    team_files = [f for f in only_files if 'team' in f and 'csv' in f]
    # Assume there's only one 'team' file in the directory
    task_csv_file = team_files[0]
    output['task_csv_path'] = os.path.join(task_csv_path, task_csv_file)

    # Add physio data paths
    physio_data_path = os.path.join(path_to_physio, experiment)
    physio_name_path = {}
    computer_names = ["lion", "tiger", "leopard"]
    for computer_name in computer_names:
        physio_file = f"{computer_name}_{physio_type}_affective_task_team.csv"
        physio_name_path[computer_name] = os.path.join(physio_data_path, physio_file)
    output['physio_name_path'] = physio_name_path

    return output
