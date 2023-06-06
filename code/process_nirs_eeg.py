from pipeline import process_experiment

path_to_task = '/space/eduong/exp_tasks'
path_to_physio = '/space/rchamplin/Neurips/rerun_2023_06_03'
path_to_experiment_info = '/space/eduong/exp_info'
output_dir = '/tomcat/data/derived/drafts/draft_2023_06_05_11'

nirs_physio_type = 'nirs'
nirs_output_path = f'{output_dir}/nirs'
nirs_frequency = 20.0

eeg_physio_type = 'eeg'
eeg_output_path = f'{output_dir}/eeg'
eeg_frequency = 500.0

experiments = [
    # "exp_2022_09_30_10",  # Does not have physio data for minecraft
    # "exp_2022_10_04_09",
    # "exp_2022_10_07_15",
    # "exp_2022_10_14_10",
    # "exp_2022_10_18_10",
    # "exp_2022_10_21_15",
    # "exp_2022_10_24_12",  # Baseline task 00027, but Rick's sheet says 99999 EA
    # "exp_2022_10_27_10",  # Baseline task 00065, but Rick's sheet says 99999 ED
    # "exp_2022_10_28_10",  # Baseline task 00056, but Rick's sheet says 99999 ED
    # "exp_2022_10_31_10",  # Baseline task 00062, but Rick's sheet says 99999 VS
    # "exp_2022_11_01_10",
    # "exp_2022_11_04_10",
    # "exp_2022_11_07_10",
    # "exp_2022_11_08_11",
    # "exp_2022_11_10_10",
    # "exp_2022_11_14_12",
    # "exp_2022_11_15_13",
    # "exp_2022_11_17_15",
    # "exp_2022_11_18_10",
    # "exp_2022_11_22_10",
    # "exp_2022_12_02_15",
    # "exp_2022_12_05_12", # DO NOT INCLUDE, Program crashed
    # "exp_2023_01_30_13",
    # "exp_2023_01_31_14", # DO NOT INCLUDE, Adarsh said skip because Minecraft problematic
    # "exp_2023_02_03_10",
    # "exp_2023_02_06_13",
    # "exp_2023_02_07_14",
    # "exp_2023_02_10_10", # DO NOT INCLDUE, Does not have minecraft message mission start/stop
    # "exp_2023_02_16_14",
    # "exp_2023_02_20_01",
    # "exp_2023_02_21_14",
    "exp_2023_04_17_13",
    "exp_2023_04_18_14",
    "exp_2023_04_21_10",
    "exp_2023_04_24_13",
    "exp_2023_04_27_14",
    "exp_2023_04_28_10",
    "exp_2023_05_01_13",
    "exp_2023_05_02_14",
    "exp_2023_05_03_10"
]

if __name__ == '__main__':
    print("Processing NIRS data")
    process_experiment(
        path_to_task,
        path_to_physio,
        path_to_experiment_info,
        nirs_physio_type,
        experiments,
        nirs_output_path,
        nirs_frequency
    )

    print("Processing EEG data")
    process_experiment(
        path_to_task,
        path_to_physio,
        path_to_experiment_info,
        eeg_physio_type,
        experiments,
        eeg_output_path,
        eeg_frequency
    )
