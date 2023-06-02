import glob
import json


def prepare_affective_task_individual(path_to_task: str,
                                      path_to_physio: str,
                                      path_to_experiment_info: str,
                                      experiment: str,
                                      physio_type: str = "nirs") -> dict:
    info_path = f"{path_to_experiment_info}/{experiment}_info.json"
    with open(info_path, 'r') as f:
        participant_info = json.load(f)["participant_ids"]

    output = {}
    for computer_name, participant_id in participant_info.items():
        # Search for CSV files starting with "individual_{participant_id}"
        csv_files = glob.glob(
            f"{path_to_task}/{experiment}/affective/individual_{participant_id}*.csv")

        # Get the first match
        task_csv_path = csv_files[0] if csv_files else None

        participant_dict = {
            "info": info_path,
            "participant_id": participant_id,
            "computer_name": computer_name,
            "task_csv_path": task_csv_path,
            "physio_csv_path": f"{path_to_physio}/{experiment}/{computer_name}_{physio_type}_affective_task_individual.csv"
        }
        output[computer_name] = participant_dict

    return output
