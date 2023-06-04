import os
from bisect import bisect_right

import numpy as np
import pandas as pd

from physio import combine_participants_physio_from_files
from utils import read_csv_file, iso_from_unix_time


def _combine_affective_physio_task(affective_task_df: pd.DataFrame,
                                   affective_physio_df: pd.DataFrame) -> pd.DataFrame:
    # Reset the index
    affective_task_df = affective_task_df.reset_index()

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

    return affective_physio_df


class AffectiveTaskIndividual:
    def __init__(self,
                 participant_id: str,
                 participant_name: str,
                 affective_task_df: pd.DataFrame,
                 affective_physio_df: pd.DataFrame,
                 affective_physio_task_df: pd.DataFrame):
        self.participant_id = participant_id
        self.participant_name = participant_name
        self.affective_task_df = affective_task_df
        self.affective_physio_df = affective_physio_df
        self.affective_physio_task_df = affective_physio_task_df

    @classmethod
    def from_files(cls,
                   experiment_id: str,
                   participant_id: str,
                   participant_name: str,
                   affective_task_csv_path: str,
                   affective_physio_path: str,
                   frequency: float):
        """
        Create an AffectiveTask object from a metadata dictionary
        :param experiment_id: ID of experiment
        :param participant_id: id number of participant
        :param participant_name: name of participant computer (lion, tiger, leopard)
        :param affective_physio_path: affective task physio path
        :param affective_task_csv_path: affective task csv file path
        :param frequency: frequency of the physio data
        :return: AffectiveTask object
        """
        # Read affective task data
        affective_task_df = read_csv_file(affective_task_csv_path, delimiter=';')

        start_time = affective_task_df['time'].iloc[0]
        end_time = affective_task_df['time'].iloc[-1]

        # Read finger tapping physio data
        physio_id_filepath = {participant_id: affective_physio_path}

        affective_individual_physio = combine_participants_physio_from_files(
            physio_id_filepath,
            start_time,
            end_time,
            frequency
        )

        affective_individual_physio = affective_individual_physio.reset_index()

        affective_individual_physio['experiment_id'] = experiment_id
        affective_individual_physio[participant_name] = participant_id

        affective_individual_physio_task = _combine_affective_physio_task(
            affective_task_df,
            affective_individual_physio
        )

        physio_task_start_time = affective_individual_physio_task['unix_time'].iloc[0]
        affective_individual_physio_task["seconds_since_start"] = \
            affective_individual_physio_task["unix_time"] - physio_task_start_time

        affective_individual_physio_task['human_readable_time'] = \
            iso_from_unix_time(affective_individual_physio_task['unix_time'])

        affective_individual_physio_task = affective_individual_physio_task.set_index('unix_time')

        return cls(
            participant_id=participant_id,
            participant_name=participant_name,
            affective_task_df=affective_task_df,
            affective_physio_df=affective_individual_physio,
            affective_physio_task_df=affective_individual_physio_task
        )

    def write_physio_data_csv(self, output_dir_path: str):
        """
        Write the physio data to a csv file in the output directory
        :param output_dir_path: output directory path
        """
        # Create the directory if it doesn't exist
        if not os.path.exists(output_dir_path):
            os.makedirs(output_dir_path)

        self.affective_physio_task_df.to_csv(
            output_dir_path + f'/{self.participant_name}_affective_individual_physio_task.csv',
            index=True)
