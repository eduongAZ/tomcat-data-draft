import pandas as pd


def write_df(df: pd.DataFrame, path: str):
    df.to_csv(path, index=True)
