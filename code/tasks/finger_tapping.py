import os

import pandas as pd

from utils import read_csv_file
from utils import read_json_file


def _combine_finger_tapping_physio_task(finger_tapping_task_df: pd.DataFrame,
                                        finger_tapping_physio_csv_path: str,
                                        participant_id: str) -> pd.DataFrame:
    finger_tapping_physio_df = read_csv_file(finger_tapping_physio_csv_path, delimiter='\t')

    # Save the original 'unix_time' column
    original_unix_time = finger_tapping_physio_df['unix_time'].copy()

    # Ensure that 'unix_time' and 'time' columns are in datetime format
    finger_tapping_physio_df['unix_time'] = pd.to_datetime(finger_tapping_physio_df['unix_time'],
                                                           unit='s')
    finger_tapping_task_df['time'] = pd.to_datetime(finger_tapping_task_df['time'], unit='s')

    # Use merge_asof to merge the dataframes based on time
    merged_df = pd.merge_asof(finger_tapping_physio_df, finger_tapping_task_df,
                              left_on='unix_time', right_on='time', direction='backward',
                              suffixes=('_physio_data', '_task_data'))

    # Restore the original 'unix_time' column
    merged_df['unix_time'] = original_unix_time

    merged_df = merged_df.assign(participant_id=participant_id)

    # Drop the 'time' column from the task data as it's redundant now
    merged_df = merged_df.drop(columns=['time'])

    return merged_df


class FingerTapping:
    def __init__(self,
                 participant_ids: dict,
                 finger_tapping_task_df: pd.DataFrame,
                 finger_tapping_physio: dict[str, pd.DataFrame]
                 ):
        self.participant_ids = participant_ids
        self.finger_tapping_task_df = finger_tapping_task_df
        self.finger_tapping_physio = finger_tapping_physio

    @classmethod
    def from_files(cls,
                   metadata_path: str,
                   finger_tapping_csv_path: str,
                   finger_tapping_physio_directory: str):
        """
        Create a FingerTapping object from a metadata dictionary
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

        lion_physio_nirs_df = _combine_finger_tapping_physio_task(
            finger_tapping_task_df=finger_tapping_task_df,
            finger_tapping_physio_csv_path=finger_tapping_physio_directory + '/lion/NIRS_filtered_finger_tapping.csv',
            participant_id=participant_ids['lion'])

        tiger_physio_nirs_df = _combine_finger_tapping_physio_task(
            finger_tapping_task_df=finger_tapping_task_df,
            finger_tapping_physio_csv_path=finger_tapping_physio_directory + '/tiger/NIRS_filtered_finger_tapping.csv',
            participant_id=participant_ids['tiger'])

        leopard_physio_nirs_df = _combine_finger_tapping_physio_task(
            finger_tapping_task_df=finger_tapping_task_df,
            finger_tapping_physio_csv_path=finger_tapping_physio_directory + '/leopard/NIRS_filtered_finger_tapping.csv',
            participant_id=participant_ids['leopard'])

        return cls(
            participant_ids=participant_ids,
            finger_tapping_task_df=finger_tapping_task_df,
            finger_tapping_physio={
                'lion': lion_physio_nirs_df,
                'tiger': tiger_physio_nirs_df,
                'leopard': leopard_physio_nirs_df
            }
        )

    def write_physio_data_csv(self, output_dir_path: str):
        """
        Write the physio data to a csv file in output directory
        :param output_dir_path: output directory path
        """
        # Create the directory if it doesn't exist
        if not os.path.exists(output_dir_path):
            os.makedirs(output_dir_path)

        for participant, physio_df in self.finger_tapping_physio.items():
            output_dir_participant = output_dir_path + f'/{participant}'
            if not os.path.exists(output_dir_participant):
                os.makedirs(output_dir_participant)

            physio_df.to_csv(
                output_dir_participant + f'/{participant}_finger_tapping_physio_task.csv',
                index=False)
