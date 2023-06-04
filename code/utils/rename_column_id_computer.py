import pandas as pd


def rename_column_id_computer(df: pd.DataFrame, id_computer: dict[str, str]) -> pd.DataFrame:
    """
    Rename column 'id' to 'computer' in a dataframe
    :param df: dataframe
    :param id_computer: id-computer mapping
    :return: dataframe with renamed column
    """
    new_cols = {c: c.replace(k, v) for c in df.columns for k, v in id_computer.items() if
                c.startswith(k)}
    df = df.rename(columns=new_cols)

    return df
