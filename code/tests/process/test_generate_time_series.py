import numpy as np

from process.synchronize_physio.utils.generate_time_series import generate_time_series


def test_generate_time_series():
    start_time = 0.0
    end_time = 1.0
    frequency = 10.0

    result = generate_time_series(start_time, end_time, frequency)
    expected = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

    # Test whether result matches the expected value within a tolerance
    assert np.allclose(result, expected)
