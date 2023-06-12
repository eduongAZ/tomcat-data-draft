import os

from common import ReportWriter
from interpolation import linear_interpolation
from prepare import prepare_task_data
from process import process_task_data

if __name__ == "__main__":
    task_data_path = '/home/eric/Documents/projects/tomcat-data-draft/data/raw/tasks'
    physio_data_path = '/home/eric/Documents/projects/tomcat-data-draft/data/raw/physio'
    experiment_info_path = '/home/eric/Documents/projects/tomcat-data-draft/data/raw/info'
    output_dir = '/home/eric/Documents/projects/tomcat-data-draft/data/derived'
    synchronization_frequency = 500.0
    report_writer = ReportWriter(os.path.join(output_dir, 'report'))
    physio_type_data = {
        "eeg": {
            "interpolation_method": linear_interpolation
        }
    }

    experiments = [
        "exp_2022_09_30_10",  # Does not have physio data for minecraft
        "exp_2022_10_04_09",
        "exp_2022_10_07_15",
        "exp_2022_10_14_10",
        "exp_2022_10_18_10",
        "exp_2022_10_21_15",
        "exp_2022_10_24_12",  # Baseline task 00027, but Rick's sheet says 99999 EA
        "exp_2022_10_27_10",  # Baseline task 00065, but Rick's sheet says 99999 ED
        "exp_2022_10_28_10",  # Baseline task 00056, but Rick's sheet says 99999 ED
        "exp_2022_10_31_10",  # Baseline task 00062, but Rick's sheet says 99999 VS
        "exp_2022_11_01_10",
        "exp_2022_11_04_10",
        "exp_2022_11_07_10",
        "exp_2022_11_08_11",
        "exp_2022_11_10_10",
        "exp_2022_11_14_12",
        "exp_2022_11_15_13",
        "exp_2022_11_17_15",
        "exp_2022_11_18_10",
        "exp_2022_11_22_10",
        "exp_2022_12_02_15",
        # "exp_2022_12_05_12", # DO NOT INCLUDE, Program crashed
        "exp_2023_01_30_13",
        # "exp_2023_01_31_14", # DO NOT INCLUDE, Adarsh said skip because Minecraft problematic
        "exp_2023_02_03_10",
        "exp_2023_02_06_13",
        "exp_2023_02_07_14",
        # "exp_2023_02_10_10", # DO NOT INCLUDE, Does not have minecraft message mission start/stop
        "exp_2023_02_16_14",
        "exp_2023_02_20_01",
        "exp_2023_02_21_14",
        "exp_2023_04_17_13",
        "exp_2023_04_18_14",
        "exp_2023_04_21_10",
        "exp_2023_04_24_13",
        "exp_2023_04_27_14",
        "exp_2023_04_28_10",
        # "exp_2023_05_01_13", # DO NOT INCLUDE, skip because Minecraft problematic
        "exp_2023_05_02_14",
        "exp_2023_05_03_10"
    ]

    os.makedirs(output_dir + '/report', exist_ok=True)
    experiments_tasks_data = prepare_task_data(
        task_data_path,
        physio_data_path,
        experiment_info_path,
        output_dir,
        synchronization_frequency,
        report_writer,
        physio_type_data,
        experiments,
        verbose=False
    )

    process_task_data(experiments_tasks_data, num_processors=15)