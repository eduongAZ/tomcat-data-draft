# The following configurations are for synchronizing physio data

task_data_path = '/space/eduong/exp_tasks'
physio_data_path = '/space/rchamplin/Neurips/rerun_filtered_2023_06_22'
experiment_info_path = '/space/eduong/exp_info'
output_dir = '/tomcat/data/derived/drafts/draft_2023_06_23_13'

experiments = [
    "exp_2022_09_30_10",
    "exp_2022_10_04_09",
    "exp_2022_10_07_15",
    "exp_2022_10_14_10",
    "exp_2022_10_18_10",
    "exp_2022_10_21_15",
    "exp_2022_10_24_12",
    "exp_2022_10_27_10",
    "exp_2022_10_28_10",
    "exp_2022_10_31_10",
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
    # "exp_2022_12_05_12",  # DO NOT INCLUDE, Program crashed
    "exp_2023_01_30_13",
    # "exp_2023_01_31_14",  # DO NOT INCLUDE, because Minecraft data needs cleaning
    "exp_2023_02_03_10",
    "exp_2023_02_06_13",
    "exp_2023_02_07_14",
    # "exp_2023_02_10_10",  # DO NOT INCLUDE, because Minecraft data needs cleaning
    "exp_2023_02_16_14",
    "exp_2023_02_20_01",
    "exp_2023_02_21_14",
    "exp_2023_04_17_13",
    "exp_2023_04_18_14",
    "exp_2023_04_21_10",
    "exp_2023_04_24_13",
    "exp_2023_04_27_14",
    "exp_2023_04_28_10",
    "exp_2023_05_01_13",  # Minecraft data needs cleaning
    "exp_2023_05_02_14",
    "exp_2023_05_03_10"
]

# The following configurations are for analyzing physio data correlation vs score

correlation_analysis_blacklist = [
    "exp_2022_09_30_10",  # Saturn A score is 60, too low
    "exp_2023_02_07_14",  # Saturn A score is 50, too low
    "exp_2022_10_18_10",  # Saturn A score is 100, too low
]

physio_task_dir = "/home/eric/Documents/projects/tomcat-data-draft/data/from_gauss_old"
correlation_output_dir = "./code_outputs"
