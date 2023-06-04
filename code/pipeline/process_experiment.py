import multiprocessing
import os

from tqdm import tqdm

from tasks import RestState, FingerTapping, AffectiveTaskIndividual, AffectiveTaskTeam, \
    PingPongCompetitive, PingPongCooperative, Minecraft
from .prepare import prepare_rest_state, prepare_finger_tapping, prepare_affective_task_individual, \
    prepare_affective_task_team, prepare_ping_pong_competitive, prepare_ping_pong_cooperative, \
    prepare_minecraft, FileDoesNotExistError


def _process_rest_state(path_to_task: str,
                        path_to_physio: str,
                        path_to_experiment_info: str,
                        experiment: str,
                        physio_type: str,
                        output_path: str,
                        frequency: float):
    os.makedirs(os.path.join(output_path, experiment, 'report'), exist_ok=True)
    log_file_path = os.path.join(output_path, experiment, 'report', 'rest_state.txt')
    log_file = open(log_file_path, "w")

    log_file.write(f"# Experiment: {experiment}\n\nOutput of the program:\n\n```\n")
    log_file.write("==Rest state==\n")

    try:
        rest_state_data = prepare_rest_state(
            path_to_task=path_to_task,
            path_to_physio=path_to_physio,
            path_to_experiment_info=path_to_experiment_info,
            experiment=experiment,
            physio_type=physio_type,
            output_file=log_file
        )

        rest_state = RestState.from_files(
            rest_state_data['info'],
            rest_state_data['task_csv_path'],
            rest_state_data['physio_name_path'],
            frequency=frequency
        )

        rest_state.write_physio_data_csv(output_path + '/' + experiment)
    except FileDoesNotExistError as e:
        log_file.write(str(e) + '\n')

    log_file.write('```\n')
    log_file.close()


def _process_finger_tapping(path_to_task: str,
                            path_to_physio: str,
                            path_to_experiment_info: str,
                            experiment: str,
                            physio_type: str,
                            output_path: str,
                            frequency: float):
    os.makedirs(os.path.join(output_path, experiment, 'report'), exist_ok=True)
    log_file_path = os.path.join(output_path, experiment, 'report', 'finger_tapping.txt')
    log_file = open(log_file_path, "w")

    log_file.write(f"# Experiment: {experiment}\n\nOutput of the program:\n\n```\n")
    log_file.write("==Finger tapping==\n")

    try:
        finger_tapping_data = prepare_finger_tapping(
            path_to_task=path_to_task,
            path_to_physio=path_to_physio,
            path_to_experiment_info=path_to_experiment_info,
            experiment=experiment,
            physio_type=physio_type,
            output_file=log_file
        )

        finger_tapping = FingerTapping.from_files(
            finger_tapping_data['info'],
            finger_tapping_data['task_csv_path'],
            finger_tapping_data['physio_name_path'],
            frequency=frequency
        )

        finger_tapping.write_physio_data_csv(output_path + '/' + experiment)
    except FileDoesNotExistError as e:
        log_file.write(str(e) + '\n')

    log_file.write('```\n')
    log_file.close()


def _process_affective_individual_per_computer(experiment_id: str,
                                               participant_id: str,
                                               participant_name: str,
                                               task_csv_path: str,
                                               physio_csv_path: str,
                                               frequency: float,
                                               output_location: str):
    affective_individual = AffectiveTaskIndividual.from_files(
        experiment_id,
        participant_id,
        participant_name,
        task_csv_path,
        physio_csv_path,
        frequency=frequency
    )

    affective_individual.write_physio_data_csv(output_location)


def _process_affective_individual(path_to_task: str,
                                  path_to_physio: str,
                                  path_to_experiment_info: str,
                                  experiment: str,
                                  physio_type: str,
                                  output_path: str,
                                  frequency: float):
    os.makedirs(os.path.join(output_path, experiment, 'report'), exist_ok=True)
    log_file_path = os.path.join(output_path, experiment, 'report', 'affective_individual.txt')
    log_file = open(log_file_path, "w")

    log_file.write(f"# Experiment: {experiment}\n\nOutput of the program:\n\n```\n")

    log_file.write("==Affective task individual==\n")

    try:
        affective_individual_data = prepare_affective_task_individual(
            path_to_task=path_to_task,
            path_to_physio=path_to_physio,
            path_to_experiment_info=path_to_experiment_info,
            experiment=experiment,
            physio_type=physio_type,
            output_file=log_file
        )

        computer_names = ['lion', 'tiger', 'leopard']
        processes = []
        for computer_name in computer_names:
            if computer_name not in affective_individual_data:
                continue

            processes.append(multiprocessing.Process(
                target=_process_affective_individual_per_computer,
                args=(
                    experiment,
                    affective_individual_data[computer_name]['participant_id'],
                    affective_individual_data[computer_name]['computer_name'],
                    affective_individual_data[computer_name]['task_csv_path'],
                    affective_individual_data[computer_name]['physio_csv_path'],
                    frequency,
                    output_path + '/' + experiment
                )
            ))

        for process in processes:
            process.start()

        for process in processes:
            process.join()
    except FileDoesNotExistError as e:
        log_file.write(str(e))

    log_file.write('```\n')
    log_file.close()


def _process_affective_team(path_to_task: str,
                            path_to_physio: str,
                            path_to_experiment_info: str,
                            experiment: str,
                            physio_type: str,
                            output_path: str,
                            frequency: float):
    os.makedirs(os.path.join(output_path, experiment, 'report'), exist_ok=True)
    log_file_path = os.path.join(output_path, experiment, 'report', 'affective_team.txt')
    log_file = open(log_file_path, "w")

    log_file.write(f"# Experiment: {experiment}\n\nOutput of the program:\n\n```\n")
    log_file.write("==Affective task team==\n")

    try:
        affective_team_data = prepare_affective_task_team(
            path_to_task=path_to_task,
            path_to_physio=path_to_physio,
            path_to_experiment_info=path_to_experiment_info,
            experiment=experiment,
            physio_type=physio_type,
            output_file=log_file
        )

        affective_team = AffectiveTaskTeam.from_files(
            affective_team_data['info'],
            affective_team_data['task_csv_path'],
            affective_team_data['physio_name_path'],
            frequency=frequency
        )

        affective_team.write_physio_data_csv(output_path + '/' + experiment)
    except FileDoesNotExistError as e:
        log_file.write(str(e) + '\n')

    log_file.write('```\n')
    log_file.close()


def __process_ping_pong_competitive_per_match(match: str,
                                              info_file: str,
                                              task_csv_path: str,
                                              physio_name_path: dict[str, str],
                                              frequency: float,
                                              output_location: str):
    ping_pong_competitive = PingPongCompetitive.from_files(
        info_file,
        task_csv_path,
        physio_name_path,
        frequency=frequency
    )

    ping_pong_competitive.write_physio_data_csv(output_location, match)


def _process_ping_pong_competitive(path_to_task: str,
                                   path_to_physio: str,
                                   path_to_experiment_info: str,
                                   experiment: str,
                                   physio_type: str,
                                   output_path: str,
                                   frequency: float):
    os.makedirs(os.path.join(output_path, experiment, 'report'), exist_ok=True)
    log_file_path = os.path.join(output_path, experiment, 'report', 'ping_pong_competitive.txt')
    log_file = open(log_file_path, "w")

    log_file.write(f"# Experiment: {experiment}\n\nOutput of the program:\n\n```\n")
    log_file.write("==Ping pong competitive==\n")

    try:
        ping_pong_competitive_data = prepare_ping_pong_competitive(
            path_to_task=path_to_task,
            path_to_physio=path_to_physio,
            path_to_experiment_info=path_to_experiment_info,
            experiment=experiment,
            physio_type=physio_type,
            output_file=log_file
        )

        matches = ['0', '1']
        processes = []
        for match in matches:
            processes.append(multiprocessing.Process(
                target=__process_ping_pong_competitive_per_match,
                args=(
                    match,
                    ping_pong_competitive_data[match]['info'],
                    ping_pong_competitive_data[match]['task_csv_path'],
                    ping_pong_competitive_data[match]['physio_name_path'],
                    frequency,
                    output_path + '/' + experiment
                )
            ))

        for process in processes:
            process.start()

        for process in processes:
            process.join()
    except FileDoesNotExistError as e:
        log_file.write(str(e) + '\n')

    log_file.write('```\n')
    log_file.close()


def _process_ping_pong_cooperative(path_to_task: str,
                                   path_to_physio: str,
                                   path_to_experiment_info: str,
                                   experiment: str,
                                   physio_type: str,
                                   output_path: str,
                                   frequency: float):
    os.makedirs(os.path.join(output_path, experiment, 'report'), exist_ok=True)
    log_file_path = os.path.join(output_path, experiment, 'report', 'ping_pong_cooperative.txt')
    log_file = open(log_file_path, "w")

    log_file.write(f"# Experiment: {experiment}\n\nOutput of the program:\n\n```\n")
    log_file.write("==Ping pong cooperative==\n")

    try:
        ping_pong_cooperative_data = prepare_ping_pong_cooperative(
            path_to_task=path_to_task,
            path_to_physio=path_to_physio,
            path_to_experiment_info=path_to_experiment_info,
            experiment=experiment,
            physio_type=physio_type,
            output_file=log_file
        )

        ping_pong_cooperative = PingPongCooperative.from_files(
            ping_pong_cooperative_data['info'],
            ping_pong_cooperative_data['task_csv_path'],
            ping_pong_cooperative_data['physio_name_path'],
            frequency=frequency
        )

        ping_pong_cooperative.write_physio_data_csv(output_path + '/' + experiment)
    except FileDoesNotExistError as e:
        log_file.write(str(e) + '\n')

    log_file.write('```\n')
    log_file.close()


def __process_minecraft_per_trial(mission: str,
                                  info_file: str,
                                  task_metadata_path: str,
                                  physio_name_path: dict[str, str],
                                  frequency: float,
                                  output_location: str):
    minecraft = Minecraft.from_files(
        info_file,
        task_metadata_path,
        physio_name_path,
        frequency=frequency
    )

    minecraft.write_physio_data_csv(output_location, mission)


def _process_minecraft(path_to_task: str,
                       path_to_physio: str,
                       path_to_experiment_info: str,
                       experiment: str,
                       physio_type: str,
                       output_path: str,
                       frequency: float):
    os.makedirs(os.path.join(output_path, experiment, 'report'), exist_ok=True)
    log_file_path = os.path.join(output_path, experiment, 'report', 'minecraft.txt')
    log_file = open(log_file_path, "w")

    log_file.write(f"# Experiment: {experiment}\n\nOutput of the program:\n\n```\n")
    log_file.write("==Minecraft==\n")

    try:
        minecraft_data = prepare_minecraft(
            path_to_task=path_to_task,
            path_to_physio=path_to_physio,
            path_to_experiment_info=path_to_experiment_info,
            experiment=experiment,
            physio_type=physio_type,
            output_file=log_file
        )

        processes = []
        for mission, mission_data in minecraft_data.items():
            processes.append(multiprocessing.Process(
                target=__process_minecraft_per_trial,
                args=(
                    mission,
                    mission_data['info'],
                    mission_data['task_metadata_path'],
                    mission_data['physio_name_path'],
                    frequency,
                    output_path + '/' + experiment
                )
            ))

        for process in processes:
            process.start()

        for process in processes:
            process.join()
    except FileDoesNotExistError as e:
        log_file.write(str(e) + '\n')

    log_file.write('```\n')
    log_file.close()


def process_experiment(path_to_task: str,
                       path_to_physio: str,
                       path_to_experiment_info: str,
                       physio_type: str,
                       experiments: list[str],
                       output_path: str,
                       frequency: float):
    pbar = tqdm(experiments)
    for experiment in pbar:
        pbar.set_description(experiment)
        # Create the directories if they don't exist
        os.makedirs(os.path.join(output_path, experiment), exist_ok=True)

        processes = [
            multiprocessing.Process(
                target=_process_rest_state,
                args=(
                    path_to_task,
                    path_to_physio,
                    path_to_experiment_info,
                    experiment,
                    physio_type,
                    output_path,
                    frequency
                )
            ),
            multiprocessing.Process(
                target=_process_finger_tapping,
                args=(
                    path_to_task,
                    path_to_physio,
                    path_to_experiment_info,
                    experiment,
                    physio_type,
                    output_path,
                    frequency
                )
            ),
            multiprocessing.Process(
                target=_process_affective_individual,
                args=(
                    path_to_task,
                    path_to_physio,
                    path_to_experiment_info,
                    experiment,
                    physio_type,
                    output_path,
                    frequency
                )
            ),
            multiprocessing.Process(
                target=_process_affective_team,
                args=(
                    path_to_task,
                    path_to_physio,
                    path_to_experiment_info,
                    experiment,
                    physio_type,
                    output_path,
                    frequency
                )
            ),
            multiprocessing.Process(
                target=_process_ping_pong_competitive,
                args=(
                    path_to_task,
                    path_to_physio,
                    path_to_experiment_info,
                    experiment,
                    physio_type,
                    output_path,
                    frequency
                )
            ),
            multiprocessing.Process(
                target=_process_ping_pong_cooperative,
                args=(
                    path_to_task,
                    path_to_physio,
                    path_to_experiment_info,
                    experiment,
                    physio_type,
                    output_path,
                    frequency
                )
            ),
            multiprocessing.Process(
                target=_process_minecraft,
                args=(
                    path_to_task,
                    path_to_physio,
                    path_to_experiment_info,
                    experiment,
                    physio_type,
                    output_path,
                    frequency
                )
            ),
        ]

        for process in processes:
            process.start()

        for process in processes:
            process.join()
