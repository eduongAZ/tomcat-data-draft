import os

from tasks import RestState, FingerTapping, AffectiveTaskIndividual, AffectiveTaskTeam, \
    PingPongCompetitive, PingPongCooperative, Minecraft
from .prepare import prepare_rest_state, prepare_finger_tapping, prepare_affective_task_individual, \
    prepare_affective_task_team, prepare_ping_pong_competitive, prepare_ping_pong_cooperative, \
    prepare_minecraft, FileDoesNotExistError


def process_experiment(path_to_task: str,
                       path_to_physio: str,
                       path_to_experiment_info: str,
                       physio_type: str,
                       experiments: list[str],
                       output_path: str):
    for experiment in experiments:
        # Create the directories if they don't exist
        os.makedirs(os.path.join(output_path, experiment), exist_ok=True)

        log_file = open(os.path.join(output_path, experiment, 'README.md'), "a")
        log_file.write(f"# Experiment: {experiment}\n\nOutput of the program:\n\n```")

        log_file.write("[Processing] " + experiment + '\n')
        # Rest state
        log_file.write("Rest state\n")
        try:
            rest_state_data = prepare_rest_state(
                path_to_task=path_to_task,
                path_to_physio=path_to_physio,
                path_to_experiment_info=path_to_experiment_info,
                experiment=experiment,
                physio_type=physio_type
            )

            rest_state = RestState.from_files(
                rest_state_data['info'],
                rest_state_data['task_csv_path'],
                rest_state_data['physio_name_path']
            )

            rest_state.write_physio_data_csv(output_path + '/' + experiment)
        except FileDoesNotExistError as e:
            log_file.write(str(e) + '\n')

        # Finger tapping
        log_file.write("Finger tapping\n")
        try:
            finger_tapping_data = prepare_finger_tapping(
                path_to_task=path_to_task,
                path_to_physio=path_to_physio,
                path_to_experiment_info=path_to_experiment_info,
                experiment=experiment,
                physio_type=physio_type
            )

            finger_tapping = FingerTapping.from_files(
                finger_tapping_data['info'],
                finger_tapping_data['task_csv_path'],
                finger_tapping_data['physio_name_path']
            )

            finger_tapping.write_physio_data_csv(output_path + '/' + experiment)
        except FileDoesNotExistError as e:
            log_file.write(str(e) + '\n')

        # Affective task individual
        log_file.write("Affective task individual:\n")
        computer_names = ['lion', 'tiger', 'leopard']
        for computer_name in computer_names:
            log_file.write("\tAffective task individual " + computer_name + '\n')
            try:
                affective_individual_data = prepare_affective_task_individual(
                    path_to_task=path_to_task,
                    path_to_physio=path_to_physio,
                    path_to_experiment_info=path_to_experiment_info,
                    experiment=experiment,
                    physio_type=physio_type,
                    output_file=log_file
                )

                affective_individual = AffectiveTaskIndividual.from_files(
                    affective_individual_data[computer_name]['participant_id'],
                    affective_individual_data[computer_name]['computer_name'],
                    affective_individual_data[computer_name]['task_csv_path'],
                    affective_individual_data[computer_name]['physio_csv_path']
                )

                affective_individual.write_physio_data_csv(output_path + '/' + experiment)
            except FileDoesNotExistError as e:
                log_file.write(str(e))

        # Affective task team
        log_file.write("Affective task team\n")
        try:
            affective_team_data = prepare_affective_task_team(
                path_to_task=path_to_task,
                path_to_physio=path_to_physio,
                path_to_experiment_info=path_to_experiment_info,
                experiment=experiment,
                physio_type=physio_type
            )

            affective_team = AffectiveTaskTeam.from_files(
                affective_team_data['info'],
                affective_team_data['task_csv_path'],
                affective_team_data['physio_name_path']
            )

            affective_team.write_physio_data_csv(output_path + '/' + experiment)
        except FileDoesNotExistError as e:
            log_file.write(str(e) + '\n')

        # Ping pong competitive
        log_file.write("Ping pong competitive:\n")
        matches = ['0', '1']
        for match in matches:
            log_file.write("\tPing pong competitive " + match + '\n')
            try:
                ping_pong_competitive_data = prepare_ping_pong_competitive(
                    path_to_task=path_to_task,
                    path_to_physio=path_to_physio,
                    path_to_experiment_info=path_to_experiment_info,
                    experiment=experiment,
                    physio_type=physio_type,
                    output_file=log_file
                )

                ping_pong_competitive = PingPongCompetitive.from_files(
                    ping_pong_competitive_data[match]['info'],
                    ping_pong_competitive_data[match]['task_csv_path'],
                    ping_pong_competitive_data[match]['physio_name_path']
                )

                ping_pong_competitive.write_physio_data_csv(output_path + '/' + experiment, match)
            except FileDoesNotExistError as e:
                log_file.write(str(e) + '\n')

        # Ping pong cooperative
        log_file.write("Ping pong cooperative\n")
        try:
            ping_pong_cooperative_data = prepare_ping_pong_cooperative(
                path_to_task=path_to_task,
                path_to_physio=path_to_physio,
                path_to_experiment_info=path_to_experiment_info,
                experiment=experiment,
                physio_type=physio_type
            )

            ping_pong_cooperative = PingPongCooperative.from_files(
                ping_pong_cooperative_data['info'],
                ping_pong_cooperative_data['task_csv_path'],
                ping_pong_cooperative_data['physio_name_path']
            )

            ping_pong_cooperative.write_physio_data_csv(output_path + '/' + experiment)
        except FileDoesNotExistError as e:
            log_file.write(str(e) + '\n')

        # Minecraft
        log_file.write("Minecraft:\n")
        try:
            minecraft_data = prepare_minecraft(
                path_to_task=path_to_task,
                path_to_physio=path_to_physio,
                path_to_experiment_info=path_to_experiment_info,
                experiment=experiment,
                physio_type=physio_type,
                output_file=log_file
            )

            for mission, mission_data in minecraft_data.items():
                log_file.write("\tMinecraft " + mission + '\n')
                minecraft = Minecraft.from_files(
                    mission_data['info'],
                    mission_data['task_metadata_path'],
                    mission_data['physio_name_path']
                )

                minecraft.write_physio_data_csv(output_path + '/' + experiment, mission)
        except FileDoesNotExistError as e:
            log_file.write(str(e) + '\n')

        log_file.write('```\n')
        log_file.close()
