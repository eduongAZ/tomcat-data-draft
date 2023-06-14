from common import find_files
from .utils import get_physio_correlations_and_scores, linear_fit, plot_regression_per_channel


def regression(physio_task_dir: str,
               physio_task_file_name: str,
               score_column_name: str,
               channels: list[str],
               output_img_dir: str | None = None,
               show_plots: bool = True,
               output_file_path: str | None = None,
               absolute_value_correlations: bool = False,
               blacklist_experiments: list[str] | None = None):
    """
    Perform linear regression for each channel vs score for all experiments
    @param physio_task_dir: The directory containing the physio task files
    @param physio_task_file_name: The name of the physio task file
    @param score_column_name: The name of the column containing the scores
    @param channels: The channels to perform regression on
    @param output_img_dir: The directory to save the regression plots to
    @param show_plots: Whether to show the regression plots
    @param output_file_path: The file to save the regression results to
    @param absolute_value_correlations: Whether to take the absolute value of the correlations before linear regression
    @param blacklist_experiments: The experiments to exclude from the regression
    @return: The predictions, RMSE, linear regressor, R2, null model R2, and linear regression slope for each channel
    """
    # Find all the files in the physio_task_dir that match the physio_task_file_name in all experiments
    exp_files = find_files(physio_task_dir, physio_task_file_name)

    # Remove the experiments that are in the blacklist
    if blacklist_experiments is not None:
        exp_files = {k: v for k, v in exp_files.items() if k not in blacklist_experiments}

    # Get the correlations and scores for each channel in each experiment
    correlation_per_channel, scores = get_physio_correlations_and_scores(
        list(exp_files.values()),
        channels,
        score_column_name,
        remove_nan=True
    )

    # Perform linear regression for each channel vs score
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

    # Plot the regression results
    if output_img_dir is not None:
        plot_regression_per_channel(
            correlation_per_channel,
            scores,
            linear_regressor_per_channel,
            output_img_dir,
            show_plots)

    return predictions_per_channel, \
        rmse_per_channel, \
        linear_regressor_per_channel, \
        r2_per_channel, \
        null_model_r2, \
        linear_regression_slope_per_channel
