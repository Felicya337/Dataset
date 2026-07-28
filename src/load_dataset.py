import pandas as pd

FILE = "data/Dataset HackathonTourism - IT DEL.xlsx"

def load_all_data():
    excel = pd.ExcelFile(FILE)

    datasets = {}

    for sheet in excel.sheet_names:
        datasets[sheet] = pd.read_excel(FILE, sheet_name=sheet)

    return datasets


if __name__ == "__main__":
    data = load_all_data()

    for name, df in data.items():
        print(name, df.shape)