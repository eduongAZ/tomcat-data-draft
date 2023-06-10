import pandas as pd
import os

from utils import read_csv_file
from .combine_participants_physio import combine_participants_physio


def combine_participants_physio_from_files(
        id_filepath: dict[str, str],
        start_time: float,
        end_time: float,
        frequency: float) -> pd.DataFrame:
    id_df = {}

    for participant_id, filepath in id_filepath.items():
        # Open the file in text mode and read the first line
        with open(filepath, 'r') as f:
            first_line = f.readline()

        # Determine the delimiter
        if '\t' in first_line:
            delimiter = '\t'
        elif ',' in first_line:
            delimiter = ','
        else:
            raise ValueError('Delimiter could not be detected')

        # Read file
        id_df[participant_id] = read_csv_file(filepath, delimiter=delimiter)

        # # Extract the prefix from the file name
        # prefix = '_'.join(os.path.basename(filepath).split('_')[0:2]) + "_"
        #
        # # Rename the columns by removing the prefix
        # id_df[participant_id].columns = id_df[participant_id].columns.str.replace(prefix, '')

    return combine_participants_physio(
        id_df,
        start_time,
        end_time,
        frequency
    )
