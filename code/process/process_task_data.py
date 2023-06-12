import os

from tqdm import tqdm

from common import write_df
from .process_rest_state import process_rest_state


def processing_rest_state(exp_data: dict[str, any]):
    rest_state_df = process_rest_state(
        exp_data['info'],
        exp_data['task_csv_path'],
        exp_data['physio'],
        exp_data['frequency']
    )
    os.makedirs(exp_data['output_dir'], exist_ok=True)
    write_df(rest_state_df, os.path.join(exp_data['output_dir'], 'rest_state_physio_task.csv'))


def process_task_data(task_data: dict[str, any]):
    pbar = tqdm(task_data.items())
    for exp, exp_data in pbar:
        pbar.set_description(exp)

        processing_rest_state(exp_data['rest_state'])
