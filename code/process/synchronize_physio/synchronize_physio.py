import pandas as pd

from common import read_csv_file
from .utils import generate_time_series


def _get_entries_before_each_time_series(df: pd.DataFrame,
                                         sync_df: pd.DataFrame) -> pd.DataFrame:
    """
    Get the entries before each time series.
    @param df: dataframe of physio data
    @param sync_df: dataframe with the target time series
    @return: dataframe of entries before each time series
    """
    return pd.merge_asof(sync_df, df, on='unix_time', direction='backward')


def _get_entries_after_each_time_series(df: pd.DataFrame,
                                        sync_df: pd.DataFrame) -> pd.DataFrame:
    """
    Get the entries after each time series.
    @param df: dataframe of physio data
    @param sync_df: dataframe with the target time series
    @return: dataframe of entries after each time series
    """
    return pd.merge_asof(sync_df, df, on='unix_time', direction='forward')


def _sync_data_to_time_series(df: pd.DataFrame,
                              time_series: list[float],
                              interpolation_method: callable) -> pd.DataFrame:
    """
    Syncs a dataframe to a given time series.
    @param df: dataframe of physio data
    @param time_series: time series to synchronize to
    @param interpolation_method: interpolation method to use
    @return: dataframe of physio data synchronized to time series
    """
    # Create a dataframe for synchronized data
    sync_df = pd.DataFrame(time_series, columns=['unix_time'])

    # Remember the original unix_time column before removing it later
    df['original_unix_time'] = df['unix_time'].copy()

    # Find the nearest entry at or before each time
    df_before = _get_entries_before_each_time_series(df, sync_df)

    # Find the nearest entry at or after each time
    df_after = _get_entries_after_each_time_series(df, sync_df)

    # Drop old, unwanted columns from the dataframes
    columns_to_drop = ['Unnamed: 0', 'human_readable_time', 'unix_time', 'event_type', 'original_unix_time']
    columns_to_drop = [col for col in columns_to_drop if col in df.columns]
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop)

    # Interpolate each column
    for column in df.columns:
        sync_df[column] = interpolation_method(
            df_before['original_unix_time'],
            df_after['original_unix_time'],
            sync_df['unix_time'],
            df_before[column],
            df_after[column]
        )

    # Set the index to unix_time
    sync_df = sync_df.set_index('unix_time')

    return sync_df


def synchronize_physio(physio_data: dict[str, any],
                       start_time: float,
                       end_time: float,
                       frequency: float) -> pd.DataFrame:
    # Generate time series
    time_series = generate_time_series(start_time, end_time, frequency)

    # If physio_df is empty, return combined_df with unix_time as index
    if not physio_data:
        return pd.DataFrame(index=time_series).rename_axis('unix_time')

    # Synchronize each physio dataframe to the time series
    combined_df = None
    for physio_type, physio_type_data in physio_data.items():
        interpolation_method = physio_type_data['interpolation_method']

        # Synchronize each physio dataframe to the time series
        for computer_name, physio_path in physio_type_data["name_path"].items():
            # Read the physio data from the csv file
            physio_df = read_csv_file(physio_path, delimiter=';')

            # Synchronize the data to the time series
            synchronized_physio_df = _sync_data_to_time_series(physio_df, time_series, interpolation_method)

            # Prefix the column names with the computer name
            synchronized_physio_df.columns = [
                f'{computer_name}_{physio_type}_{col}' for col in synchronized_physio_df.columns
            ]

            # Concatenate the dataframes
            if combined_df is None:
                combined_df = synchronized_physio_df
            else:
                combined_df = pd.concat([combined_df, synchronized_physio_df], axis=1)

            # Set the index name to unix_time
            combined_df.index.name = 'unix_time'

    return combined_df
