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
    # Define the columns for the new dataframe
    columns = df.columns.drop(['Unnamed: 0', 'human_readable_time', 'unix_time', 'event_type'])
    synced_df = pd.DataFrame(columns=columns, index=time_series)

    df_start_time = df['unix_time'].min()  # Get the start time in the df

    for target_time in time_series:
        if target_time < df_start_time:  # Skip if target_time is less than start_time in df
            continue

        # Find the rows where the target time fits
        mask = (df['unix_time'] >= target_time)
        if mask.sum() == 0:
            break

        # Get the row before and after the target time
        after_target_row = df[mask].iloc[0]
        before_target_row = df[df['unix_time'] < target_time].iloc[-1]

        for column in columns:
            start_value = before_target_row[column]
            end_value = after_target_row[column]
            start_time = before_target_row['unix_time']
            end_time = after_target_row['unix_time']

            interpolated_value = linear_interpolation(
                start_time, end_time, target_time, start_value, end_value)

            synced_df.loc[target_time, column] = interpolated_value

    return synced_df


def combine_participants_physio(
        physio_df: dict[str, pd.DataFrame],
        start_time: float,
        end_time: float,
        num_increments: int) -> pd.DataFrame:
    """
    Combine physio data from multiple participants into one dataframe.
    :param physio_df: dictionary of participant id and physio dataframe
    :param start_time: start time
    :param end_time: end time
    :param num_increments: number of increments
    :return: combined physio dataframe
    """
    # Generate time series
    time_series = generate_time_series(start_time, end_time, num_increments)

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
