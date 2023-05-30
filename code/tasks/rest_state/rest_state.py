import pandas as pd

from utils import read_csv_file
from utils import read_json_file


def _combine_rest_state_physio_task(rest_state_task_df: pd.DataFrame,
                                    rest_state_physio_csv_path: str,
                                    participant_id: str) -> pd.DataFrame:
    rest_state_physio_df = read_csv_file(rest_state_physio_csv_path, delimiter='\t')

    start_time = rest_state_task_df.query('event_type == "start_rest_state"').iloc[0]['time']
    end_time = rest_state_task_df.query('event_type == "end_rest_state"').iloc[0]['time']

    rest_state_physio_df = rest_state_physio_df.assign(participant_id=participant_id)

    def _assign_event_type(row):
        if start_time <= row['unix_time'] <= end_time:
            return 'during_rest_state'
        else:
            return 'outside_of_rest_state'

    rest_state_physio_df['task_status'] = rest_state_physio_df.apply(_assign_event_type, axis=1)

    return rest_state_physio_df


class RestState:
    def __init__(self,
                 participant_ids: dict,
                 rest_state_task_df: pd.DataFrame,
                 rest_state_physio: dict[str, pd.DataFrame]
                 ):
        self.participant_ids = participant_ids
        self.rest_state_task_df = rest_state_task_df
        self.rest_state_physio = rest_state_physio

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

        lion_physio_nirs_df = _combine_rest_state_physio_task(
            rest_state_task_df=rest_state_task_df,
            rest_state_physio_csv_path=rest_state_physio_directory + '/lion/NIRS_filtered_rest_state.csv',
            participant_id=participant_ids['lion'])

        tiger_physio_nirs_df = _combine_rest_state_physio_task(
            rest_state_task_df=rest_state_task_df,
            rest_state_physio_csv_path=rest_state_physio_directory + '/tiger/NIRS_filtered_rest_state.csv',
            participant_id=participant_ids['tiger'])

        leopard_physio_nirs_df = _combine_rest_state_physio_task(
            rest_state_task_df=rest_state_task_df,
            rest_state_physio_csv_path=rest_state_physio_directory + '/leopard/NIRS_filtered_rest_state.csv',
            participant_id=participant_ids['leopard'])

        return cls(
            participant_ids=participant_ids,
            rest_state_task_df=rest_state_task_df,
            rest_state_physio={
                'lion': lion_physio_nirs_df,
                'tiger': tiger_physio_nirs_df,
                'leopard': leopard_physio_nirs_df
            }
        )
