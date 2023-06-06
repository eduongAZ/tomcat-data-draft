import pandas as pd

from utils import linear_interpolation
from .utils import generate_time_series


def _sync_data_to_time_series(df: pd.DataFrame, time_series: list[float]) -> pd.DataFrame:
    """
    Syncs a dataframe to a given time series.
    :param df: pandas dataframe of physio data
    :param time_series: time series to synchronize to
    :return: physio data synchronized to time series
    """
    sync_df = pd.DataFrame(time_series, columns=['unix_time'])

    df['original_unix_time'] = df['unix_time'].copy()

    # merge_asof to find the nearest entry at or before each time
    df_before = pd.merge_asof(sync_df, df, on='unix_time', direction='backward')

    # merge_asof to find the nearest entry at or after each time
    df_after = pd.merge_asof(sync_df, df, on='unix_time', direction='forward')

    # Drop column Unnamed: 0 if it exists
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    columns = df.columns.drop(['human_readable_time',
                               'unix_time',
                               'event_type',
                               'original_unix_time'])
    for column in columns:
        sync_df[column] = linear_interpolation(
            df_before['original_unix_time'],
            df_after['original_unix_time'],
            sync_df['unix_time'],
            df_before[column],
            df_after[column]
        )

    sync_df = sync_df.set_index('unix_time')

    return sync_df


def combine_participants_physio(
        physio_df: dict[str, pd.DataFrame],
        start_time: float,
        end_time: float,
        frequency: float) -> pd.DataFrame:
    """
    Combine physio data from multiple participants into one dataframe.
    :param physio_df: dictionary of participant id and physio dataframe
    :param start_time: start time
    :param end_time: end time
    :param frequency: time series frequency
    :return: combined physio dataframe
    """
    # Generate time series
    time_series = generate_time_series(start_time, end_time, frequency)

    # If physio_df is empty, return combined_df with unix_time as index
    if not physio_df:
        return pd.DataFrame(index=time_series).rename_axis('unix_time')

    combined_df = None

    for participant_id, df in physio_df.items():
        # Sync the dataframe to the shared time series
        synced_df = _sync_data_to_time_series(df, time_series)

        # Prefix the column names with the participant id
        synced_df.columns = [f'{participant_id}_{col}' for col in synced_df.columns]

        # Concatenate the dataframes
        if combined_df is None:
            combined_df = synced_df
        else:
            combined_df = pd.concat([combined_df, synced_df], axis=1)

        combined_df.index.name = 'unix_time'

    return combined_df
