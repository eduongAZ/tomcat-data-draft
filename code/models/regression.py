from typing import Any, Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


from constants import EEG_CHANNELS, NIRS_CHANNELS


def regress_nirs(axs: List[Any], dataset_filepaths: List[str]):
    return regress(axs, dataset_filepaths, NIRS_CHANNELS)


def regress_eeg(axs: List[Any], dataset_filepaths: List[str]):
    return regress(axs, dataset_filepaths, EEG_CHANNELS)


def regress(axs: List[Any], dataset_filepaths: List[str], channels: List[str]):
    correlation_per_channel = {channel: [] for channel in channels}
    scores = []

    for dataset_filepath in dataset_filepaths:  # one per experiment
        data = pd.read_csv(dataset_filepath)
        for channel in channels:
            corr_lt = pearsonr(data[f"lion_{channel}"], data[f"tiger_{channel}"]).correlation
            corr_tp = pearsonr(data[f"tiger_{channel}"], data[f"leopard_{channel}"]).correlation
            corr_pl = pearsonr(data[f"leopard_{channel}"], data[f"lion_{channel}"]).correlation

            corr = (corr_lt + corr_tp + corr_pl) / 3

            correlation_per_channel[channel].append(corr)
        scores.append(data["score"].values[-1])

    return fit(axs, correlation_per_channel, scores)


def fit(axs: List[Any], correlation_per_channel: Dict[str, Any], scores: Any):
    lr = LinearRegression()

    rmse_per_channel = {}

    for i, (channel, values) in enumerate(correlation_per_channel.items()):
        X = np.array(values)[:, None]
        lr.fit(X, scores)

        y_hat = lr.predict(X)

        rmse_per_channel[channel] = np.sqrt(mean_squared_error(scores, y_hat))

        axs[i].scatter(values, scores)
        axs[i].plot([0, 1], lr.predict([[0], [1]]))
        axs[i].set_xlabel("Average Pairwise Correlation")
        axs[i].set_xlabel("Score")
        axs[i].set_title(channel)

    return rmse_per_channel


if __name__ == "__main__":
    axs = []
    for _ in range(len(NIRS_CHANNELS)):
        plt.figure()
        axs.append(plt.gca())

    rmses = regress_nirs(axs, ["../../data/exp_2023_02_21_14/minecraft_saturn_a_physio_task.csv", "../../data/exp_2023_02_21_14/minecraft_saturn_a_physio_task.csv"])

    print(rmses)
    plt.show()
