import matplotlib.pyplot as plt


def plot_regression_per_channel(correlation_per_channel: dict[str, list[any]],
                                scores: list[any],
                                linear_regressor_per_channel: dict[str, any],
                                output_dir: str | None = None):
    # Ensure valid input
    assert len(correlation_per_channel) > 0
    for channel in correlation_per_channel.keys():
        assert channel in linear_regressor_per_channel.keys()
        assert len(correlation_per_channel[channel]) == len(scores)
        assert len(correlation_per_channel[channel]) > 0

    # axs = []
    # for _ in range(len(correlation_per_channel.keys())):
    #     plt.figure()
    #     axs.append(plt.gca())
    #
    # for i, (channel, values) in enumerate(correlation_per_channel.items()):
    #     axs[i].scatter(values, scores)
    #     axs[i].plot([0, 1], linear_regressor_per_channel[channel].predict([[0], [1]]))
    #     axs[i].set_xlabel("Average Pairwise Correlation")
    #     axs[i].set_ylabel("Score")
    #     axs[i].set_title(channel)
    #
    #     if output_dir is not None:
    #         plt.savefig(f"{output_dir}/regression_{channel}.png")
    #
    #     plt.show()

    for channel, values in correlation_per_channel.items():
        plt.figure()
        plt.scatter(values, scores)
        plt.plot([0, 1], linear_regressor_per_channel[channel].predict([[0], [1]]))
        plt.xlabel("Average Pairwise Correlation")
        plt.ylabel("Score")
        plt.title(channel)

        if output_dir is not None:
            plt.savefig(f"{output_dir}/regression_{channel}.png")

        plt.show()
