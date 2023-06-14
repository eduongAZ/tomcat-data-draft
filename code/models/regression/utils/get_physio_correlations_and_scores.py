import itertools

from common import read_csv_file
from .compute_correlation import compute_correlation


def get_physio_correlations_and_scores(
        physio_task_file_paths: list[str],
        channels: list[str],
        score_column_name: str,
        remove_nan: bool = False) -> tuple[dict[str, list[float]], list[float]]:
    """
    Get the correlations and scores for each channel in each experiment
    @param physio_task_file_paths: The paths to the physio task files
    @param channels: The channels to compute correlations for
    @param score_column_name: The name of the column containing the scores
    @param remove_nan: Whether to remove rows with NaN values in any of the correlated channels
    @return: The correlations and scores for each channel in each experiment
    """
    correlation_per_channel = {channel: [] for channel in channels}
    scores = []

    # Iterate over all the physio task files
    for physio_task_file_path in physio_task_file_paths:  # one per experiment
        # Read the physio task file
        physio_task_df = read_csv_file(physio_task_file_path)

        # Get physio channel columns
        physio_channel_columns = [col for col in physio_task_df.columns if
                                  any(sub_string in col for sub_string in channels)]

        # Continue if there are no physio channel columns
        if not physio_channel_columns:
            continue

        # Drop rows with NaN values in any of the physio channel columns
        physio_task_df = physio_task_df.dropna(subset=physio_channel_columns)

        # Continue if there are no rows left
        if len(physio_task_df) < 2:
            continue

        # Compute correlations
        for channel in channels:
            computers = ["lion", "tiger", "leopard"]

            # Get pairs of computers: lion-tiger, lion-leopard, tiger-leopard
            combinations = itertools.combinations(computers, 2)

            physio_correlations = []
            for computer1, computer2 in combinations:
                if f"{computer1}_{channel}" in physio_task_df.columns and \
                        f"{computer2}_{channel}" in physio_task_df.columns:
                    corr = compute_correlation(physio_task_df[f"{computer1}_{channel}"],
                                               physio_task_df[f"{computer2}_{channel}"])
                    physio_correlations.append(corr)

            # Compute average correlation for the channel by the number of pairs of computers
            average_corr = None if not physio_correlations \
                else sum(physio_correlations) / len(physio_correlations)

            # Add average correlation to the list of correlations for the channel
            correlation_per_channel[channel].append(average_corr)

        # Get score
        scores.append(physio_task_df[score_column_name].values[-1])

    # Remove NaN values across all channels if a channel has a NaN value
    if remove_nan:
        # Identify indices of rows with NaN values in any of the channels
        indices_to_remove = []
        for channel in channels:
            indices_to_remove += [i for i, x in enumerate(correlation_per_channel[channel]) if
                                  x is None]
        indices_to_remove = list(set(indices_to_remove))

        # Remove rows with NaN values in any of the channels
        for channel in channels:
            correlation_per_channel[channel] = [x for i, x in
                                                enumerate(correlation_per_channel[channel])
                                                if i not in indices_to_remove]
        scores = [x for i, x in enumerate(scores) if i not in indices_to_remove]

    return correlation_per_channel, scores
