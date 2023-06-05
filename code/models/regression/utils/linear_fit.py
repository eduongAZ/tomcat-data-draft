import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


def linear_fit(correlation_per_channel: dict[str, list[any]],
               scores: list[any]
               ) -> tuple[dict[str, list[any]], dict[str, float], dict[str, LinearRegression]]:
    # ensure valid input
    for correlations in correlation_per_channel.values():
        assert len(correlations) == len(scores)
        assert len(correlations) > 0
        assert not any(corr is None for corr in correlations)
        assert not any(score is None for score in scores)

    # fit a linear regression model for each channel
    rmse_per_channel = {}
    linear_regressor_per_channel = {}
    predictions_per_channel = {}

    for i, (channel, values) in enumerate(correlation_per_channel.items()):
        lr = LinearRegression()

        X = np.array(values)[:, None]
        lr.fit(X, scores)

        y_hat = lr.predict(X)

        predictions_per_channel[channel] = y_hat
        linear_regressor_per_channel[channel] = lr
        rmse_per_channel[channel] = np.sqrt(mean_squared_error(scores, y_hat))

    return predictions_per_channel, rmse_per_channel, linear_regressor_per_channel
