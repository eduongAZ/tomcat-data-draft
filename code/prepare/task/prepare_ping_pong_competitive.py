import glob
import json
import os
from io import StringIO

from .utils import check_file_exists


def prepare_ping_pong_competitive(task_data_path: str,
                                  physio_data_path: str,
                                  experiment_info_path: str,
                                  experiment: str,
                                  physio_type: str,
                                  synchronization_frequency: float,
                                  output_dir: str,
                                  interpolation_method: callable) -> tuple[dict[str, any], bool, str]:
    experiment_dict = {}

    experiment_info_file = os.path.join(experiment_info_path, experiment + "_info.json")
    if not check_file_exists(experiment_info_file):
        return {}, False, f"{experiment_info_file} does not exist\n"

    # Get participant id of each computer
    with open(experiment_info_file, 'r') as f:
        participant_ids = json.load(f)["participant_ids"]
    participant_ids['cheetah'] = 'exp'

    # getting all competitive task for the experiment
    matching_file_path = os.path.join(task_data_path, experiment, 'ping_pong', 'competitive_*.csv')
    competitive_tasks = glob.glob(matching_file_path)
    if not competitive_tasks:
        return {}, False, f"Cannot find files matching pattern {matching_file_path}\n"

    string_stream = StringIO()
    for task in competitive_tasks:
        # extracting match number
        match_num = task.split('/')[-1].split('_')[1]

        # get directory name from the csv file path
        directory = os.path.dirname(task)
        # pattern to match
        pattern = os.path.join(directory, f"competitive_{match_num}*.json")
        # Use glob to find files that match the pattern
        matching_files = glob.glob(pattern)
        matching_file = matching_files[0] if matching_files else None
        if matching_file is None:
            string_stream.write(f"Cannot find file matching pattern " + pattern + "\n")
            continue
        # Get match information
        with open(matching_file) as f:
            metadata = json.load(f)
        # Remove all other metadata fields except for left and right team
        metadata = {key: metadata[key] for key in ["left_team", "right_team"]}

        # Constructing paths to corresponding physio data files
        physio_paths = {}
        for team, task_participants_ids in metadata.items():
            for task_participant_id in task_participants_ids:
                if task_participant_id == 'exp':
                    continue
                elif task_participant_id not in participant_ids.values():
                    continue

                # finding the participant name for the id
                participant_name = \
                    [k for k, v in participant_ids.items() if v == task_participant_id][0]

                # finding the physio data file for the participant
                physio_file = os.path.join(
                    physio_data_path,
                    experiment,
                    participant_name + f'_{physio_type}_ping_pong_competetive_' + match_num + '.csv'
                )
                if not check_file_exists(physio_file):
                    string_stream.write(f"{physio_file} does not exist\n")
                    continue

                physio_paths[participant_name] = physio_file

        if not physio_paths:
            string_stream.write("No physio data found for match " + match_num + "\n")

        experiment_dict[match_num] = {
            "info": experiment_info_file,
            "task_csv_path": task,
            "physio_name_path": physio_paths,
            "teams": metadata,
            "frequency": synchronization_frequency,
            "output_dir": output_dir,
            "output_log_dir": os.path.join(output_dir, "report"),
            "interpolation_method": interpolation_method
        }

    string_stream.write("Ping pong competitive data prepared.\n")
    return experiment_dict, True, string_stream.getvalue()
