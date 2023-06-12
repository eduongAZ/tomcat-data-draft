import pandas as pd

from common import read_csv_file, read_json_file, iso_from_unix_time
from .synchronize_physio import synchronize_physio


def _get_start_end_time(task_df: pd.DataFrame) -> tuple[float, float]:
    start_time = task_df['time'].iloc[0]
    end_time = task_df['time'].iloc[-1]

    return start_time, end_time


def _combine_physio_task(task_df: pd.DataFrame,
                         physio_df: pd.DataFrame) -> pd.DataFrame:
    # Save the original 'unix_time' column
    original_unix_time = physio_df['unix_time'].copy()

    # Ensure that 'unix_time' and 'time' columns are in datetime format
    physio_df['unix_time'] = pd.to_datetime(physio_df['unix_time'],
                                            unit='s')
    task_df['time'] = pd.to_datetime(task_df['time'], unit='s')

    # Use merge_asof to merge the dataframes based on time, assigning the task data to the closest
    # physio data entry that is before it.
    merged_df = pd.merge_asof(physio_df, task_df,
                              left_on='unix_time', right_on='time', direction='backward',
                              suffixes=('_physio_data', '_task_data'))

    # Restore the original 'unix_time' column
    merged_df['unix_time'] = original_unix_time

    # Drop the 'time' column from the task data as it's redundant now
    merged_df = merged_df.drop(columns=['time'])

    # Drop columns
    merged_df = merged_df.drop(columns=['monotonic_time', 'human_readable_time'])

    return merged_df


def process_ping_pong_cooperative(exp_info_path: str,
                                  task_csv_path: str,
                                  physio_data: dict[str, any],
                                  frequency: float):
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
    combined_physio['lion_id'] = exp_info['participant_ids']['lion']
    combined_physio['tiger_id'] = exp_info['participant_ids']['tiger']
    combined_physio['leopard_id'] = exp_info['participant_ids']['leopard']

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

    return physio_task
