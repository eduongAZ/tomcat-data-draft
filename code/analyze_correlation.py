import csv
import os

import pandas as pd

from config import correlation_analysis_blacklist
from config import physio_task_dir, correlation_output_dir
from models import regression, NIRS_CHANNELS, EEG_CHANNELS


def list_experiments_minecraft_saturn_a_score(physio_task_dir: str):
    # Get all directories inside the physio_task_dir
    experiments = os.listdir(physio_task_dir)

    for experiment in experiments:
        # Get minecraft file path
        minecraft_file_path = os.path.join(physio_task_dir, experiment,
                                           "minecraft_saturn_a_physio_task.csv")

        # Check if the file exists and is not empty
        if not os.path.exists(minecraft_file_path) or os.stat(minecraft_file_path).st_size == 0:
            continue

        # Read the file
        with open(minecraft_file_path, mode='r') as f:

            # Read dataframe
            df = pd.read_csv(f)

            # Get score from the last row
            score = df.iloc[-1]["score"]

            print(experiment, score)


def write_experiment_to_csv(csv_filename: str,
                            rmse_per_channel: dict[str, float],
                            r2_per_channel: dict[str, float],
                            linear_regression_slope_per_channel: dict[str, float]):
    # Extract channel names
    channels = list(rmse_per_channel.keys())

    # Open the file in write mode and create a CSV writer object
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write header
        header = ['channel', 'rmse_per_channel', 'r2_per_channel', 'linear_regression_slope']
        writer.writerow(header)

        # Write the data rows
        for channel in channels:
            writer.writerow([
                channel,
                rmse_per_channel[channel],
                r2_per_channel[channel],
                linear_regression_slope_per_channel[channel]
            ])


if __name__ == "__main__":
    if not os.path.exists(physio_task_dir):
        os.makedirs(physio_task_dir)

    nirs_physio_task_dir = f"{physio_task_dir}/nirs"
    nirs_correlation_output_dir = f"{correlation_output_dir}/nirs/files"
    nirs_image_output_dir = f"{correlation_output_dir}/images"
    # Create the output directory if it does not exist
    if not os.path.exists(nirs_physio_task_dir):
        os.makedirs(nirs_physio_task_dir)
    if not os.path.exists(nirs_image_output_dir):
        os.makedirs(nirs_image_output_dir)
    if not os.path.exists(nirs_correlation_output_dir):
        os.makedirs(nirs_correlation_output_dir)

    eeg_physio_task_dir = f"{physio_task_dir}/eeg"
    eeg_correlation_output_dir = f"{correlation_output_dir}/eeg/files"
    eeg_image_output_dir = f"{correlation_output_dir}/eeg/images"
    # Create the output directory if it does not exist
    if not os.path.exists(eeg_physio_task_dir):
        os.makedirs(eeg_physio_task_dir)
    if not os.path.exists(eeg_correlation_output_dir):
        os.makedirs(eeg_correlation_output_dir)
    if not os.path.exists(eeg_image_output_dir):
        os.makedirs(eeg_image_output_dir)

    # NIRS

    nirs_target_file = "ping_pong_cooperative_physio_task.csv"
    nirs_correlation_output_json = f"{nirs_correlation_output_dir}/ping_pong_cooperative_correlation.json"
    nirs_correlation_output_csv = f"{nirs_correlation_output_dir}/ping_pong_cooperative_correlation.csv"
    nirs_correlation_output_image = f"{nirs_image_output_dir}/ping_pong_cooperative"
    if not os.path.exists(nirs_correlation_output_image):
        os.makedirs(nirs_correlation_output_image)

    predictions_per_channel, \
        rmse_per_channel, \
        linear_regressor_per_channel, \
        r2_per_channel, \
        null_model_r2, \
        linear_regression_slope_per_channel = \
        regression(
            nirs_physio_task_dir,
            nirs_target_file,
            "score_left",
            NIRS_CHANNELS,
            nirs_correlation_output_image,
            show_plots=False,
            output_file_path=nirs_correlation_output_json,
            blacklist_experiments=correlation_analysis_blacklist)

    write_experiment_to_csv(nirs_correlation_output_csv,
                            rmse_per_channel,
                            r2_per_channel,
                            linear_regression_slope_per_channel)

    nirs_target_file = "minecraft_saturn_a_physio_task.csv"
    nirs_correlation_output_json = f"{nirs_correlation_output_dir}/minecraft_saturn_a_correlation.json"
    nirs_correlation_output_csv = f"{nirs_correlation_output_dir}/minecraft_saturn_a_correlation.csv"
    nirs_correlation_output_image = f"{nirs_image_output_dir}/minecraft_saturn_a"
    if not os.path.exists(nirs_correlation_output_image):
        os.makedirs(nirs_correlation_output_image)

    predictions_per_channel, \
        rmse_per_channel, \
        linear_regressor_per_channel, \
        r2_per_channel, \
        null_model_r2, \
        linear_regression_slope_per_channel = \
        regression(
            nirs_physio_task_dir,
            nirs_target_file,
            "score",
            NIRS_CHANNELS,
            nirs_correlation_output_image,
            show_plots=False,
            output_file_path=nirs_correlation_output_json,
            blacklist_experiments=correlation_analysis_blacklist)

    write_experiment_to_csv(nirs_correlation_output_csv,
                            rmse_per_channel,
                            r2_per_channel,
                            linear_regression_slope_per_channel)

    nirs_target_file = "minecraft_saturn_b_physio_task.csv"
    nirs_correlation_output_json = f"{nirs_correlation_output_dir}/minecraft_saturn_b_correlation.json"
    nirs_correlation_output_csv = f"{nirs_correlation_output_dir}/minecraft_saturn_b_correlation.csv"
    nirs_correlation_output_image = f"{nirs_image_output_dir}/minecraft_saturn_b"
    if not os.path.exists(nirs_correlation_output_image):
        os.makedirs(nirs_correlation_output_image)

    predictions_per_channel, \
        rmse_per_channel, \
        linear_regressor_per_channel, \
        r2_per_channel, \
        null_model_r2, \
        linear_regression_slope_per_channel = \
        regression(
            nirs_physio_task_dir,
            nirs_target_file,
            "score",
            NIRS_CHANNELS,
            nirs_correlation_output_image,
            show_plots=False,
            output_file_path=nirs_correlation_output_json,
            blacklist_experiments=correlation_analysis_blacklist)

    write_experiment_to_csv(nirs_correlation_output_csv,
                            rmse_per_channel,
                            r2_per_channel,
                            linear_regression_slope_per_channel)

    # EEG

    eeg_target_file = "ping_pong_cooperative_physio_task.csv"
    eeg_correlation_output_json = f"{eeg_correlation_output_dir}/ping_pong_cooperative_correlation.json"
    eeg_correlation_output_csv = f"{eeg_correlation_output_dir}/ping_pong_cooperative_correlation.csv"
    eeg_correlation_output_image = f"{eeg_image_output_dir}/ping_pong_cooperative"
    if not os.path.exists(eeg_correlation_output_image):
        os.makedirs(eeg_correlation_output_image)

    predictions_per_channel, \
        rmse_per_channel, \
        linear_regressor_per_channel, \
        r2_per_channel, \
        null_model_r2, \
        linear_regression_slope_per_channel = \
        regression(
            eeg_physio_task_dir,
            eeg_target_file,
            "score_left",
            EEG_CHANNELS,
            eeg_correlation_output_image,
            show_plots=False,
            output_file_path=eeg_correlation_output_json,
            blacklist_experiments=correlation_analysis_blacklist)

    write_experiment_to_csv(eeg_correlation_output_csv,
                            rmse_per_channel,
                            r2_per_channel,
                            linear_regression_slope_per_channel)

    eeg_target_file = "minecraft_saturn_a_physio_task.csv"
    eeg_correlation_output_json = f"{eeg_correlation_output_dir}/minecraft_saturn_a_correlation.json"
    eeg_correlation_output_csv = f"{eeg_correlation_output_dir}/minecraft_saturn_a_correlation.csv"
    eeg_correlation_output_image = f"{eeg_image_output_dir}/minecraft_saturn_a"
    if not os.path.exists(eeg_correlation_output_image):
        os.makedirs(eeg_correlation_output_image)

    predictions_per_channel, \
        rmse_per_channel, \
        linear_regressor_per_channel, \
        r2_per_channel, \
        null_model_r2, \
        linear_regression_slope_per_channel = \
        regression(
            eeg_physio_task_dir,
            eeg_target_file,
            "score",
            EEG_CHANNELS,
            eeg_correlation_output_image,
            show_plots=False,
            output_file_path=eeg_correlation_output_json,
            blacklist_experiments=correlation_analysis_blacklist)

    write_experiment_to_csv(eeg_correlation_output_csv,
                            rmse_per_channel,
                            r2_per_channel,
                            linear_regression_slope_per_channel)

    eeg_target_file = "minecraft_saturn_b_physio_task.csv"
    eeg_correlation_output_json = f"{eeg_correlation_output_dir}/minecraft_saturn_b_correlation.json"
    eeg_correlation_output_csv = f"{eeg_correlation_output_dir}/minecraft_saturn_b_correlation.csv"
    eeg_correlation_output_image = f"{eeg_image_output_dir}/minecraft_saturn_b"
    if not os.path.exists(eeg_correlation_output_image):
        os.makedirs(eeg_correlation_output_image)

    predictions_per_channel, \
        rmse_per_channel, \
        linear_regressor_per_channel, \
        r2_per_channel, \
        null_model_r2, \
        linear_regression_slope_per_channel = \
        regression(
            eeg_physio_task_dir,
            eeg_target_file,
            "score",
            EEG_CHANNELS,
            eeg_correlation_output_image,
            show_plots=False,
            output_file_path=eeg_correlation_output_json,
            blacklist_experiments=correlation_analysis_blacklist)

    write_experiment_to_csv(eeg_correlation_output_csv,
                            rmse_per_channel,
                            r2_per_channel,
                            linear_regression_slope_per_channel)
