from common import find_files
from .utils import get_physio_correlations_and_scores, linear_fit, plot_regression_per_channel


def regression(physio_task_dir: str,
               physio_task_file_name: str,
               score_column_name: str,
               channels: list[str],
               output_img_dir: str | None = None,
               output_file_path: str | None = None,
               absolute_value_correlations: bool = False,
               blacklist_experiments: list[str] | None = None):
    exp_files = find_files(physio_task_dir, physio_task_file_name)

    if blacklist_experiments is not None:
        exp_files = {k: v for k, v in exp_files.items() if k not in blacklist_experiments}

    correlation_per_channel, scores = get_physio_correlations_and_scores(
        list(exp_files.values()),
        channels,
        score_column_name,
        remove_nan=True)

    predictions_per_channel, \
        rmse_per_channel, \
        linear_regressor_per_channel, \
        r2_per_channel, \
        null_model_r2, \
        linear_regression_slope_per_channel = \
        linear_fit(
            correlation_per_channel,
            scores,
            output_file_path,
            absolute_value_correlations)

    if output_img_dir is not None:
        plot_regression_per_channel(
            correlation_per_channel,
            scores,
            linear_regressor_per_channel,
            output_img_dir)

    return predictions_per_channel, \
        rmse_per_channel, \
        linear_regressor_per_channel, \
        r2_per_channel, \
        null_model_r2, \
        linear_regression_slope_per_channel
