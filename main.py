import pandas as pd

file = "data/Dataset HackathonTourism - IT DEL.xlsx"

excel = pd.ExcelFile(file)

print("=" * 60)
print("RINGKASAN DATASET")
print("=" * 60)

for sheet in excel.sheet_names:
    df = pd.read_excel(file, sheet_name=sheet)

    print(f"\nSheet : {sheet}")
    print(f"Jumlah baris : {df.shape[0]}")
    print(f"Jumlah kolom : {df.shape[1]}")

    print("Kolom:")
    print(list(df.columns))

    print("-" * 60)