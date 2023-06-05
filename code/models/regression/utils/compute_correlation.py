from scipy.stats import pearsonr


def compute_correlation(x_values, y_values) -> float:
    return pearsonr(x_values, y_values).correlation
