import pandas as pd
import os

EXCEL_FILE = "data/Dataset HackathonTourism - IT DEL.xlsx"

os.makedirs("database/knowledge", exist_ok=True)

excel = pd.ExcelFile(EXCEL_FILE)

knowledge = []

# ============================
# WISATA
# ============================

wisata = pd.read_excel(EXCEL_FILE, sheet_name="wisata-metadata")

for _, row in wisata.iterrows():

    text = f"""
Nama Tempat : {row.get("place-name","")}

Kategori : {row.get("place-type","")}

Rating : {row.get("place-rating","")}

Alamat : {row.get("address","")}

Jam Operasional : {row.get("operational-hour","")}

Harga Tiket : {row.get("entry-fee","")}

Status : {row.get("status","")}
"""

    knowledge.append({
        "category":"wisata",
        "title":row.get("place-name",""),
        "content":text
    })

# ============================
# HOTEL
# ============================

hotel = pd.read_excel(EXCEL_FILE,sheet_name="hotel-metadata")

for _, row in hotel.iterrows():

    text = f"""
Nama Hotel : {row.get("place-name","")}

Harga : {row.get("price-per-head","")}

Check In : {row.get("check-in","")}

Check Out : {row.get("check-out","")}

Fasilitas : {row.get("Fasilitas","")}

Alamat : {row.get("address","")}

Rating : {row.get("place-rating","")}
"""

    knowledge.append({
        "category":"hotel",
        "title":row.get("place-name",""),
        "content":text
    })

# ============================
# RESTORAN
# ============================

resto = pd.read_excel(EXCEL_FILE,sheet_name="resto-metadata")

for _, row in resto.iterrows():

    text = f"""
Nama Restoran : {row.get("place-name","")}

Harga : {row.get("price-per-head","")}

Jam Operasional : {row.get("opening-hours","")}

Menu Favorit : {row.get("recommend-menu","")}

Fasilitas : {row.get("Fasilitas","")}

Alamat : {row.get("address","")}

Rating : {row.get("place-rating","")}
"""

    knowledge.append({
        "category":"restoran",
        "title":row.get("place-name",""),
        "content":text
    })

# ============================
# TRANSPORTASI
# ============================

transport = pd.read_excel(EXCEL_FILE,sheet_name="transportasi")

for _, row in transport.iterrows():

    text = f"""
Transportasi : {row.get("transport-name","")}

Rute : {row.get("direction","")}

Harga : {row.get("price","")}

Jenis Mobil : {row.get("jenis-mobil","")}

Jam Operasional : {row.get("operational-hour","")}
"""

    knowledge.append({
        "category":"transportasi",
        "title":row.get("transport-name",""),
        "content":text
    })

# ============================
# SIMPAN
# ============================

df = pd.DataFrame(knowledge)

df.to_csv("database/knowledge/knowledge.csv",index=False)

print(df.head())

print("\nJumlah Knowledge :",len(df))