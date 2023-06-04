import os

import pandas as pd

from physio import combine_participants_physio_from_files
from utils import read_csv_file
from utils import read_json_file


def _combine_ping_pong_physio_task(ping_pong_task_df: pd.DataFrame,
                                   ping_pong_physio_df: pd.DataFrame) -> pd.DataFrame:
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

    # Drop columns
    merged_df = merged_df.drop(columns=['monotonic_time', 'human_readable_time'])

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
                   ping_pong_physio_name_filepath: dict[str, str],
                   frequency: float):
        """
        Create a PingPongCooperative object from a metadata dictionary
        :param frequency: frequency of the physio data
        :param ping_pong_physio_name_filepath: ping pong physio directory name-filepath mapping
        :param ping_pong_csv_path: ping pong csv file path
        :param metadata_path: json file metadata path
        :return: PingPongCooperative object
        """
        # Read metadata
        metadata = read_json_file(metadata_path)
        participant_ids = metadata['participant_ids']

        # Read ping pong task data
        ping_pong_task_df = read_csv_file(ping_pong_csv_path, delimiter=';')

        start_time = ping_pong_task_df['time'].iloc[0]
        end_time = ping_pong_task_df['time'].iloc[-1]

        # Read physio data
        physio_id_filepath = {v: ping_pong_physio_name_filepath[k] for k, v in
                              participant_ids.items() if k in ping_pong_physio_name_filepath}

        ping_pong_physio = combine_participants_physio_from_files(
            physio_id_filepath,
            start_time,
            end_time,
            frequency
        )

        ping_pong_physio = ping_pong_physio.reset_index()

        ping_pong_physio['experiment_id'] = metadata['experiment']
        ping_pong_physio['lion_id'] = participant_ids['lion']
        ping_pong_physio['tiger_id'] = participant_ids['tiger']
        ping_pong_physio['leopard_id'] = participant_ids['leopard']

        ping_pong_physio_task = _combine_ping_pong_physio_task(
            ping_pong_task_df,
            ping_pong_physio
        )

        ping_pong_physio_task = ping_pong_physio_task.set_index('unix_time')

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
