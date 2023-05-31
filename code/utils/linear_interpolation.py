from .linear_average import linear_average


def linear_interpolation(
        start_time: float,
        end_time: float,
        target_time: float,
        start_value: float,
        end_value: float) -> float:
    """
    Performs linear interpolation between two values based on a given target time.
    :param start_time: start time
    :param end_time: end time
    :param target_time: target time
    :param start_value: start value
    :param end_value: end value
    :return: linear interpolated value
    """
    if not (start_time <= target_time <= end_time):
        raise ValueError("Target time must be between start and end time.")

    percentage = (target_time - start_time) / (end_time - start_time)
    return linear_average(start_value, end_value, percentage)
