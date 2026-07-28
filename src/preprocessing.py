import pandas as pd
from load_dataset import load_all_data

data = load_all_data()

clean_data = {}

for sheet, df in data.items():

    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    df = df.dropna(axis=1, how="all")

    clean_data[sheet] = df

    print(f"{sheet}")
    print(f"Shape : {df.shape}")
    print(df.columns.tolist())
    print("-"*60)