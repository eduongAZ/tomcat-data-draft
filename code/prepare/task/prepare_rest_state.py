import os
from io import StringIO

from .utils import check_file_exists


def prepare_rest_state(task_data_path: str,
                       physio_data_path: str,
                       experiment_info_path: str,
                       experiment: str,
                       physio_type_data: dict[str, dict[str, any]],
                       synchronization_frequency: float,
                       output_dir: str) -> tuple[dict[str, any], bool, str]:
    output = {}
    string_stream = StringIO()

    # Create a dictionary and add info path
    experiment_info_file = os.path.join(experiment_info_path, experiment + "_info.json")
    if not check_file_exists(experiment_info_file):
        return {}, False, f"{experiment_info_file} does not exist\n"
    output['info'] = experiment_info_file

    # Add task csv path
    task_csv_path = os.path.join(task_data_path, experiment, 'rest_state')
    # List all files in the directory
    files_in_directory = os.listdir(task_csv_path)
    # Filter out directories, leave only files
    only_files = [f for f in files_in_directory if os.path.isfile(os.path.join(task_csv_path, f))]
    # We assume there's only one file in the directory
    task_csv_file = only_files[0] if only_files else None
    if task_csv_file is None:
        return {}, False, f"No task csv file found in {task_csv_path}\n"
    task_csv_file_path = os.path.join(task_csv_path, task_csv_file)
    if not check_file_exists(task_csv_file_path):
        return {}, False, f"{task_csv_file_path} does not exist\n"
    output['task_csv_path'] = task_csv_file_path

    # Add physio data paths
    physio_information = {}
    for physio_type, physio_type_info in physio_type_data.items():
        physio_data_exp_dir = os.path.join(physio_data_path, physio_type, experiment)
        physio_names_paths = {}

        # For each computer
        computer_names = ["lion", "tiger", "leopard"]
        for computer_name in computer_names:
            # Get physio file for that computer
            physio_file = f"{computer_name}_{physio_type}_rest_state.csv"
            physio_name_path = os.path.join(physio_data_exp_dir, physio_file)
            if not check_file_exists(physio_name_path):
                string_stream.write(f"{physio_name_path} does not exist\n")
                continue
            physio_names_paths[computer_name] = physio_name_path

        # If no physio data found, move to another physio type
        if not physio_names_paths:
            string_stream.write(f"No physio data found for {physio_type}\n")
            continue

        if physio_type not in physio_information:
            physio_information[physio_type] = {}

        physio_information[physio_type]['name_path'] = physio_names_paths
        physio_information[physio_type].update(physio_type_info)

    if not physio_information:
        string_stream.write("No physio data found\n")

    output['physio'] = physio_information

    # Add synchronization frequency
    output['frequency'] = synchronization_frequency

    # Add output directory
    output['output_dir'] = output_dir

    # Add output log path
    output_log_dir = os.path.join(output_dir, "report")
    output['output_log_dir'] = output_log_dir

    string_stream.write("Rest state data prepared.\n")
    return output, True, string_stream.getvalue()
