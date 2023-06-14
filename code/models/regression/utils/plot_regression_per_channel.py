import matplotlib.pyplot as plt


def plot_regression_per_channel(correlation_per_channel: dict[str, list[any]],
                                scores: list[any],
                                linear_regressor_per_channel: dict[str, any],
                                output_dir: str | None = None,
                                show_images: bool = True):
    # Ensure valid input
    assert len(correlation_per_channel) > 0
    for channel in correlation_per_channel.keys():
        assert channel in linear_regressor_per_channel.keys()
        assert len(correlation_per_channel[channel]) == len(scores)
        assert len(correlation_per_channel[channel]) > 0

    for channel, values in correlation_per_channel.items():
        lowest_value = min(values)
        highest_value = max(values)
        plt.figure()
        plt.scatter(values, scores)
        plt.plot([lowest_value, highest_value],
                 linear_regressor_per_channel[channel].predict([[lowest_value], [highest_value]]))
        plt.xlabel("Average Pairwise Correlation")
        plt.ylabel("Score")
        plt.title(channel)

        if output_dir is not None:
            plt.savefig(f"{output_dir}/regression_{channel}.png")

        if show_images:
            plt.show()
        else:
            plt.close()
