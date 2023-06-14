import glob
import os
from io import StringIO

from common import read_json_file
from .utils import check_file_exists


def prepare_affective_individual(task_data_path: str,
                                 physio_data_path: str,
                                 experiment_info_path: str,
                                 experiment: str,
                                 physio_type_data: dict[str, dict[str, any]],
                                 synchronization_frequency: float,
                                 output_dir: str,
                                 downsample_frequency: float | None = None) -> tuple[dict[str, any], bool, str]:
    output = {}

    experiment_info_file = os.path.join(experiment_info_path, experiment + "_info.json")
    if not check_file_exists(experiment_info_file):
        return {}, False, f"{experiment_info_file} does not exist.\n"

    participant_info = read_json_file(experiment_info_file)["participant_ids"]

    string_stream = StringIO()
    for computer_name, participant_id in participant_info.items():
        # Search for CSV files starting with "individual_{participant_id}"
        csv_file_matching_pattern = f"{task_data_path}/{experiment}/affective/individual_{participant_id}*.csv"
        csv_files = glob.glob(csv_file_matching_pattern)

        # Get the first match
        task_csv_path = csv_files[0] if csv_files else None
        if task_csv_path is None or not check_file_exists(task_csv_path):
            string_stream.write(f"Cannot find file matching pattern " + csv_file_matching_pattern + "\n")
            continue

        physio_information = {}
        for physio_type, physio_type_info in physio_type_data.items():
            physio_csv_path = os.path.join(physio_data_path,
                                           experiment,
                                           f"{computer_name}_{physio_type}_affective_task_individual.csv")
            if not check_file_exists(physio_csv_path):
                string_stream.write(f"Cannot find {physio_csv_path} for {computer_name}\n")
                continue

            physio_information[physio_type] = {
                "name_path": {computer_name: physio_csv_path},
            }
            physio_information[physio_type].update(physio_type_info)

        if not physio_information:
            string_stream.write(f"Cannot find any physio data for {computer_name}\n")

        participant_dict = {
            "info": experiment_info_file,
            "participant_id": participant_id,
            "computer_name": computer_name,
            "task_csv_path": task_csv_path,
            "physio": physio_information,
            "frequency": synchronization_frequency,
            "downsample_frequency": downsample_frequency,
            "output_dir": output_dir,
            "output_log_dir": os.path.join(output_dir, "report")
        }

        output[f"affective_individual_{computer_name}"] = participant_dict

    string_stream.write("Affective individual data prepared.\n")
    return output, True, string_stream.getvalue()
