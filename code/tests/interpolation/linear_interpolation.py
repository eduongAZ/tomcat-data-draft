from interpolation import linear_interpolation

import numpy as np


def test_linear_interpolation_floats():
    start_time = 0.0
    end_time = 10.0
    target_time = 5.0

    start_value = 1.0
    end_value = 2.0

    assert np.isclose(linear_interpolation(start_time, end_time, target_time, start_value, end_value), 1.5)


def test_linear_interpolation_numpy():
    start_time = np.array([0.0, 11.0, 22.0])
    end_time = np.array([10.0, 21.0, 32.0])
    target_time = np.array([5.0, 16.0, 27.0])

    start_value = np.array([1.0, 2.0, 3.0])
    end_value = np.array([2.0, 3.0, 4.0])

    expected_results = np.array([1.5, 2.5, 3.5])

    np.testing.assert_allclose(linear_interpolation(start_time, end_time, target_time, start_value, end_value),
                               expected_results)
