import json
import os
from typing import TextIO

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

    return output


def prepare_minecraft(path_to_task: str,
                      path_to_physio: str,
                      path_to_experiment_info: str,
                      experiment: str,
                      physio_type: str = "nirs",
                      output_file: TextIO | None = None) -> dict:
    output = {}

    # Identify the minecraft missions
    path_to_minecraft = os.path.join(path_to_task, experiment, 'minecraft')
    minecraft_missions = _identify_missions(path_to_minecraft)

    for mission, path_to_metadata in minecraft_missions.items():
        # Create the dictionary for the current mission
        mission_dict = {}

        # Add the info file
        mission_dict["info"] = os.path.join(path_to_experiment_info, f"{experiment}_info.json")
        if not check_file_exists(mission_dict["info"]):
            if output_file is not None:
                output_file.write("Cannot find " + mission_dict["info"] + "\n")
            else:
                print("Cannot find " + mission_dict["info"])
            continue

        # Add the path to the task metadata
        mission_dict["task_metadata_path"] = path_to_metadata
        if not check_file_exists(path_to_metadata):
            if output_file is not None:
                output_file.write("Cannot find " + mission_dict["task_metadata_path"] + "\n")
            else:
                print("Cannot find " + mission_dict["task_metadata_path"])
            continue

        # Add the physio data
        physio_data = {}
        for animal in ["lion", "tiger", "leopard"]:
            physio_file_path = os.path.join(path_to_physio, experiment,
                                            f"{animal}_{physio_type}_{mission}.csv")
            if not check_file_exists(physio_file_path):
                if output_file is not None:
                    output_file.write("Cannot find " + physio_file_path + "\n")
                else:
                    print("Cannot find " + physio_file_path)
                continue

            physio_data[animal] = physio_file_path

        mission_dict["physio_name_path"] = physio_data

        # Add the current mission to the output dictionary
        output[mission] = mission_dict

    return output
