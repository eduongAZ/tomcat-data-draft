def linear_average(
        value1: float,
        value2: float,
        percentage: float) -> float:
    """
    Performs linear averaging between two values based on a given percentage.

    Arguments:
    value1 -- The first value.
    value2 -- The second value.
    percentage -- The percentage (between 0 and 1) determining the weight of the second value.

    Returns:
    The linearly averaged value.
    """
    if not (0 <= percentage <= 1):
        raise ValueError("Percentage must be between 0 and 1.")

    return value1 * (1 - percentage) + value2 * percentage
