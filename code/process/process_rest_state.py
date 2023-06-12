import pandas as pd

from common import read_csv_file, read_json_file, iso_from_unix_time
from .synchronize_physio import synchronize_physio


def _get_start_end_time(task_df: pd.DataFrame) -> tuple[float, float]:
    start_time = task_df.query('event_type == "start_rest_state"').iloc[0]['time']
    end_time = task_df.query('event_type == "end_rest_state"').iloc[0]['time']

    return start_time, end_time


def _combine_physio_task(task_df: pd.DataFrame,
                         physio_df: pd.DataFrame) -> pd.DataFrame:
    start_time, end_time = _get_start_end_time(task_df)

    def _assign_event_type(row):
        if start_time <= row["unix_time"] <= end_time:
            return 'during_rest_state'
        else:
            return 'outside_of_rest_state'

    physio_df['task_status'] = physio_df.apply(_assign_event_type, axis=1)

    return physio_df


def process_rest_state(exp_info_path: str,
                       task_csv_path: str,
                       physio_data: dict[str, any],
                       frequency: float) -> tuple[any, bool, str]:
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

    return physio_task, True, "Processed rest state data"
