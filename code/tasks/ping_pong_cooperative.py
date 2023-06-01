import os

import pandas as pd

from physio import combine_participants_physio
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


class PingPongCooperative:
    def __init__(self,
                 participant_ids: dict,
                 ping_pong_task_df: pd.DataFrame,
                 ping_pong_physio: pd.DataFrame,
                 ping_pong_physio_task: pd.DataFrame
                 ):
        self.participant_ids = participant_ids
        self.ping_pong_task_df = ping_pong_task_df
        self.ping_pong_physio = ping_pong_physio
        self.ping_pong_physio_task = ping_pong_physio_task

    @classmethod
    def from_files(cls,
                   metadata_path: str,
                   ping_pong_csv_path: str,
                   ping_pong_physio_directory: str,
                   num_increments: int = 1324):
        """
        Create a PingPongCooperative object from a metadata dictionary
        :param num_increments: number of time series increments
        :param ping_pong_physio_directory: ping pong physio directory
        :param ping_pong_csv_path: ping pong csv file path
        :param metadata_path: json file metadata path
        :return: PingPongCooperative object
        """
        # Read metadata
        metadata = read_json_file(metadata_path)
        participant_ids = metadata['participant_ids']

        # Read ping pong task data
        ping_pong_task_df = read_csv_file(ping_pong_csv_path, delimiter=';')

        lion_ping_pong_physio_csv_path = ping_pong_physio_directory + '/lion/NIRS_filtered_ping_pong_cooperative.csv'
        tiger_ping_pong_physio_csv_path = ping_pong_physio_directory + '/tiger/NIRS_filtered_ping_pong_cooperative.csv'
        leopard_ping_pong_physio_csv_path = ping_pong_physio_directory + '/leopard/NIRS_filtered_ping_pong_cooperative.csv'

        ping_pong_physio = {
            participant_ids['lion']: read_csv_file(lion_ping_pong_physio_csv_path,
                                                   delimiter='\t'),
            participant_ids['tiger']: read_csv_file(tiger_ping_pong_physio_csv_path,
                                                    delimiter='\t'),
            participant_ids['leopard']: read_csv_file(leopard_ping_pong_physio_csv_path,
                                                      delimiter='\t'),
        }

        start_time = ping_pong_task_df['time'].iloc[0]
        end_time = ping_pong_task_df['time'].iloc[-1]

        ping_pong_physio = combine_participants_physio(
            ping_pong_physio,
            start_time,
            end_time,
            num_increments=num_increments
        )

        ping_pong_physio_task = _combine_ping_pong_physio_task(
            ping_pong_task_df,
            ping_pong_physio
        )

        return cls(
            participant_ids=participant_ids,
            ping_pong_task_df=ping_pong_task_df,
            ping_pong_physio=ping_pong_physio,
            ping_pong_physio_task=ping_pong_physio_task
        )

    def write_physio_data_csv(self, output_dir_path: str):
        """
        Write the physio data to a csv file in output directory
        :param output_dir_path: output directory path
        """
        # Create the directory if it doesn't exist
        if not os.path.exists(output_dir_path):
            os.makedirs(output_dir_path)

        self.ping_pong_physio_task.to_csv(
            output_dir_path + '/ping_pong_cooperative_physio_task.csv',
            index=True)