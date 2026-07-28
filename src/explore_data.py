from load_dataset import load_all_data

data = load_all_data()

for sheet, df in data.items():
    print("=" * 70)
    print(f"Sheet : {sheet}")
    print("=" * 70)

    print("\n5 Data Pertama:")
    print(df.head())

    print("\nJumlah Missing Value:")
    print(df.isnull().sum())

    print("\n")