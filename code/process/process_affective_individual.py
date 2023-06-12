from bisect import bisect_right

import numpy as np
import pandas as pd

from common import read_csv_file, read_json_file, iso_from_unix_time
from .synchronize_physio import synchronize_physio


def _get_start_end_time(task_df: pd.DataFrame) -> tuple[float, float]:
    start_time = task_df['time'].iloc[0]
    end_time = task_df['time'].iloc[-1]

    return start_time, end_time


def _combine_physio_task(task_df: pd.DataFrame,
                         physio_df: pd.DataFrame) -> pd.DataFrame:
    # Reset the index
    task_df = task_df.reset_index()

    # Save the original 'unix_time' column
    original_unix_time = physio_df['unix_time'].copy()

    # Ensure that 'unix_time' and 'time' columns are in datetime format
    physio_df['unix_time'] = pd.to_datetime(physio_df['unix_time'], unit='s')
    task_df['time'] = pd.to_datetime(task_df['time'], unit='s')

    # Sort both dataframes by time
    physio_df = physio_df.sort_values(by='unix_time')
    task_df = task_df.sort_values(by='time')

    # Get the 'unix_time' values as a list for binary search
    unix_times = physio_df['unix_time'].tolist()

    # Rename columns to avoid duplicates
    task_df.columns = ['task_' + col for col in task_df.columns]

    # Initialize new columns in the brain data and set as NaN
    for col in task_df.columns:
        physio_df[col] = np.nan

    for i, row in task_df.iterrows():
        # Find the index of the closest brain data entry which is before the current task data
        idx = bisect_right(unix_times, row['task_time']) - 1

        if idx >= 0:
            # Assign the task data to this brain data entry
            for col in task_df.columns:
                physio_df.loc[physio_df.index[idx], col] = row[col]

    # Restore the original 'unix_time' column
    physio_df['unix_time'] = original_unix_time

    return physio_df


def process_affective_individual(exp_info_path: str,
                                 task_csv_path: str,
                                 physio_data: dict[str, any],
                                 frequency: float,
                                 computer_name: str,
                                 participant_id: str) -> tuple[any, bool, str]:
    # Read task data
    task_df = read_csv_file(task_csv_path, delimiter=';')

    # Detect if there is a column called lsl_timestamp. If so, remove the existing time column
    # and rename the lsl_timestamp column to time
    if 'lsl_timestamp' in task_df.columns:
        task_df = task_df.drop(columns=['time'])
        task_df = task_df.rename(columns={'lsl_timestamp': 'time'})

    start_time, end_time = _get_start_end_time(task_df)

    combined_physio = synchronize_physio(physio_data, start_time, end_time, frequency)

    combined_physio = combined_physio.reset_index()

    exp_info = read_json_file(exp_info_path)
    combined_physio['experiment_id'] = exp_info['experiment']
    combined_physio[f'{computer_name}_id'] = participant_id

    physio_task = _combine_physio_task(
        task_df,
        combined_physio
    )

    physio_task_start_time = physio_task['unix_time'].iloc[0]
    physio_task["seconds_since_start"] = \
        physio_task["unix_time"] - physio_task_start_time

    physio_task['human_readable_time'] = \
        iso_from_unix_time(physio_task['unix_time'])

    physio_task = physio_task.set_index('unix_time')

    return physio_task, True, "Processed affective individual data"
