import os

import pandas as pd

from physio import combine_participants_physio
from utils import read_csv_file
from utils import read_json_file


def _combine_rest_state_physio_task(rest_state_task_df: pd.DataFrame,
                                    rest_state_physio_df: pd.DataFrame) -> pd.DataFrame:
    start_time = rest_state_task_df.query('event_type == "start_rest_state"').iloc[0]['time']
    end_time = rest_state_task_df.query('event_type == "end_rest_state"').iloc[0]['time']

    def _assign_event_type(row):
        if start_time <= row.name <= end_time:
            return 'during_rest_state'
        else:
            return 'outside_of_rest_state'

    rest_state_physio_df['task_status'] = rest_state_physio_df.apply(_assign_event_type, axis=1)

    return rest_state_physio_df


class RestState:
    def __init__(self,
                 participant_ids: dict,
                 rest_state_task_df: pd.DataFrame,
                 rest_state_physio: pd.DataFrame,
                 rest_state_physio_task: pd.DataFrame):
        self.participant_ids = participant_ids
        self.rest_state_task_df = rest_state_task_df
        self.rest_state_physio = rest_state_physio
        self.rest_state_physio_task = rest_state_physio_task

    @classmethod
    def from_files(cls,
                   metadata_path: str,
                   rest_state_csv_path: str,
                   rest_state_physio_directory: str,
                   num_increments: int = 3069):
        """
        Create a RestState object from a metadata dictionary
        :param num_increments: number of time series increments
        :param rest_state_physio_directory: rest state physio directory
        :param rest_state_csv_path: rest state csv file path
        :param metadata_path: json file metadata path
        :return: RestState object
        """
        # Read metadata
        metadata = read_json_file(metadata_path)
        participant_ids = metadata['participant_ids']

        # Read rest state task data
        rest_state_task_df = read_csv_file(rest_state_csv_path, delimiter=';')

        lion_rest_state_physio_csv_path = rest_state_physio_directory + '/lion/NIRS_filtered_rest_state.csv'
        tiger_rest_state_physio_csv_path = rest_state_physio_directory + '/tiger/NIRS_filtered_rest_state.csv'
        leopard_rest_state_physio_csv_path = rest_state_physio_directory + '/leopard/NIRS_filtered_rest_state.csv'

        rest_state_physio = {
            participant_ids['lion']: read_csv_file(lion_rest_state_physio_csv_path, delimiter='\t'),
            participant_ids['tiger']: read_csv_file(tiger_rest_state_physio_csv_path,
                                                    delimiter='\t'),
            participant_ids['leopard']: read_csv_file(leopard_rest_state_physio_csv_path,
                                                      delimiter='\t'),
        }

        start_time = rest_state_task_df.query('event_type == "start_rest_state"').iloc[0]['time']
        end_time = rest_state_task_df.query('event_type == "end_rest_state"').iloc[0]['time']

        rest_state_physio = combine_participants_physio(
            rest_state_physio,
            start_time,
            end_time,
            num_increments=num_increments
        )

        rest_state_physio_task = _combine_rest_state_physio_task(
            rest_state_task_df,
            rest_state_physio
        )

        return cls(
            participant_ids=participant_ids,
            rest_state_task_df=rest_state_task_df,
            rest_state_physio=rest_state_physio,
            rest_state_physio_task=rest_state_physio_task
        )

    def write_physio_data_csv(self, output_dir_path: str):
        """
        Write the physio data to a csv file in output directory
        :param output_dir_path: output directory path
        """
        # Create the directory if it doesn't exist
        if not os.path.exists(output_dir_path):
            os.makedirs(output_dir_path)

        self.rest_state_physio_task.to_csv(output_dir_path + '/rest_state_physio_task.csv',
                                           index=True)
