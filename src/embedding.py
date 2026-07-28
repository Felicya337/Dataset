import pandas as pd
from sentence_transformers import SentenceTransformer
import pickle
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

df = pd.read_csv("database/knowledge/knowledge.csv")

documents = df["content"].fillna("").tolist()

print("Membuat embedding...")

embeddings = model.encode(
    documents,
    show_progress_bar=True,
    convert_to_numpy=True
)

os.makedirs("database/vector", exist_ok=True)

with open("database/vector/embeddings.pkl", "wb") as f:
    pickle.dump(embeddings, f)

df.to_pickle("database/vector/knowledge.pkl")

print("\nEmbedding selesai dibuat!")
print("Jumlah dokumen :", len(documents))
print("Dimensi embedding :", embeddings.shape)