import os

import pandas as pd

from physio import combine_participants_physio
from utils import read_csv_file
from utils import read_json_file


def _combine_finger_tapping_physio_task(finger_tapping_task_df: pd.DataFrame,
                                        finger_tapping_physio_df: pd.DataFrame) -> pd.DataFrame:
    # Reset the index
    finger_tapping_physio_df = finger_tapping_physio_df.reset_index()
    finger_tapping_task_df = finger_tapping_task_df.reset_index()

    # Save the original 'unix_time' column
    original_unix_time = finger_tapping_physio_df['unix_time'].copy()

    # Ensure that 'unix_time' and 'time' columns are in datetime format
    finger_tapping_physio_df['unix_time'] = pd.to_datetime(finger_tapping_physio_df['unix_time'],
                                                           unit='s')
    finger_tapping_task_df['time'] = pd.to_datetime(finger_tapping_task_df['time'], unit='s')

    # Use merge_asof to merge the dataframes based on time, assigning the task data to the closest
    # physio data entry that is before it.
    merged_df = pd.merge_asof(finger_tapping_physio_df, finger_tapping_task_df,
                              left_on='unix_time', right_on='time', direction='backward',
                              suffixes=('_physio_data', '_task_data'))

    # Restore the original 'unix_time' column
    merged_df['unix_time'] = original_unix_time

    # Drop the 'time' column from the task data as it's redundant now
    merged_df = merged_df.drop(columns=['time'])

    # Set 'unix_time' back as the index
    merged_df = merged_df.set_index('unix_time')

    return merged_df


class FingerTapping:
    def __init__(self,
                 participant_ids: dict,
                 finger_tapping_task_df: pd.DataFrame,
                 finger_tapping_physio: pd.DataFrame,
                 finger_tapping_physio_task: pd.DataFrame
                 ):
        self.participant_ids = participant_ids
        self.finger_tapping_task_df = finger_tapping_task_df
        self.finger_tapping_physio = finger_tapping_physio
        self.finger_tapping_physio_task = finger_tapping_physio_task

    @classmethod
    def from_files(cls,
                   metadata_path: str,
                   finger_tapping_csv_path: str,
                   finger_tapping_physio_directory: str,
                   num_increments: int = 511):
        """
        Create a FingerTapping object from a metadata dictionary
        :param num_increments: number of time series increments
        :param finger_tapping_physio_directory: finger tapping physio directory
        :param finger_tapping_csv_path: finger tapping csv file path
        :param metadata_path: json file metadata path
        :return: FingerTapping object
        """
        # Read metadata
        metadata = read_json_file(metadata_path)
        participant_ids = metadata['participant_ids']

        # Read finger tapping task data
        finger_tapping_task_df = read_csv_file(finger_tapping_csv_path, delimiter=';')

        lion_finger_tapping_physio_csv_path = finger_tapping_physio_directory + '/lion/NIRS_filtered_finger_tapping.csv'
        tiger_finger_tapping_physio_csv_path = finger_tapping_physio_directory + '/tiger/NIRS_filtered_finger_tapping.csv'
        leopard_finger_tapping_physio_csv_path = finger_tapping_physio_directory + '/leopard/NIRS_filtered_finger_tapping.csv'

        finger_tapping_physio = {
            participant_ids['lion']: read_csv_file(lion_finger_tapping_physio_csv_path,
                                                   delimiter='\t'),
            participant_ids['tiger']: read_csv_file(tiger_finger_tapping_physio_csv_path,
                                                    delimiter='\t'),
            participant_ids['leopard']: read_csv_file(leopard_finger_tapping_physio_csv_path,
                                                      delimiter='\t'),
        }

        c

        finger_tapping_physio = combine_participants_physio(
            finger_tapping_physio,
            start_time,
            end_time,
            num_increments=num_increments
        )

        finger_tapping_physio_task = _combine_finger_tapping_physio_task(
            finger_tapping_task_df,
            finger_tapping_physio
        )

        return cls(
            participant_ids=participant_ids,
            finger_tapping_task_df=finger_tapping_task_df,
            finger_tapping_physio=finger_tapping_physio,
            finger_tapping_physio_task=finger_tapping_physio_task
        )

    def write_physio_data_csv(self, output_dir_path: str):
        """
        Write the physio data to a csv file in output directory
        :param output_dir_path: output directory path
        """
        # Create the directory if it doesn't exist
        if not os.path.exists(output_dir_path):
            os.makedirs(output_dir_path)

        self.finger_tapping_physio_task.to_csv(output_dir_path + '/finger_tapping_physio_task.csv',
                                               index=True)
