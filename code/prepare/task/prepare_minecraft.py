import json
import os
from io import StringIO

from dateutil.parser import parse

from .utils import check_file_exists


def _metadata_message_generator(metadata_file_path: str):
    with open(metadata_file_path, 'r') as metadata_file:
        for line in metadata_file:
            yield json.loads(line)


def _get_mission_type(metadata_file_path: str) -> str:
    messages = _metadata_message_generator(metadata_file_path)

    trial_topic = "trial"

    # parse messages
    for message in messages:
        # Find trial message
        if "topic" in message and message["topic"] == trial_topic and message["msg"][
            "sub_type"] == "start":
            return message["data"]["experiment_mission"]

    return ""


def _get_trial_time(metadata_file_path: str) -> str:
    messages = _metadata_message_generator(metadata_file_path)

    trial_topic = "trial"

    # parse messages
    for message in messages:
        # Find trial message
        if "topic" in message and message["topic"] == trial_topic and message["msg"][
            "sub_type"] == "start":
            return message["header"]["timestamp"]

    return ""


def _is_hands_on_training(metadata_file_path: str) -> bool:
    mission_type = _get_mission_type(metadata_file_path)
    return mission_type == "Hands-on Training"


def _is_saturn_a(metadata_file_path: str) -> bool:
    mission_type = _get_mission_type(metadata_file_path)
    return mission_type == "Saturn_A"


def _is_saturn_b(metadata_file_path: str) -> bool:
    mission_type = _get_mission_type(metadata_file_path)
    return mission_type == "Saturn_B"


def _identify_missions(path_to_minecraft: str) -> dict[str, str]:
    output = {}
    saturn_a_start_time = None
    saturn_b_start_time = None
    training_start_time = None

    for mission in os.listdir(path_to_minecraft):
        if mission.endswith("metadata"):
            mission_path = os.path.join(path_to_minecraft, mission)
            if _is_saturn_a(mission_path):
                if saturn_a_start_time is None:
                    saturn_a_start_time = parse(_get_trial_time(mission_path))
                    output["saturn_a"] = mission_path
                else:
                    new_saturn_a_start_time = parse(_get_trial_time(mission_path))
                    if new_saturn_a_start_time > saturn_a_start_time:
                        saturn_a_start_time = new_saturn_a_start_time
                        output["saturn_a"] = mission_path
            elif _is_saturn_b(mission_path):
                if saturn_b_start_time is None:
                    saturn_b_start_time = parse(_get_trial_time(mission_path))
                    output["saturn_b"] = mission_path
                else:
                    new_saturn_b_start_time = parse(_get_trial_time(mission_path))
                    if new_saturn_b_start_time > saturn_b_start_time:
                        saturn_b_start_time = new_saturn_b_start_time
                        output["saturn_b"] = mission_path
            elif _is_hands_on_training(mission_path):
                if training_start_time is None:
                    training_start_time = parse(_get_trial_time(mission_path))
                    output["hands_on_training"] = mission_path
                else:
                    new_training_start_time = parse(_get_trial_time(mission_path))
                    if new_training_start_time > training_start_time:
                        training_start_time = new_training_start_time
                        output["hands_on_training"] = mission_path

    return output


def prepare_minecraft(task_data_path: str,
                      physio_data_path: str,
                      experiment_info_path: str,
                      experiment: str,
                      physio_type: str,
                      synchronization_frequency: float,
                      output_dir: str,
                      interpolation_method: callable) -> tuple[dict[str, any], bool, str]:
    output = {}
    string_stream = StringIO()

    # Get the path to the experiment info
    experiment_info_file = os.path.join(experiment_info_path, f"{experiment}_info.json")
    if not check_file_exists(experiment_info_file):
        return {}, False, f"{experiment_info_file} does not exist\n"

    # Identify the minecraft missions
    path_to_minecraft = os.path.join(task_data_path, experiment, 'minecraft')
    minecraft_missions = _identify_missions(path_to_minecraft)

    if not minecraft_missions:
        return {}, False, f"Cannot find minecraft missions for {experiment}\n"

    if "saturn_a" not in minecraft_missions:
        string_stream.write(f"Cannot find Saturn A mission for {experiment}\n")

    if "saturn_b" not in minecraft_missions:
        string_stream.write(f"Cannot find Saturn B mission for {experiment}\n")

    if "hands_on_training" not in minecraft_missions:
        string_stream.write(f"Cannot find Hands-on Training mission for {experiment}\n")

    for mission, path_to_metadata in minecraft_missions.items():
        # Get physio data files
        physio_data = {}
        for animal in ["lion", "tiger", "leopard"]:
            physio_file_path = os.path.join(physio_data_path, experiment,
                                            f"{animal}_{physio_type}_{mission}.csv")
            if not check_file_exists(physio_file_path):
                string_stream.write(f"Cannot find {physio_file_path}\n")
                continue

            physio_data[animal] = physio_file_path

        if not physio_data:
            string_stream.write(f"Cannot find physio data for {mission}\n")
            continue

        mission_dict = {
            "info": experiment_info_file,
            "task_metadata_path": path_to_metadata,
            "physio_name_path": physio_data,
            "frequency": synchronization_frequency,
            "output_dir": output_dir,
            "output_log_dir": os.path.join(output_dir, "report"),
            "interpolation_method": interpolation_method
        }

        # Add the current mission to the output dictionary
        output[mission] = mission_dict

    string_stream.write("Minecraft missions prepared.\n")
    return output, True, string_stream.getvalue()
