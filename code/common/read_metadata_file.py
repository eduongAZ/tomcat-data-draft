from datetime import datetime

import pandas as pd

from .metadata_message_generator import metadata_message_generator


def read_metadata_file(metadata_file_path: str) -> pd.DataFrame:
    messages = metadata_message_generator(metadata_file_path)

    mission_topic = "observations/events/mission"
    score_topic = "observations/events/scoreboard"
    trial_started = False

    task_data = {
        "time": [],
        "score": []
    }

    # parse messages
    for message in messages:
        # parse trial message
        if "topic" in message and message["topic"] == mission_topic:
            if message["data"]["mission_state"] == "Start":
                trial_started = True
                continue
            # end parsing after the trial has ended
            elif message["data"]["mission_state"] == "Stop":
                break
            else:
                raise ValueError("Unknown mission state")

        # only start monitoring after trial has started
        elif not trial_started:
            continue

        # extract score
        if "topic" in message and message["topic"] == score_topic:
            score = message["data"]["scoreboard"]["TeamScore"]
            timestamp = datetime.fromisoformat(
                message["header"]["timestamp"]).timestamp()
            task_data["score"].append(score)
            task_data["time"].append(timestamp)

    task_df = pd.DataFrame(task_data)

    return task_df
