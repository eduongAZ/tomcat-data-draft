from common import ReportWriter
from io import StringIO
import os

from .task import prepare_rest_state, prepare_finger_tapping, prepare_affective_team, prepare_ping_pong_cooperative


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
    for physio_type, physio_type_info in physio_type_data.items():
        string_stream.write(f'# Processing {physio_type} data\n\n')
        experiments_tasks_data[physio_type] = {}

        for experiment in experiments:
            experiments_tasks_data[physio_type][experiment] = {}

            # Rest state
            string_stream.write(f'[{experiment}] Processing rest state\n')
            task_data, status, message = prepare_rest_state(
                task_data_path,
                os.path.join(physio_data_path, physio_type),
                experiment_info_path,
                experiment,
                physio_type,
                synchronization_frequency,
                os.path.join(output_dir, experiment, physio_type),
                physio_type_info['interpolation_method']
            )
            string_stream.write(message)
            if status:
                experiments_tasks_data[physio_type][experiment]['rest_state'] = task_data

            # Finger tapping
            string_stream.write(f'[{experiment}] Processing finger tapping\n')
            task_data, status, message = prepare_finger_tapping(
                task_data_path,
                os.path.join(physio_data_path, physio_type),
                experiment_info_path,
                experiment,
                physio_type,
                synchronization_frequency,
                os.path.join(output_dir, experiment, physio_type),
                physio_type_info['interpolation_method']
            )
            string_stream.write(message)
            if status:
                experiments_tasks_data[physio_type][experiment]['finger_tapping'] = task_data

            string_stream.write(f'[{experiment}] Processing affective individual\n')

            experiments_tasks_data[physio_type][experiment]['affective_individual'] = {}

            # Affective team
            string_stream.write(f'[{experiment}] Processing affective team\n')
            task_data, status, message = prepare_affective_team(
                task_data_path,
                os.path.join(physio_data_path, physio_type),
                experiment_info_path,
                experiment,
                physio_type,
                synchronization_frequency,
                os.path.join(output_dir, experiment, physio_type),
                physio_type_info['interpolation_method']
            )
            string_stream.write(message)
            if status:
                experiments_tasks_data[physio_type][experiment]['affective_team'] = task_data

            string_stream.write(f'[{experiment}] Processing ping pong competitive\n')

            experiments_tasks_data[physio_type][experiment]['ping_pong_competitive'] = {}

            string_stream.write(f'[{experiment}] Processing ping pong cooperative\n')

            task_data, status, message = prepare_ping_pong_cooperative(
                task_data_path,
                os.path.join(physio_data_path, physio_type),
                experiment_info_path,
                experiment,
                physio_type,
                synchronization_frequency,
                os.path.join(output_dir, experiment, physio_type),
                physio_type_info['interpolation_method']
            )
            string_stream.write(message)
            if status:
                experiments_tasks_data[physio_type][experiment]['ping_pong_cooperative'] = task_data

            string_stream.write(f'[{experiment}] Processing minecraft training\n')

            experiments_tasks_data[physio_type][experiment]['minecraft_training'] = {}

            string_stream.write(f'[{experiment}] Processing minecraft saturn A\n')

            experiments_tasks_data[physio_type][experiment]['minecraft_saturn_a'] = {}

            string_stream.write(f'[{experiment}] Processing minecraft saturn B\n\n')

            experiments_tasks_data[physio_type][experiment]['minecraft_saturn_b'] = {}

            # experiment_tasks_data = {
            #     'frequency': synchronization_frequency,
            #     'report_writer': ReportWriter(os.path.join(output_dir, experiment, physio_type, 'report')),
            #     'interpolation_method': physio_type_info['interpolation_method']
            # }

    report_writer('processing_preparation_report.txt', string_stream.getvalue(), to_terminal=verbose)

    return experiments_tasks_data
