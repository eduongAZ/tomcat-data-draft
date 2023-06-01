import os

import pandas as pd

from physio import combine_participants_physio_from_files
from utils import read_csv_file
from utils import read_json_file


def _combine_ping_pong_physio_task(ping_pong_task_df: pd.DataFrame,
                                   ping_pong_physio_df: pd.DataFrame) -> pd.DataFrame:
    # Reset the index
    ping_pong_physio_df = ping_pong_physio_df.reset_index()
    ping_pong_task_df = ping_pong_task_df.reset_index()

    # Save the original 'unix_time' column
    original_unix_time = ping_pong_physio_df['unix_time'].copy()

    # Ensure that 'unix_time' and 'time' columns are in datetime format
    ping_pong_physio_df['unix_time'] = pd.to_datetime(ping_pong_physio_df['unix_time'],
                                                      unit='s')
    ping_pong_task_df['time'] = pd.to_datetime(ping_pong_task_df['time'], unit='s')

    # Use merge_asof to merge the dataframes based on time, assigning the task data to the closest
    # physio data entry that is before it.
    merged_df = pd.merge_asof(ping_pong_physio_df, ping_pong_task_df,
                              left_on='unix_time', right_on='time', direction='backward',
                              suffixes=('_physio_data', '_task_data'))

    # Restore the original 'unix_time' column
    merged_df['unix_time'] = original_unix_time

    # Drop the 'time' column from the task data as it's redundant now
    merged_df = merged_df.drop(columns=['time'])

    # Set 'unix_time' back as the index
    merged_df = merged_df.set_index('unix_time')

    return merged_df


class PingPongCompetitive:
    def __init__(self,
                 participant_ids: dict,
                 ping_pong_tasks: pd.DataFrame,
                 ping_pong_physio: pd.DataFrame,
                 ping_pong_physio_task: pd.DataFrame
                 ):
        self.participant_ids = participant_ids
        self.ping_pong_matches_task = ping_pong_tasks
        self.ping_pong_physio = ping_pong_physio
        self.ping_pong_physio_task = ping_pong_physio_task

    @classmethod
    def from_files(cls,
                   metadata_path: str,
                   ping_pong_task_csv_path: str,
                   ping_pong_physio_name_filepath: dict[str, str],
                   num_increments: int = 1324):
        """
        Create a PingPongCompetitive object from a metadata dictionary
        :param num_increments: number of time series increments
        :param ping_pong_physio_name_filepath: ping pong competitive physio name-filepath mapping
        :param ping_pong_task_csv_path: ping pong competitive task path
        :param metadata_path: json file metadata path
        :return: PingPongCompetitive object
        """
        # Read metadata
        metadata = read_json_file(metadata_path)
        participant_ids = metadata['participant_ids']

        ping_pong_task_df = read_csv_file(ping_pong_task_csv_path, delimiter=';')

        start_time = ping_pong_task_df['time'].iloc[0]
        end_time = ping_pong_task_df['time'].iloc[-1]

        # Read finger tapping physio data
        physio_id_filepath = {v: ping_pong_physio_name_filepath[k] for k, v in
                              participant_ids.items() if k in ping_pong_physio_name_filepath}

        ping_pong_physio = combine_participants_physio_from_files(
            physio_id_filepath,
            start_time,
            end_time,
            num_increments
        )

        ping_pong_physio_task = _combine_ping_pong_physio_task(
            ping_pong_task_df,
            ping_pong_physio
        )

        return cls(
            participant_ids=participant_ids,
            ping_pong_tasks=ping_pong_task_df,
            ping_pong_physio=ping_pong_physio,
            ping_pong_physio_task=ping_pong_physio_task
        )

    def write_physio_data_csv(self, output_dir_path: str, match: int):
        """
        Write the physio data to a csv file in output directory
        :param match: ping pong competitive match id
        :param output_dir_path: output directory path
        """
        # Create the directory if it doesn't exist
        if not os.path.exists(output_dir_path):
            os.makedirs(output_dir_path)

        self.ping_pong_physio_task.to_csv(
            output_dir_path + f'/ping_pong_competitive_{match}_physio_task.csv',
            index=True)
