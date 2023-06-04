import os
from bisect import bisect_right

import numpy as np
import pandas as pd

from physio import combine_participants_physio_from_files
from utils import read_csv_file, read_json_file, iso_from_unix_time, rename_column_id_computer


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


class AffectiveTaskTeam:
    def __init__(self,
                 participant_ids: dict,
                 affective_task_team_df: pd.DataFrame,
                 affective_task_team_physio: pd.DataFrame,
                 affective_task_team_physio_task: pd.DataFrame):
        self.participant_ids = participant_ids
        self.affective_task_team_df = affective_task_team_df
        self.affective_task_team_physio = affective_task_team_physio
        self.affective_task_team_physio_task = affective_task_team_physio_task

    @classmethod
    def from_files(cls,
                   metadata_path: str,
                   affective_task_team_csv_path: str,
                   affective_team_physio_name_filepath: dict[str, str],
                   frequency: float):
        """
        Create an AffectiveTaskTeam object from a metadata dictionary
        :param frequency: frequency of the data
        :param affective_team_physio_name_filepath: affective task team physio name-filepath mapping
        :param affective_task_team_csv_path: affective task team csv file path
        :param metadata_path: json file metadata path
        :return: AffectiveTaskTeam object
        """
        # Read metadata
        metadata = read_json_file(metadata_path)
        participant_ids = metadata['participant_ids']
        id_computer = {value: key for key, value in participant_ids.items()}

        # Read affective task team data
        affective_task_team_df = read_csv_file(affective_task_team_csv_path, delimiter=';')

        start_time = affective_task_team_df['time'].iloc[0]
        end_time = affective_task_team_df['time'].iloc[-1]

        # Read affective task team physio data
        physio_id_filepath = {v: affective_team_physio_name_filepath[k] for k, v in
                              participant_ids.items() if k in affective_team_physio_name_filepath}

        affective_team_physio = combine_participants_physio_from_files(
            physio_id_filepath,
            start_time,
            end_time,
            frequency
        )

        affective_team_physio = affective_team_physio.reset_index()

        affective_team_physio['experiment_id'] = metadata['experiment']
        affective_team_physio['lion_id'] = participant_ids['lion']
        affective_team_physio['tiger_id'] = participant_ids['tiger']
        affective_team_physio['leopard_id'] = participant_ids['leopard']

        affective_team_physio_task = _combine_affective_physio_task(
            affective_task_team_df,
            affective_team_physio
        )

        physio_task_start_time = affective_team_physio_task['unix_time'].iloc[0]
        affective_team_physio_task["seconds_since_start"] = \
            affective_team_physio_task["unix_time"] - physio_task_start_time

        affective_team_physio_task['human_readable_time'] = \
            iso_from_unix_time(affective_team_physio_task['unix_time'])

        affective_team_physio_task = rename_column_id_computer(affective_team_physio_task,
                                                               id_computer)

        affective_team_physio_task = affective_team_physio_task.set_index('unix_time')

        return cls(
            participant_ids=participant_ids,
            affective_task_team_df=affective_task_team_df,
            affective_task_team_physio=affective_team_physio,
            affective_task_team_physio_task=affective_team_physio_task
        )

    def write_physio_data_csv(self, output_dir_path: str):
        """
        Write the physio data to a csv file in output directory
        :param output_dir_path: output directory path
        """
        # Create the directory if it doesn't exist
        if not os.path.exists(output_dir_path):
            os.makedirs(output_dir_path)

        self.affective_task_team_physio_task.to_csv(
            output_dir_path + '/affective_task_team_physio_task.csv', index=True)
