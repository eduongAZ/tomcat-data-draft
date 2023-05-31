import numpy as np


def generate_time_series(start_time: float,
                         end_time: float,
                         num_increments: int):
    return np.linspace(start_time, end_time, num_increments)
