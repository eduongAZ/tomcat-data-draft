import os

from common import ReportWriter
from config import *
from interpolation import linear_interpolation
from prepare import prepare_task_data
from process import process_task_data

if __name__ == "__main__":
    synchronization_frequency = 2000.0
    physio_type_output_dir = os.path.join(output_dir, 'eeg')
    os.makedirs(physio_type_output_dir, exist_ok=True)

    report_writer = ReportWriter(os.path.join(physio_type_output_dir, 'report'))
    physio_type_data = {
        "eeg": {
            "interpolation_method": linear_interpolation
        }
    }

    os.makedirs(physio_type_output_dir + '/report', exist_ok=True)
    experiments_tasks_data = prepare_task_data(
        task_data_path,
        physio_data_path,
        experiment_info_path,
        physio_type_output_dir,
        synchronization_frequency,
        report_writer,
        physio_type_data,
        experiments,
        verbose=False
    )

    process_task_data(experiments_tasks_data, num_processors=24)
