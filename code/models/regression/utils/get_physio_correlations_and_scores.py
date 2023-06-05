import itertools

from utils import read_csv_file
from .compute_correlation import compute_correlation


def get_physio_correlations_and_scores(
        physio_task_file_paths: list[str],
        channels: list[str],
        score_column_name: str,
        remove_nan: bool = False) -> tuple[dict[str, list[float]], list[float]]:
    correlation_per_channel = {channel: [] for channel in channels}
    scores = []

    for physio_task_file_path in physio_task_file_paths:  # one per experiment
        physio_task_df = read_csv_file(physio_task_file_path)

        # Drop rows with NaN values in any of the columns to check
        columns_to_check = [col for col in physio_task_df.columns if
                            any(sub_string in col for sub_string in channels)]
        physio_task_df = physio_task_df.dropna(subset=columns_to_check)

        # Compute correlations
        for channel in channels:
            computers = ["lion", "tiger", "leopard"]
            combinations = itertools.combinations(computers, 2)
            physio_correlations = []

            # Compute correlation for each pair of computers
            for computer1, computer2 in combinations:
                if f"{computer1}_{channel}" in physio_task_df.columns and \
                        f"{computer2}_{channel}" in physio_task_df.columns:
                    corr = compute_correlation(physio_task_df[f"{computer1}_{channel}"],
                                               physio_task_df[f"{computer2}_{channel}"])
                    physio_correlations.append(corr)

            # Compute average correlation for the channel
            average_corr = None if not physio_correlations \
                else sum(physio_correlations) / len(physio_correlations)

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
