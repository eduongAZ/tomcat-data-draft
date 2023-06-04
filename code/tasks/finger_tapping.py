import os

import pandas as pd

from physio import combine_participants_physio_from_files
from utils import read_csv_file, read_json_file, iso_from_unix_time


def _combine_finger_tapping_physio_task(finger_tapping_task_df: pd.DataFrame,
                                        finger_tapping_physio_df: pd.DataFrame) -> pd.DataFrame:
    # Reset the index
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
                   finger_tapping_physio_name_filepath: dict[str, str],
                   frequency: float):
        """
        Create a FingerTapping object from a metadata dictionary
        :param frequency: frequency of the physio data
        :param finger_tapping_physio_name_filepath: finger tapping physio name-filepath mapping
        :param finger_tapping_csv_path: finger tapping csv file path
        :param metadata_path: json file metadata path
        :return: FingerTapping object
        """
        # Read metadata
        metadata = read_json_file(metadata_path)
        participant_ids = metadata['participant_ids']

        # Read finger tapping task data
        finger_tapping_task_df = read_csv_file(finger_tapping_csv_path, delimiter=';')

        start_time = finger_tapping_task_df['time'].iloc[0]
        end_time = finger_tapping_task_df['time'].iloc[-1]

        # Read finger tapping physio data
        physio_id_filepath = {v: finger_tapping_physio_name_filepath[k] for k, v in
                              participant_ids.items() if k in finger_tapping_physio_name_filepath}

        finger_tapping_physio = combine_participants_physio_from_files(
            physio_id_filepath,
            start_time,
            end_time,
            frequency
        )

        finger_tapping_physio = finger_tapping_physio.reset_index()
        finger_tapping_physio['experiment_id'] = metadata['experiment']
        finger_tapping_physio['lion_id'] = participant_ids['lion']
        finger_tapping_physio['tiger_id'] = participant_ids['tiger']
        finger_tapping_physio['leopard_id'] = participant_ids['leopard']

        finger_tapping_physio_task = _combine_finger_tapping_physio_task(
            finger_tapping_task_df,
            finger_tapping_physio
        )

        physio_task_start_time = finger_tapping_physio_task['unix_time'].iloc[0]
        finger_tapping_physio_task["seconds_since_start"] = \
            finger_tapping_physio_task["unix_time"] - physio_task_start_time

        finger_tapping_physio_task['human_readable_time'] = \
            iso_from_unix_time(finger_tapping_physio_task['unix_time'])

        finger_tapping_physio_task = finger_tapping_physio_task.set_index('unix_time')

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
