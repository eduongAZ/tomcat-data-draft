import os
from io import StringIO

from common import ReportWriter
from .task import *


def prepare_task_data(task_data_path: str,
                      physio_data_path: str,
                      experiment_info_path: str,
                      output_dir: str,
                      synchronization_frequency: float,
                      report_writer: ReportWriter,
                      physio_type_data: dict[str, dict[str, any]],
                      experiments: list[str],
                      verbose: bool = False) -> dict[str, dict[str, dict[str, any]]]:
    string_stream = StringIO()

    experiments_tasks_data = {}

    for experiment in experiments:
        experiments_tasks_data[experiment] = {}

        string_stream.write(f"[{experiment}]\n")

        # Rest state
        string_stream.write('(Preparing rest state)\n')
        task_data, status, message = prepare_rest_state(
            task_data_path,
            physio_data_path,
            experiment_info_path,
            experiment,
            physio_type_data,
            synchronization_frequency,
            os.path.join(output_dir, experiment)
        )
        string_stream.write(message)
        if status:
            experiments_tasks_data[experiment]['rest_state'] = task_data

        # Finger tapping
        string_stream.write('(Preparing finger tapping)\n')
        task_data, status, message = prepare_finger_tapping(
            task_data_path,
            physio_data_path,
            experiment_info_path,
            experiment,
            physio_type_data,
            synchronization_frequency,
            os.path.join(output_dir, experiment)
        )
        string_stream.write(message)
        if status:
            experiments_tasks_data[experiment]['finger_tapping'] = task_data

        # Affective individual
        string_stream.write('(Preparing affective individual)\n')
        task_data, status, message = prepare_affective_individual(
            task_data_path,
            physio_data_path,
            experiment_info_path,
            experiment,
            physio_type_data,
            synchronization_frequency,
            os.path.join(output_dir, experiment)
        )
        string_stream.write(message)
        if status:
            experiments_tasks_data[experiment].update(task_data)

        # Affective team
        string_stream.write('(Preparing affective team)\n')
        task_data, status, message = prepare_affective_team(
            task_data_path,
            physio_data_path,
            experiment_info_path,
            experiment,
            physio_type_data,
            synchronization_frequency,
            os.path.join(output_dir, experiment)
        )
        string_stream.write(message)
        if status:
            experiments_tasks_data[experiment]['affective_team'] = task_data

        # Ping pong competitive
        string_stream.write('(Preparing ping pong competitive)\n')
        task_data, status, message = prepare_ping_pong_competitive(
            task_data_path,
            physio_data_path,
            experiment_info_path,
            experiment,
            physio_type_data,
            synchronization_frequency,
            os.path.join(output_dir, experiment)
        )
        string_stream.write(message)
        if status:
            experiments_tasks_data[experiment].update(task_data)

        # Ping pong cooperative
        string_stream.write('(Preparing ping pong cooperative)\n')
        task_data, status, message = prepare_ping_pong_cooperative(
            task_data_path,
            physio_data_path,
            experiment_info_path,
            experiment,
            physio_type_data,
            synchronization_frequency,
            os.path.join(output_dir, experiment)
        )
        string_stream.write(message)
        if status:
            experiments_tasks_data[experiment]['ping_pong_cooperative'] = task_data

        # Prepare Minecraft missions
        string_stream.write('(Preparing minecraft missions)\n')
        task_data, status, message = prepare_minecraft(
            task_data_path,
            physio_data_path,
            experiment_info_path,
            experiment,
            physio_type_data,
            synchronization_frequency,
            os.path.join(output_dir, experiment)
        )
        string_stream.write(message)
        if status:
            experiments_tasks_data[experiment].update(task_data)

        string_stream.write('\n')

    report_writer('data_preparation_report.txt', string_stream.getvalue(), to_terminal=verbose)

    return experiments_tasks_data
