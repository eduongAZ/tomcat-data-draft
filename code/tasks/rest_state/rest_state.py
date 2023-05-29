import pandas as pd

from utils import read_csv_file
from utils import read_json_file


class RestState:
    def __init__(self,
                 participant_ids: dict,
                 rest_state_task_df: pd.DataFrame,
                 rest_state_physio_df: dict[str, pd.DataFrame]
                 ):
        self.participant_ids = participant_ids
        self.rest_state_task_df = rest_state_task_df
        self.rest_state_physio_df = rest_state_physio_df

    @classmethod
    def from_files(cls,
                   metadata_path: str,
                   rest_state_csv_path: str,
                   rest_state_physio_directory: str):
        """
        Create a RestState object from a metadata dictionary
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

        # Read rest state physio data
        lion_physio_nirs_df = read_csv_file(
            rest_state_physio_directory + '/lion/NIRS_filtered_rest_state.csv',
            delimiter='\t')
        tiger_physio_nirs_df = read_csv_file(
            rest_state_physio_directory + '/tiger/NIRS_filtered_rest_state.csv',
            delimiter='\t')
        leopard_physio_nirs_df = read_csv_file(
            rest_state_physio_directory + '/leopard/NIRS_filtered_rest_state.csv',
            delimiter='\t')

        return cls(
            participant_ids=participant_ids,
            rest_state_task_df=rest_state_task_df,
            rest_state_physio_df={
                'lion': lion_physio_nirs_df,
                'tiger': tiger_physio_nirs_df,
                'leopard': leopard_physio_nirs_df
            }
        )
