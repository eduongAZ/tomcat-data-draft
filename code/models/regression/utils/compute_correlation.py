from scipy.stats import pearsonr


def compute_correlation(x_values, y_values) -> float:
    """
    Compute the correlation between two lists of values.
    @param x_values: x value array
    @param y_values: y value array
    @return: correlation between x and y values
    """
    return pearsonr(x_values, y_values).correlation
