import pandas as pd
import os

from utils import read_csv_file
from .combine_participants_physio import combine_participants_physio


def combine_participants_physio_from_files(
        id_filepath: dict[str, str],
        start_time: float,
        end_time: float,
        num_increments: int) -> pd.DataFrame:
    id_df = {}

    for participant_id, filepath in id_filepath.items():
        # Read file
        id_df[participant_id] = read_csv_file(filepath, delimiter=',')

        # Extract the prefix from the file name
        prefix = '_'.join(os.path.basename(filepath).split('_')[0:2]) + "_"

        # Rename the columns by removing the prefix
        id_df[participant_id].columns = id_df[participant_id].columns.str.replace(prefix, '')

    return combine_participants_physio(
        id_df,
        start_time,
        end_time,
        num_increments
    )
