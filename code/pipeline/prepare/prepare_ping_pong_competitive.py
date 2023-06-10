import glob
import json
import os
from typing import TextIO

from .utils import check_file_exists, FileDoesNotExistError


def prepare_ping_pong_competitive(path_to_task: str,
                                  path_to_physio: str,
                                  path_to_experiment_info: str,
                                  experiment: str,
                                  physio_type: str = "nirs",
                                  output_file: TextIO | None = None) -> dict:
    experiment_dict = {}

    info_path = os.path.join(path_to_experiment_info, experiment + '_info.json')
    if not check_file_exists(info_path):
        raise FileDoesNotExistError(info_path)

    # loading participant ids from the experiment info json
    with open(info_path) as f:
        experiment_info = json.load(f)

    participant_ids = experiment_info['participant_ids']
    participant_ids['cheetah'] = 'exp'

    # getting all competitive tasks for the experiment
    matching_file_path = os.path.join(path_to_task, experiment, 'ping_pong', 'competitive_*.csv')
    competitive_tasks = glob.glob(matching_file_path)
    if not competitive_tasks:
        raise FileDoesNotExistError(matching_file_path)

    for task in competitive_tasks:
        # TODO: this might be unnecessary - competitive_tasks should be empty if no valid files
        if not check_file_exists(task):
            if output_file:
                output_file.write("Cannot find " + task + "\n")
            else:
                print("Cannot find " + task)
            continue

        # extracting match number
        match_num = task.split('/')[-1].split('_')[1]

        # get directory name from the csv file path
        directory = os.path.dirname(task)
        # pattern to match
        pattern = os.path.join(directory, f"competitive_{match_num}*.json")
        # Use glob to find files that match the pattern
        matching_file = glob.glob(pattern)[0]
        with open(matching_file) as f:
            metadata = json.load(f)

        # Remove all other metadata fields except for left and right team
        metadata = {key: metadata[key] for key in ["left_team", "right_team"]}

        # constructing paths to corresponding physio data files
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
                matching_physio_path = os.path.join(
                    path_to_physio,
                    experiment,
                    participant_name + f'_{physio_type}_ping_pong_competetive_' + match_num + '.csv'
                )
                matching_physio_files = glob.glob(matching_physio_path)
                if len(matching_physio_files) == 0:
                    if output_file:
                        output_file.write("Cannot find " + matching_physio_path + "\n")
                    else:
                        print("Cannot find " + matching_physio_path)
                    continue
                physio_file = matching_physio_files[0]
                if not check_file_exists(physio_file):
                    if output_file:
                        output_file.write("Cannot find " + physio_file + "\n")
                    else:
                        print("Cannot find " + physio_file)
                    continue

                physio_paths[participant_name] = physio_file

        if not physio_paths:
            if output_file:
                output_file.write("No physio data found for match " + match_num + "\n")
            else:
                print("No physio data found for match " + match_num)

        experiment_dict[match_num] = {
            "info": info_path,
            "task_csv_path": task,
            "physio_name_path": physio_paths,
            "teams": metadata
        }

    return experiment_dict
