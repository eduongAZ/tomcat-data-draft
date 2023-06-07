import json

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


def linear_fit(correlation_per_channel: dict[str, list[any]],
               scores: list[any],
               output_file: str | None = None):
    # ensure valid input
    for correlations in correlation_per_channel.values():
        assert len(correlations) == len(scores)
        assert len(correlations) > 0
        assert not any(corr is None for corr in correlations)
        assert not any(score is None for score in scores)

    # fit a linear regression model for each channel
    rmse_per_channel = {}
    linear_regressor_per_channel = {}
    linear_regression_slope_per_channel = {}
    predictions_per_channel = {}
    r2_per_channel = {}

    mean_score = np.mean(scores)  # for null model

    for i, (channel, values) in enumerate(correlation_per_channel.items()):
        lr = LinearRegression()

        X = np.array(values)[:, None]
        lr.fit(X, scores)

        y_hat = lr.predict(X)

        predictions_per_channel[channel] = y_hat.tolist()
        linear_regressor_per_channel[channel] = lr
        rmse_per_channel[channel] = np.sqrt(mean_squared_error(scores, y_hat))
        r2_per_channel[channel] = r2_score(scores, y_hat)
        linear_regression_slope_per_channel[channel] = lr.coef_[0]

    null_model_r2 = r2_score(scores, [mean_score] * len(scores))

    # Log results to JSON file
    if output_file is not None:
        json_filename = output_file
        json_data = {
            'predictions_per_channel': predictions_per_channel,
            'rmse_per_channel': rmse_per_channel,
            'r2_per_channel': r2_per_channel,
            'null_model_r2': null_model_r2,
            'linear_regression_slope': linear_regression_slope_per_channel
        }
        with open(json_filename, 'w') as jsonfile:
            json.dump(json_data, jsonfile, indent=4)

    return predictions_per_channel, \
        rmse_per_channel, \
        linear_regressor_per_channel, \
        r2_per_channel, \
        null_model_r2, \
        linear_regression_slope_per_channel
