from utils import find_files
from .utils import get_physio_correlations_and_scores, linear_fit, plot_regression_per_channel


def regression(physio_task_dir: str,
               physio_task_file_name: str,
               score_column_name: str,
               channels: list[str],
               output_dir: str):
    exp_files = find_files(physio_task_dir, physio_task_file_name)
    correlation_per_channel, scores = get_physio_correlations_and_scores(
        exp_files.values(),
        channels,
        score_column_name,
        remove_nan=True)

    predictions_per_channel, rmse_per_channel, linear_regressor_per_channel = linear_fit(
        correlation_per_channel, scores)

    print(rmse_per_channel)

    plot_regression_per_channel(
        correlation_per_channel,
        scores,
        linear_regressor_per_channel,
        output_dir)
