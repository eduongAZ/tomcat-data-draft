import pandas as pd


def read_csv_file(csv_file_path, delimiter=','):
    """
    Read csv file and return a pandas dataframe
    :param csv_file_path: path to csv file
    :param delimiter: delimiter used in csv file
    :return: pandas dataframe
    """
    df = pd.read_csv(csv_file_path, delimiter=delimiter)
    return df
