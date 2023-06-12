import pandas as pd

from common import read_csv_file
from .utils import generate_time_series


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
        sync_df[column] = interpolation_method(
            df_before['original_unix_time'],
            df_after['original_unix_time'],
            sync_df['unix_time'],
            df_before[column],
            df_after[column]
        )

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

    combined_df = None

    for physio_type, physio_type_data in physio_data.items():
        interpolation_method = physio_type_data['interpolation_method']

        for computer_name, physio_path in physio_type_data["name_path"].items():
            # Determine the delimiter
            with open(physio_path, 'r') as f:
                first_line = f.readline()
            if '\t' in first_line:
                delimiter = '\t'
            elif ',' in first_line:
                delimiter = ','
            elif ';' in first_line:
                delimiter = ';'
            else:
                raise ValueError('Delimiter could not be detected')

            physio_df = read_csv_file(physio_path, delimiter=delimiter)

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

            combined_df.index.name = 'unix_time'

    return combined_df
