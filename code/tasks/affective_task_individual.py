import os
from bisect import bisect_right

import numpy as np
import pandas as pd

from utils import read_csv_file


def _combine_affective_physio_task(affective_task_df: pd.DataFrame,
                                   affective_physio_csv_path: str,
                                   participant_id: str) -> pd.DataFrame:
    affective_physio_df = read_csv_file(affective_physio_csv_path, delimiter='\t')

    # Save the original 'unix_time' column
    original_unix_time = affective_physio_df['unix_time'].copy()

    # Ensure that 'unix_time' and 'time' columns are in datetime format
    affective_physio_df['unix_time'] = pd.to_datetime(affective_physio_df['unix_time'], unit='s')
    affective_task_df['time'] = pd.to_datetime(affective_task_df['time'], unit='s')

    # Sort both dataframes by time
    affective_physio_df = affective_physio_df.sort_values(by='unix_time')
    affective_task_df = affective_task_df.sort_values(by='time')

    # Get the 'unix_time' values as a list for binary search
    unix_times = affective_physio_df['unix_time'].tolist()

    # Rename columns to avoid duplicates
    affective_task_df.columns = ['task_' + col for col in affective_task_df.columns]

    # Initialize new columns in the brain data and set as NaN
    for col in affective_task_df.columns:
        affective_physio_df[col] = np.nan

    for i, row in affective_task_df.iterrows():
        # Find the index of the closest brain data entry which is before the current task data
        idx = bisect_right(unix_times, row['task_time']) - 1

        if idx >= 0:
            # Assign the task data to this brain data entry
            for col in affective_task_df.columns:
                affective_physio_df.loc[affective_physio_df.index[idx], col] = row[col]

    # Restore the original 'unix_time' column
    affective_physio_df['unix_time'] = original_unix_time

    affective_physio_df = affective_physio_df.assign(physio_participant_id=participant_id)

    return affective_physio_df


class AffectiveTaskIndividual:
    def __init__(self,
                 participant_id: str,
                 participant_name: str,
                 affective_task_df: pd.DataFrame,
                 affective_physio_df: pd.DataFrame):
        self.participant_id = participant_id
        self.participant_name = participant_name
        self.affective_task_df = affective_task_df
        self.affective_physio_df = affective_physio_df

    @classmethod
    def from_files(cls,
                   participant_id: str,
                   participant_name: str,
                   affective_task_csv_path: str,
                   affective_physio_directory: str):
        """
        Create an AffectiveTask object from a metadata dictionary
        :param participant_id: id number of participant
        :param participant_name: name of participant computer (lion, tiger, leopard)
        :param affective_physio_directory: affective task physio directory
        :param affective_task_csv_path: affective task csv file path
        :return: AffectiveTask object
        """
        # Read affective task data
        affective_task_df = read_csv_file(affective_task_csv_path, delimiter=';')

        physio_df = _combine_affective_physio_task(
            affective_task_df=affective_task_df,
            affective_physio_csv_path=affective_physio_directory + '/NIRS_filtered_affective_task_individual.csv',
            participant_id=participant_id)

        return cls(
            participant_id=participant_id,
            participant_name=participant_name,
            affective_task_df=affective_task_df,
            affective_physio_df=physio_df
        )

    def write_physio_data_csv(self, output_dir_path: str):
        """
        Write the physio data to a csv file in the output directory
        :param output_dir_path: output directory path
        """
        # Create the directory if it doesn't exist
        if not os.path.exists(output_dir_path):
            os.makedirs(output_dir_path)

        output_dir_participant = output_dir_path + f'/{self.participant_name}'
        if not os.path.exists(output_dir_participant):
            os.makedirs(output_dir_participant)

        self.affective_physio_df.to_csv(
            output_dir_participant + f'/{self.participant_name}_affective_individual_physio_task.csv',
            index=False)
