from pathlib import Path
import re

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = PROJECT_ROOT / "data" / "Dataset HackathonTourism - IT DEL.xlsx"
CLEAN_DIR = PROJECT_ROOT / "data" / "cleaned"

PLACEHOLDER_VALUES = {"", "-", "na", "n/a", "none", "null", "nan"}


def _normalize_value(value):
    if pd.isna(value):
        return pd.NA

    if isinstance(value, str):
        text = value.replace("\r\n", "\n").replace("\r", "\n")
        text = re.sub(r"[ \t]+", " ", text).strip()

        if not text or text.lower() in PLACEHOLDER_VALUES:
            return pd.NA

        return text

    return value


def _normalize_column_name(value):
    text = _normalize_value(value)

    if pd.isna(text):
        return ""

    text = str(text).strip()
    text = re.sub(r"[^\w]+", "_", text, flags=re.UNICODE)
    text = re.sub(r"_+", "_", text).strip("_")

    return text


def _make_unique(names):
    seen = {}
    unique_names = []

    for name in names:
        base_name = name or "column"
        count = seen.get(base_name, 0)

        if count:
            unique_name = f"{base_name}_{count + 1}"
        else:
            unique_name = base_name

        seen[base_name] = count + 1
        unique_names.append(unique_name)

    return unique_names


def clean_dataframe(df, forward_fill_columns=None):
    cleaned = df.copy()
    cleaned.columns = [str(column).strip() for column in cleaned.columns]

    cleaned = cleaned.loc[:, ~cleaned.columns.str.match(r"^Unnamed(?::\s*\d+)?$", na=False)]
    cleaned = cleaned.dropna(axis=1, how="all")
    cleaned = cleaned.apply(lambda column: column.map(_normalize_value))

    if forward_fill_columns:
        for column in forward_fill_columns:
            if column in cleaned.columns:
                cleaned[column] = cleaned[column].ffill()

    cleaned = cleaned.dropna(how="all")
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)

    return cleaned


def clean_attractions_info_sheet(file_path=RAW_FILE):
    frame = pd.read_excel(file_path, sheet_name="Attractions Info")
    frame.columns = [str(column).strip() for column in frame.columns]
    frame = frame.loc[:, ~frame.columns.str.contains("^Unnamed", na=False)]
    frame = frame.apply(lambda column: column.map(_normalize_value))

    if {"No", "Nama Kabupaten", "Nama Atraksi", "Detail"}.issubset(frame.columns):
        placeholder_rows = frame["Detail"].eq("Deskripsi") & frame["Nama Atraksi"].isna()
        frame = frame.loc[~placeholder_rows]

    frame = frame.dropna(how="all").drop_duplicates().reset_index(drop=True)
    return frame


def clean_prompt_sheet(file_path=RAW_FILE):
    frame = pd.read_excel(file_path, sheet_name="prompt", header=None)

    if frame.shape[1] < 3:
        return pd.DataFrame(columns=["No", "Prompt"])

    frame = frame.iloc[:, 1:3].copy()
    frame.columns = ["No", "Prompt"]
    frame = frame.iloc[3:].copy()
    frame["No"] = frame["No"].map(_normalize_value)
    frame["Prompt"] = frame["Prompt"].map(_normalize_value)
    frame = frame.dropna(subset=["Prompt"]).reset_index(drop=True)
    frame = frame.drop_duplicates().reset_index(drop=True)
    return frame


def clean_info_seputar_sheet(file_path=RAW_FILE):
    raw = pd.read_excel(file_path, sheet_name="Info Seputar Danau Toba (TOP 3)", header=None)

    if raw.empty:
        return raw

    header_rows = raw.iloc[1:4].copy().ffill(axis=1)
    headers = []

    for column_index in range(raw.shape[1]):
        parts = []

        for row_index in range(header_rows.shape[0]):
            value = header_rows.iat[row_index, column_index]
            normalized = _normalize_column_name(value)

            if normalized and (not parts or parts[-1] != normalized):
                parts.append(normalized)

        headers.append("_".join(parts) if parts else f"column_{column_index + 1}")

    headers = _make_unique(headers)
    data = raw.iloc[4:].copy().reset_index(drop=True)
    data.columns = headers
    data = data.apply(lambda column: column.map(_normalize_value))

    drop_columns = [column for column in data.columns if data[column].isna().all()]
    if drop_columns:
        data = data.drop(columns=drop_columns)

    if "Nama_Kabupaten" in data.columns:
        data["Nama_Kabupaten"] = data["Nama_Kabupaten"].ffill()

    if "No" in data.columns:
        data = data.dropna(subset=["No", "Nama_Kabupaten"], how="all")

    data = data.dropna(how="all").drop_duplicates().reset_index(drop=True)
    return data


def clean_workbook(file_path=RAW_FILE):
    excel = pd.ExcelFile(file_path)
    cleaned_data = {}

    special_cleaners = {
        "Attractions Info": clean_attractions_info_sheet,
        "Info Seputar Danau Toba (TOP 3)": clean_info_seputar_sheet,
        "prompt": clean_prompt_sheet,
    }

    for sheet in excel.sheet_names:
        if sheet in special_cleaners:
            cleaned_data[sheet] = special_cleaners[sheet](file_path)
            continue

        frame = pd.read_excel(file_path, sheet_name=sheet)
        forward_fill_columns = [
            column for column in frame.columns if "kabupaten" in str(column).lower()
        ]
        cleaned_data[sheet] = clean_dataframe(frame, forward_fill_columns=forward_fill_columns)

    return cleaned_data


def save_cleaned_workbook(cleaned_data, output_dir=CLEAN_DIR):
    output_dir.mkdir(parents=True, exist_ok=True)

    for sheet_name, frame in cleaned_data.items():
        safe_name = re.sub(r"[^\w\-]+", "_", sheet_name.strip()).strip("_")
        frame.to_csv(output_dir / f"{safe_name}.csv", index=False)


if __name__ == "__main__":
    clean_data = clean_workbook()
    save_cleaned_workbook(clean_data)

    for sheet, frame in clean_data.items():
        print(sheet)
        print(f"Shape : {frame.shape}")
        print(frame.columns.tolist())
        print("-" * 60)