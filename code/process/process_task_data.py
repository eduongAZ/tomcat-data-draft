import os

from tqdm import tqdm

from common import write_df
from .process_affective_team import process_affective_team
from .process_finger_tapping import process_finger_tapping
from .process_rest_state import process_rest_state


def processing_rest_state(task_data: dict[str, any]):
    task_df = process_rest_state(
        task_data['info'],
        task_data['task_csv_path'],
        task_data['physio'],
        task_data['frequency']
    )
    os.makedirs(task_data['output_dir'], exist_ok=True)
    write_df(task_df, os.path.join(task_data['output_dir'], f'rest_state_physio_task.csv'))


def processing_finger_tapping(task_data: dict[str, any]):
    task_df = process_finger_tapping(
        task_data['info'],
        task_data['task_csv_path'],
        task_data['physio'],
        task_data['frequency']
    )
    os.makedirs(task_data['output_dir'], exist_ok=True)
    write_df(task_df, os.path.join(task_data['output_dir'], f'finger_tapping_physio_task.csv'))


def processing_affective_team(task_data: dict[str, any]):
    task_df = process_affective_team(
        task_data['info'],
        task_data['task_csv_path'],
        task_data['physio'],
        task_data['frequency']
    )
    os.makedirs(task_data['output_dir'], exist_ok=True)
    write_df(task_df, os.path.join(task_data['output_dir'], f'affective_team_physio_task.csv'))


def process_task_data(task_data: dict[str, any]):
    pbar = tqdm(task_data.items())
    for exp, exp_data in pbar:
        pbar.set_description(exp)

        if "rest_state" in exp_data:
            processing_rest_state(exp_data["rest_state"])

        if "finger_tapping" in exp_data:
            processing_finger_tapping(exp_data["finger_tapping"])

        if "affective_team" in exp_data:
            processing_affective_team(exp_data["affective_team"])
