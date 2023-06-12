from .process_rest_state import process_rest_state


def process_task_data(task_data: dict[str, any]) -> dict[str, any]:
    exp_processed_data = {}
    for exp, exp_data in task_data.items():
        # Rest state
        rest_state_df = process_rest_state(
            exp_data['rest_state']['info'],
            exp_data['rest_state']['task_csv_path'],
            exp_data['rest_state']['physio'],
            exp_data['rest_state']['frequency']
        )

        exp_processed_data[exp] = {
            'rest_state': rest_state_df
        }

    return exp_processed_data
