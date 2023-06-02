import glob
import json
import os

from .utils import check_file_exists, FileDoesNotExistError


def prepare_ping_pong_competitive(path_to_task: str,
                                  path_to_physio: str,
                                  path_to_experiment_info: str,
                                  experiment: str,
                                  physio_type: str = "nirs") -> dict:
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
    competitive_tasks = glob.glob(
        os.path.join(path_to_task, experiment, 'ping_pong', 'competitive_*.csv'))

    for task in competitive_tasks:
        if not check_file_exists(task):
            print("Cannot find " + task)
            continue

        # extracting match number
        match_num = task.split('/')[-1].split('_')[1]

        # getting corresponding metadata
        with open(task.replace('.csv', '_metadata.json')) as f:
            metadata = json.load(f)

        metadata = {key: metadata[key] for key in ["left_team", "right_team"]}

        # constructing paths to corresponding physio data files
        physio_paths = {}
        for team, ids in metadata.items():
            for participant_id in ids:
                if participant_id == 'exp':
                    continue

                # finding the participant name for the id
                participant_name = [k for k, v in participant_ids.items() if v == participant_id][0]

                # finding the physio data file for the participant
                matching_physio_path = os.path.join(
                    path_to_physio,
                    experiment,
                    participant_name + f'_{physio_type}_ping_pong_competetive_' + match_num + '.csv'
                )
                matching_physio_files = glob.glob(matching_physio_path)
                if len(matching_physio_files) == 0:
                    print("Cannot find " + matching_physio_path)
                    continue
                physio_file = matching_physio_files[0]
                if not check_file_exists(physio_file):
                    print("Cannot find " + physio_file)
                    continue

                physio_paths[participant_name] = physio_file

        if not physio_paths:
            print("No physio data found for " + match_num)

        experiment_dict[match_num] = {
            "info": info_path,
            "task_csv_path": task,
            "physio_name_path": physio_paths,
            "teams": metadata
        }

    return experiment_dict
