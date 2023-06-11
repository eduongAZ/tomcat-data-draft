from common import ReportWriter
from io import StringIO
import os


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
            string_stream.write(f'[{experiment}] Processing rest state\n')

            string_stream.write(f'[{experiment}] Processing finger tapping\n')

            string_stream.write(f'[{experiment}] Processing affective individual\n')

            string_stream.write(f'[{experiment}] Processing affective team\n')

            string_stream.write(f'[{experiment}] Processing ping pong competitive 0\n')

            string_stream.write(f'[{experiment}] Processing ping pong competitive 1\n')

            string_stream.write(f'[{experiment}] Processing ping pong cooperative\n')

            string_stream.write(f'[{experiment}] Processing minecraft training\n')

            string_stream.write(f'[{experiment}] Processing minecraft saturn A\n')

            string_stream.write(f'[{experiment}] Processing minecraft saturn B\n\n')

            # experiment_tasks_data = {
            #     'frequency': synchronization_frequency,
            #     'report_writer': ReportWriter(os.path.join(output_dir, experiment, physio_type, 'report')),
            #     'interpolation_method': physio_type_info['interpolation_method']
            # }

    report_writer('processing_preparation_report.txt', string_stream.getvalue(), to_terminal=verbose)

    return experiments_tasks_data
