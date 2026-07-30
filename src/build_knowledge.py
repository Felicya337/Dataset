import os

import pandas as pd
from load_dataset import load_all_data

DATA = load_all_data(clean=True)

os.makedirs("database/knowledge", exist_ok=True)

knowledge = []


def _text_value(value):
    if pd.isna(value):
        return ""
    return str(value).strip()

# ============================
# WISATA
# ============================

wisata = DATA.get("wisata-metadata", pd.DataFrame())

for _, row in wisata.iterrows():

    title = _text_value(row.get("place-name", ""))

    if not title:
        continue

    text = f"""
Nama Tempat : {title}

Kategori : {_text_value(row.get("place-type", ""))}

Rating : {_text_value(row.get("place-rating", ""))}

Alamat : {_text_value(row.get("address", ""))}

Jam Operasional : {_text_value(row.get("operational-hour", ""))}

Harga Tiket : {_text_value(row.get("entry-fee", ""))}

Status : {_text_value(row.get("status", ""))}
"""

    knowledge.append({
        "category":"wisata",
        "title":title,
        "content":text
    })

# ============================
# HOTEL
# ============================

hotel = DATA.get("hotel-metadata", pd.DataFrame())

for _, row in hotel.iterrows():

    title = _text_value(row.get("place-name", ""))

    if not title:
        continue

    text = f"""
Nama Hotel : {title}

Harga : {_text_value(row.get("price-per-head", ""))}

Check In : {_text_value(row.get("check-in", ""))}

Check Out : {_text_value(row.get("check-out", ""))}

Fasilitas : {_text_value(row.get("Fasilitas", ""))}

Alamat : {_text_value(row.get("address", ""))}

Rating : {_text_value(row.get("place-rating", ""))}
"""

    knowledge.append({
        "category":"hotel",
        "title":title,
        "content":text
    })

# ============================
# RESTORAN
# ============================

resto = DATA.get("resto-metadata", pd.DataFrame())

for _, row in resto.iterrows():

    title = _text_value(row.get("place-name", ""))

    if not title:
        continue

    text = f"""
Nama Restoran : {title}

Harga : {_text_value(row.get("price-per-head", ""))}

Jam Operasional : {_text_value(row.get("opening-hours", ""))}

Menu Favorit : {_text_value(row.get("recommend-menu", ""))}

Fasilitas : {_text_value(row.get("Fasilitas", ""))}

Alamat : {_text_value(row.get("address", ""))}

Rating : {_text_value(row.get("place-rating", ""))}
"""

    knowledge.append({
        "category":"restoran",
        "title":title,
        "content":text
    })

# ============================
# TRANSPORTASI
# ============================

transport = DATA.get("transportasi", pd.DataFrame())

for _, row in transport.iterrows():

    title = _text_value(row.get("transport-name", ""))

    if not title:
        continue

    text = f"""
Transportasi : {title}

Rute : {_text_value(row.get("direction", ""))}

Harga : {_text_value(row.get("price", ""))}

Jenis Mobil : {_text_value(row.get("jenis-mobil", ""))}

Jam Operasional : {_text_value(row.get("operational-hour", ""))}
"""

    knowledge.append({
        "category":"transportasi",
        "title":title,
        "content":text
    })

# ============================
# SIMPAN
# ============================

df = pd.DataFrame(knowledge)

df.to_csv("database/knowledge/knowledge.csv",index=False)

print(df.head())

print("\nJumlah Knowledge :",len(df))