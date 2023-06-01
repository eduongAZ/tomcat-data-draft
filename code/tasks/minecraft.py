import json
import os
from datetime import datetime

import pandas as pd

from physio import combine_participants_physio
from utils import read_csv_file
from utils import read_json_file


def _metadata_message_generator(metadata_file_path: str):
    with open(metadata_file_path, 'r') as metadata_file:
        for line in metadata_file:
            yield json.loads(line)


def _read_metadata_file(metadata_file_path: str) -> pd.DataFrame:
    messages = _metadata_message_generator(metadata_file_path)

    trial_topic = "trial"
    score_topic = "observations/events/scoreboard"
    trial_started = False

    task_data = {
        "time": [],
        "score": []
    }

    # parse messages
    for message in messages:
        # parse trial message
        if "topic" in message and message["topic"] == trial_topic:
            if message["msg"]["sub_type"] == "start":
                trial_started = True
                continue
            # end parsing after the trial has ended
            else:
                break

        # only start monitoring after trial has started
        elif not trial_started:
            continue

        # extract score
        if "topic" in message and message["topic"] == score_topic:
            score = message["data"]["scoreboard"]["TeamScore"]
            timestamp = datetime.fromisoformat(
                message["header"]["timestamp"]).timestamp()
            task_data["score"].append(score)
            task_data["time"].append(timestamp)

    task_df = pd.DataFrame(task_data)
    # task_df.set_index('time', inplace=True)

    return task_df


def _combine_minecraft_physio_task(minecraft_task_df: pd.DataFrame,
                                   minecraft_physio_df: pd.DataFrame) -> pd.DataFrame:
    # Reset the index
    minecraft_physio_df = minecraft_physio_df.reset_index()

    # Save the original 'unix_time' column
    original_unix_time = minecraft_physio_df['unix_time'].copy()

    # Ensure that 'unix_time' and 'time' columns are in datetime format
    minecraft_physio_df['unix_time'] = pd.to_datetime(minecraft_physio_df['unix_time'],
                                                      unit='s')
    minecraft_task_df['time'] = pd.to_datetime(minecraft_task_df['time'], unit='s')

    # Use merge_asof to merge the dataframes based on time, assigning the task data to the closest
    # physio data entry that is before it.
    merged_df = pd.merge_asof(minecraft_physio_df, minecraft_task_df,
                              left_on='unix_time', right_on='time', direction='backward',
                              suffixes=('_physio_data', '_task_data'))

    # Restore the original 'unix_time' column
    merged_df['unix_time'] = original_unix_time

    # Drop the 'time' column from the task data as it's redundant now
    merged_df = merged_df.drop(columns=['time'])

    # Set 'unix_time' back as the index
    merged_df = merged_df.set_index('unix_time')

    return merged_df


class Minecraft:
    def __init__(self,
                 participant_ids: dict,
                 minecraft_task_df: pd.DataFrame,
                 minecraft_physio: pd.DataFrame,
                 minecraft_physio_task: pd.DataFrame
                 ):
        self.participant_ids = participant_ids
        self.minecraft_task_df = minecraft_task_df
        self.minecraft_physio = minecraft_physio
        self.minecraft_physio_task = minecraft_physio_task

    @classmethod
    def from_files(cls,
                   metadata_path: str,
                   minecraft_metadata_path: str,
                   minecraft_physio_name: str,
                   minecraft_physio_directory: str,
                   num_increments: int = 5780):
        """
        Create a FingerTapping object from a metadata dictionary
        :param num_increments: number of time series increments
        :param minecraft_physio_directory: minecraft physio directory
        :param minecraft_physio_name: minecraft physio file name
        :param minecraft_metadata_path: minecraft metadata file path
        :param metadata_path: json file metadata path
        :return: FingerTapping object
        """
        # Read metadata
        metadata = read_json_file(metadata_path)
        participant_ids = metadata['participant_ids']

        # Read finger tapping task data
        minecraft_task_df = _read_metadata_file(minecraft_metadata_path)

        lion_minecraft_physio_csv_path = minecraft_physio_directory + '/lion/' + minecraft_physio_name
        tiger_minecraft_physio_csv_path = minecraft_physio_directory + '/tiger/' + minecraft_physio_name
        leopard_minecraft_physio_csv_path = minecraft_physio_directory + '/leopard/' + minecraft_physio_name

        minecraft_physio = {
            participant_ids['lion']: read_csv_file(lion_minecraft_physio_csv_path,
                                                   delimiter='\t'),
            participant_ids['tiger']: read_csv_file(tiger_minecraft_physio_csv_path,
                                                    delimiter='\t'),
            participant_ids['leopard']: read_csv_file(leopard_minecraft_physio_csv_path,
                                                      delimiter='\t'),
        }

        start_time = minecraft_task_df['time'].iloc[0]
        end_time = minecraft_task_df['time'].iloc[-1]

        minecraft_physio = combine_participants_physio(
            minecraft_physio,
            start_time,
            end_time,
            num_increments=num_increments
        )

        minecraft_physio_task = _combine_minecraft_physio_task(
            minecraft_task_df,
            minecraft_physio
        )

        return cls(
            participant_ids=participant_ids,
            minecraft_task_df=minecraft_task_df,
            minecraft_physio=minecraft_physio,
            minecraft_physio_task=minecraft_physio_task
        )

    def write_physio_data_csv(self,
                              output_dir_path: str,
                              mission_name: str):
        """
        Write the physio data to a csv file in output directory
        :param mission_name: name of mission
        :param output_dir_path: output directory path
        """
        # Create the directory if it doesn't exist
        if not os.path.exists(output_dir_path):
            os.makedirs(output_dir_path)

        self.minecraft_physio_task.to_csv(
            output_dir_path + f'/minecraft_{mission_name}_physio_task.csv',
            index=True)
