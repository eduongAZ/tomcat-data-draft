import numpy as np
import pandas as pd

from interpolation import linear_interpolation
from process.synchronize_physio.synchronize_physio import _get_entries_after_each_time_series
from process.synchronize_physio.synchronize_physio import _get_entries_before_each_time_series
from process.synchronize_physio.synchronize_physio import _sync_data_to_time_series


def test_get_entries_before_each_time_series():
    df = pd.DataFrame({
        'unix_time': [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0],
        'val': ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    })

    sync_df = pd.DataFrame({
        'unix_time': [15.0, 35.0, 55.0, 75.0]
    })

    df_before = _get_entries_before_each_time_series(df, sync_df)

    assert isinstance(df_before, pd.DataFrame), "Output should be a pandas DataFrame"

    # The df_before dataframe should have the same length as sync_df
    assert len(df_before) == len(sync_df), "Output DataFrame length should match the sync_df length"

    # Check that the 'val' column contains the values from entries before each time series
    assert list(df_before['val']) == ['a', 'c', 'e', 'g'], "Values are not as expected"

    # Check the 'unix_time' column contains the correct values as the sync_df
    assert list(df_before['unix_time']) == list(sync_df['unix_time']), "unix_time values are not as expected"


def test_get_entries_after_each_time_series():
    df = pd.DataFrame({
        'unix_time': [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0],
        'val': ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    })

    sync_df = pd.DataFrame({
        'unix_time': [15.0, 35.0, 55.0, 75.0]
    })

    df_after = _get_entries_after_each_time_series(df, sync_df)

    assert isinstance(df_after, pd.DataFrame), "Output should be a pandas DataFrame"

    # The df_after dataframe should have the same length as sync_df
    assert len(df_after) == len(sync_df), "Output DataFrame length should match the sync_df length"

    # Check that the 'val' column contains the values from entries before each time series
    assert list(df_after['val']) == ['b', 'd', 'f', np.nan], "Values are not as expected"

    # Check the 'unix_time' column contains the correct values as the sync_df
    assert list(df_after['unix_time']) == list(sync_df['unix_time']), "unix_time values are not as expected"


def test_sync_data_to_time_series_linear_interpolation():
    # Create sample Dataframe and time series
    df = pd.DataFrame({
        'unix_time': [1000.0, 1005.0, 1010.0, 1015.0],
        'val1': [1.0, 2.0, 3.0, 4.0],
        'val2': [5.0, 6.0, 7.0, 8.0],
        'event_type': ['a', 'b', 'c', 'd']
    })
    time_series = [1001.0, 1007.5, 1014.0]

    # Test with linear interpolation
    result = _sync_data_to_time_series(df, time_series, linear_interpolation)

    # Check that the result is a pandas DataFrame
    assert isinstance(result, pd.DataFrame), "Output should be a pandas DataFrame"

    # Check that the resulting Dataframe has the same unix_time as the input time series
    assert list(result.index) == time_series, "Index should match the input time series"

    # Check that the resulting Dataframe has correct values from linear interpolation
    expected_result = pd.DataFrame({
        'val1': [1.2, 2.5, 3.8],
        'val2': [5.2, 6.5, 7.8]
    }, index=time_series)
    expected_result.index.name = 'unix_time'

    pd.testing.assert_frame_equal(result, expected_result)
