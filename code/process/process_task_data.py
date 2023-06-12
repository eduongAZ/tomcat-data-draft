import os

from tqdm import tqdm

from common import write_df
from .process_affective_individual import process_affective_individual
from .process_affective_team import process_affective_team
from .process_finger_tapping import process_finger_tapping
from .process_minecraft import process_minecraft
from .process_ping_pong_competitive import process_ping_pong_competitive
from .process_ping_pong_cooperative import process_ping_pong_cooperative
from .process_rest_state import process_rest_state


def processing_rest_state(task_data: dict[str, any]):
    task_df, status, message = process_rest_state(
        task_data['info'],
        task_data['task_csv_path'],
        task_data['physio'],
        task_data['frequency']
    )
    if status:
        os.makedirs(task_data['output_dir'], exist_ok=True)
        write_df(task_df, os.path.join(task_data['output_dir'], f'rest_state_physio_task.csv'))


def processing_finger_tapping(task_data: dict[str, any]):
    task_df, status, message = process_finger_tapping(
        task_data['info'],
        task_data['task_csv_path'],
        task_data['physio'],
        task_data['frequency']
    )
    if status:
        os.makedirs(task_data['output_dir'], exist_ok=True)
        write_df(task_df, os.path.join(task_data['output_dir'], f'finger_tapping_physio_task.csv'))


def processing_affective_individual(task_data: dict[str, any]):
    computer_name = task_data['computer_name']
    task_df, status, message = process_affective_individual(
        task_data['info'],
        task_data['task_csv_path'],
        task_data['physio'],
        task_data['frequency'],
        computer_name,
        task_data['participant_id'],
    )
    if status:
        os.makedirs(task_data['output_dir'], exist_ok=True)
        write_df(task_df,
                 os.path.join(task_data['output_dir'], f'{computer_name}_affective_individual_physio_task.csv'))


def processing_affective_team(task_data: dict[str, any]):
    task_df, status, message = process_affective_team(
        task_data['info'],
        task_data['task_csv_path'],
        task_data['physio'],
        task_data['frequency']
    )
    if status:
        os.makedirs(task_data['output_dir'], exist_ok=True)
        write_df(task_df, os.path.join(task_data['output_dir'], f'affective_team_physio_task.csv'))


def processing_ping_pong_competitive(task_data: dict[str, any], match_name: str):
    task_df, status, message = process_ping_pong_competitive(
        task_data['info'],
        task_data['task_csv_path'],
        task_data['physio'],
        task_data['frequency']
    )
    if status:
        os.makedirs(task_data['output_dir'], exist_ok=True)
        write_df(task_df, os.path.join(task_data['output_dir'], f'{match_name}_physio_task.csv'))


def processing_ping_pong_cooperative(task_data: dict[str, any]):
    task_df, status, message = process_ping_pong_cooperative(
        task_data['info'],
        task_data['task_csv_path'],
        task_data['physio'],
        task_data['frequency']
    )
    if status:
        os.makedirs(task_data['output_dir'], exist_ok=True)
        write_df(task_df, os.path.join(task_data['output_dir'], f'ping_pong_cooperative_physio_task.csv'))


def processing_minecraft(task_data: dict[str, any], mission_name: str):
    task_df, status, message = process_minecraft(
        task_data['info'],
        task_data['task_metadata_path'],
        task_data['physio'],
        task_data['frequency']
    )
    if status:
        os.makedirs(task_data['output_dir'], exist_ok=True)
        write_df(task_df, os.path.join(task_data['output_dir'], f'{mission_name}_physio_task.csv'))


def process_task_data(task_data: dict[str, any]):
    pbar = tqdm(task_data.items())
    for exp, exp_data in pbar:
        pbar.set_description(exp)

        if "rest_state" in exp_data:
            processing_rest_state(exp_data["rest_state"])

        if "finger_tapping" in exp_data:
            processing_finger_tapping(exp_data["finger_tapping"])

        if "affective_individual_lion" in exp_data:
            processing_affective_individual(exp_data["affective_individual_lion"])

        if "affective_individual_tiger" in exp_data:
            processing_affective_individual(exp_data["affective_individual_tiger"])

        if "affective_individual_leopard" in exp_data:
            processing_affective_individual(exp_data["affective_individual_leopard"])

        if "affective_team" in exp_data:
            processing_affective_team(exp_data["affective_team"])

        if "ping_pong_competitive_0" in exp_data:
            processing_ping_pong_competitive(exp_data["ping_pong_competitive_0"], "ping_pong_competitive_0")

        if "ping_pong_competitive_1" in exp_data:
            processing_ping_pong_competitive(exp_data["ping_pong_competitive_1"], "ping_pong_competitive_1")

        if "ping_pong_cooperative" in exp_data:
            processing_ping_pong_cooperative(exp_data["ping_pong_cooperative"])

        if "minecraft_hands_on_training" in exp_data:
            processing_minecraft(exp_data["minecraft_hands_on_training"], "minecraft_hands_on_training")

        if "minecraft_saturn_a" in exp_data:
            processing_minecraft(exp_data["minecraft_saturn_a"], "minecraft_saturn_a")

        if "minecraft_saturn_b" in exp_data:
            processing_minecraft(exp_data["minecraft_saturn_b"], "minecraft_saturn_b")
