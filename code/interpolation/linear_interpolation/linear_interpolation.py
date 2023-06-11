from .utils import linear_average


def linear_interpolation(start_time_unix: any,
                         end_time_unix: any,
                         target_time_unix: any,
                         start_value: any,
                         end_value: any) -> any:
    """
    Performs linear interpolation between two values based on a given target time.
    @param start_time_unix: start time
    @param end_time_unix: end time
    @param target_time_unix: target time
    @param start_value: start value (percentage = 0)
    @param end_value: end value (percentage = 1)
    @return: linear interpolated value
    """
    percentage = (target_time_unix - start_time_unix) / (end_time_unix - start_time_unix)
    return linear_average(start_value, end_value, percentage)
