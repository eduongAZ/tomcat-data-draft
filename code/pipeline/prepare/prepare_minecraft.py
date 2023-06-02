import json
import os


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


def _is_saturn_a(metadata_file_path: str) -> bool:
    mission_type = _get_mission_type(metadata_file_path)
    return mission_type == "Saturn_A"


def _is_saturn_b(metadata_file_path: str) -> bool:
    mission_type = _get_mission_type(metadata_file_path)
    return mission_type == "Saturn_B"


def _identify_missions(path_to_minecraft: str) -> dict[str, str]:
    output = {}
    for mission in os.listdir(path_to_minecraft):
        if mission.endswith("metadata"):
            mission_path = os.path.join(path_to_minecraft, mission)
            if _is_saturn_a(mission_path):
                output["saturn_a"] = mission_path
            elif _is_saturn_b(mission_path):
                output["saturn_b"] = mission_path

    return output


def prepare_minecraft(path_to_task: str,
                      path_to_physio: str,
                      path_to_experiment_info: str,
                      experiment: str,
                      physio_type: str = "nirs") -> dict:
    output = {}

    # Identify the minecraft missions
    path_to_minecraft = os.path.join(path_to_task, experiment, 'minecraft')
    minecraft_missions = _identify_missions(path_to_minecraft)

    for mission, path_to_metadata in minecraft_missions.items():
        # Create the dictionary for the current mission
        mission_dict = {}

        # Add the info file
        mission_dict["info"] = os.path.join(path_to_experiment_info, f"{experiment}_info.json")

        # Add the path to the task metadata
        mission_dict["task_metadata_path"] = path_to_metadata

        # Add the physio data
        physio_data = {}
        for animal in ["lion", "tiger", "leopard"]:
            physio_data[animal] = os.path.join(path_to_physio, experiment,
                                               f"{animal}_{physio_type}_{mission}.csv")
        mission_dict["physio_name_path"] = physio_data

        # Add the current mission to the output dictionary
        output[mission] = mission_dict

    return output
