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
        print("[Processing] " + experiment)
        # Rest state
        print("Rest state")
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
            print(e)

        # Finger tapping
        print("Finger tapping")
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
            print(e)

        # Affective task individual
        print("Affective task individual:")
        computer_names = ['lion', 'tiger', 'leopard']
        for computer_name in computer_names:
            print("\tAffective task individual " + computer_name)
            try:
                affective_individual_data = prepare_affective_task_individual(
                    path_to_task=path_to_task,
                    path_to_physio=path_to_physio,
                    path_to_experiment_info=path_to_experiment_info,
                    experiment=experiment,
                    physio_type=physio_type
                )

                affective_individual = AffectiveTaskIndividual.from_files(
                    affective_individual_data[computer_name]['participant_id'],
                    affective_individual_data[computer_name]['computer_name'],
                    affective_individual_data[computer_name]['task_csv_path'],
                    affective_individual_data[computer_name]['physio_csv_path']
                )

                affective_individual.write_physio_data_csv(output_path + '/' + experiment)
            except FileDoesNotExistError as e:
                print(e)

        # Affective task team
        print("Affective task team")
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
            print(e)

        # Ping pong competitive
        print("Ping pong competitive:")
        matches = ['0', '1']
        for match in matches:
            print("\tPing pong competitive " + match)
            try:
                ping_pong_competitive_data = prepare_ping_pong_competitive(
                    path_to_task=path_to_task,
                    path_to_physio=path_to_physio,
                    path_to_experiment_info=path_to_experiment_info,
                    experiment=experiment,
                    physio_type=physio_type
                )

                ping_pong_competitive = PingPongCompetitive.from_files(
                    ping_pong_competitive_data[match]['info'],
                    ping_pong_competitive_data[match]['task_csv_path'],
                    ping_pong_competitive_data[match]['physio_name_path']
                )

                ping_pong_competitive.write_physio_data_csv(output_path + '/' + experiment, match)
            except FileDoesNotExistError as e:
                print(e)

        # Ping pong cooperative
        print("Ping pong cooperative")
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
            print(e)

        # Minecraft
        print("Minecraft:")
        try:
            minecraft_data = prepare_minecraft(
                path_to_task=path_to_task,
                path_to_physio=path_to_physio,
                path_to_experiment_info=path_to_experiment_info,
                experiment=experiment,
                physio_type=physio_type
            )

            for mission, mission_data in minecraft_data.items():
                print("\tMinecraft " + mission)
                minecraft = Minecraft.from_files(
                    mission_data['info'],
                    mission_data['task_metadata_path'],
                    mission_data['physio_name_path']
                )

                minecraft.write_physio_data_csv(output_path + '/' + experiment, mission)
        except FileDoesNotExistError as e:
            print(e)
