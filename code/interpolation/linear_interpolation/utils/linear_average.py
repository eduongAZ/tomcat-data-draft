def linear_average(value1: any, value2: any, percentage: any) -> any:
    """
    Linear average between two values
    @param value1: first value (percentage = 0)
    @param value2: second value (percentage = 1)
    @param percentage: percentage of the second value
    @return: linear average between value1 and value2
    """
    return value1 * (1.0 - percentage) + value2 * percentage
