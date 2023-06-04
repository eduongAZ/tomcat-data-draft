import numpy as np


# def generate_time_series(start_time: float,
#                          end_time: float,
#                          num_increments: int):
#     return np.linspace(start_time, end_time, num_increments)

def generate_time_series(start_time: float,
                         end_time: float,
                         frequency: float):
    period = 1.0 / frequency
    return np.arange(start_time, end_time + period, period)
