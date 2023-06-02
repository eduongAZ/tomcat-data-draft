import os

from .utils import check_file_exists, FileDoesNotExistError


def prepare_ping_pong_cooperative(path_to_task: str,
                                  path_to_physio: str,
                                  path_to_experiment_info: str,
                                  experiment: str,
                                  physio_type: str = "nirs") -> dict:
    # Create a dictionary and add info path
    output = {'info': os.path.join(path_to_experiment_info, experiment + "_info.json")}
    if not check_file_exists(output['info']):
        raise FileDoesNotExistError(output['info'])

    # Add task csv path
    task_csv_path = os.path.join(path_to_task, experiment, 'ping_pong')
    # List all files in the directory
    files_in_directory = os.listdir(task_csv_path)
    # Filter out directories, leave only files
    only_files = [f for f in files_in_directory if os.path.isfile(os.path.join(task_csv_path, f))]
    # Find the file that contains the word "cooperative"
    cooperative_files = [f for f in only_files if "cooperative" in f]
    # We assume there's only one file in the directory
    task_csv_file = cooperative_files[0]
    output['task_csv_path'] = os.path.join(task_csv_path, task_csv_file)
    if not check_file_exists(output['task_csv_path']):
        raise FileDoesNotExistError(output['task_csv_path'])

    # Add physio data paths
    physio_data_path = os.path.join(path_to_physio, experiment)
    physio_name_path = {}
    computer_names = ["lion", "tiger", "leopard"]
    for computer_name in computer_names:
        physio_file = f"{computer_name}_{physio_type}_ping_pong_cooperative_0.csv"
        physio_name_path[computer_name] = os.path.join(physio_data_path, physio_file)
        if not check_file_exists(physio_name_path[computer_name]):
            raise FileDoesNotExistError(physio_name_path[computer_name])
    output['physio_name_path'] = physio_name_path

    return output
