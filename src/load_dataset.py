import pandas as pd
from preprocessing import clean_workbook

FILE = "data/Dataset HackathonTourism - IT DEL.xlsx"

def load_all_data(clean=False):
    if clean:
        return clean_workbook(FILE)

    excel = pd.ExcelFile(FILE)

    datasets = {}

    for sheet in excel.sheet_names:
        datasets[sheet] = pd.read_excel(FILE, sheet_name=sheet)

    return datasets


if __name__ == "__main__":
    data = load_all_data()

    for name, df in data.items():
        print(name, df.shape)