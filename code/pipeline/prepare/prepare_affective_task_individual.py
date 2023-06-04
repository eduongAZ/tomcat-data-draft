import glob
import json
from typing import TextIO

from .utils import check_file_exists, FileDoesNotExistError


def prepare_affective_task_individual(path_to_task: str,
                                      path_to_physio: str,
                                      path_to_experiment_info: str,
                                      experiment: str,
                                      physio_type: str = "nirs",
                                      output_file: TextIO | None = None) -> dict:
    info_path = f"{path_to_experiment_info}/{experiment}_info.json"
    if not check_file_exists(info_path):
        raise FileDoesNotExistError(info_path)

    with open(info_path, 'r') as f:
        participant_info = json.load(f)["participant_ids"]

    output = {}
    for computer_name, participant_id in participant_info.items():
        # Search for CSV files starting with "individual_{participant_id}"
        csv_file_matching_pattern = f"{path_to_task}/{experiment}/affective/individual_{participant_id}*.csv"
        csv_files = glob.glob(csv_file_matching_pattern)

        # Get the first match
        task_csv_path = csv_files[0] if csv_files else None
        if task_csv_path is None or not check_file_exists(task_csv_path):
            if output_file:
                output_file.write(
                    "Cannot find file matching pattern " + csv_file_matching_pattern + "\n")
            else:
                print("Cannot find file matching pattern " + csv_file_matching_pattern)
            continue

        participant_dict = {
            "info": info_path,
            "participant_id": participant_id,
            "computer_name": computer_name,
            "task_csv_path": task_csv_path,
            "physio_csv_path": f"{path_to_physio}/{experiment}/{computer_name}_{physio_type}_affective_task_individual.csv"
        }
        if not check_file_exists(participant_dict["physio_csv_path"]):
            if output_file:
                output_file.write("Cannot find " + participant_dict["physio_csv_path"] + "\n")
            else:
                print("Cannot find " + participant_dict["physio_csv_path"])
            continue

        output[computer_name] = participant_dict

    return output
