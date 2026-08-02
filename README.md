# TobaMate AI — Submission AI Hackathon IT Del 2026


## 1. Deskripsi Singkat

Wisatawan yang ingin berlibur ke kawasan Danau Toba sering kesulitan memperkirakan biaya, kehilangan banyak waktu mencari informasi wisata/hotel/kuliner/transportasi yang tersebar di banyak sumber, serta melewatkan pengalaman lokal (kuliner dan budaya khas Batak) karena tidak ada satu asisten yang merangkumnya.

**TobaMate AI** adalah asisten perjalanan berbasis AI yang mengubah preferensi wisatawan (budget, lama liburan, kota asal, jumlah orang, minat) menjadi rencana perjalanan (itinerary) lengkap per hari, estimasi biaya yang transparan, dan rekomendasi *local experience* — semuanya berbasis data pariwisata Danau Toba dari panitia.

Pendekatan AI yang digunakan adalah **RAG (Retrieval-Augmented Generation)**: preferensi/pertanyaan wisatawan diubah jadi *query* semantik untuk mencari data paling relevan di knowledge base (via *sentence embeddings* + cosine similarity), lalu hasilnya dipakai sebagai konteks oleh LLM (opsional) atau disusun langsung secara rule-based untuk itinerary dan estimasi biaya — sehingga jawaban selalu berpijak pada data nyata, bukan halusinasi.

## 2. Anggota Tim

| [Felicya Panjaitan]|
| [Mikhael Josua Roganda]|
| [Bryan Torisi Siagian]|

## 3. Pemanfaatan Data Pariwisata Toba

- **Data Utama:** Seluruh kategori dari *Lake Toba Smart Tourism Knowledge Dataset* panitia digunakan: destinasi wisata (`wisata-metadata`, `tempat-wisata-v1`, `wisata-v2`, `Attractions_Info`), akomodasi (`hotel-metadata`, `hotel-resto-v1`), kuliner & kafe (`resto-metadata`, `resto-hotel-v2`, `kuliner`), transportasi (`transportasi`), serta artikel budaya & info umum (`Artikel_Danau_Toba`, `Info_Seputar_Danau_Toba_TOP_3`, `waktu_operasional_destinasi`).
- **Pengolahan:**
  1. `src/preprocessing.py` — membersihkan setiap sheet Excel mentah (normalisasi whitespace, penanganan nilai placeholder seperti `-`/`NA`, deduplikasi, penanganan header berlapis) dan menyimpan hasilnya ke `data/cleaned/`.
  2. `src/build_knowledge.py` — mengintegrasikan data wisata, hotel, restoran, dan transportasi yang sudah bersih menjadi satu **knowledge base** terstruktur (`database/knowledge/knowledge.csv`) dengan kolom `category`, `title`, `content`.
  3. `src/embedding.py` — membuat *sentence embedding* (model `all-MiniLM-L6-v2`) untuk setiap entri knowledge base dan menyimpannya di `database/vector/` untuk pencarian semantik.
  4. `src/retrieval.py` — melakukan pencarian semantik (cosine similarity) di atas embedding tersebut, dengan opsi filter kategori.
  5. `src/itinerary.py` — menyusun itinerary per hari dan estimasi biaya (tiket masuk, akomodasi, kuliner, transportasi) langsung dari harga riil di dataset (lihat `src/utils.py::parse_price_range` untuk parsing format harga dataset seperti `"5.000 - 10.000"` atau `"Gratis"`).
  6. `src/chatbot.py` — menyatukan retrieval + LLM (opsional) untuk chat bebas dan narasi itinerary yang lebih natural.
- **Data Tambahan:** -

## 4. Tautan & Aset Pendukung

- **Link Video Demonstrasi (Wajib):** [Tautan Video - Unlisted]
- **Link Pitch Deck / Proposal (Wajib):** [Tautan Dokumen PDF]
- **Link Deployment / Live App (Opsional):** [Tautan jika aplikasi sudah di-deploy]

## 5. Struktur Repository

```text
.
├── app.py                     # Entry point Streamlit (Chat + Buat Itinerary)
├── main.py                    # Ringkasan cepat isi dataset mentah (per sheet)
├── requirements.txt
├── .env.example
├── data/
│   ├── Dataset HackathonTourism - IT DEL.xlsx   # dataset mentah panitia
│   └── cleaned/                                  # hasil src/preprocessing.py
├── database/
│   ├── knowledge/knowledge.csv                   # knowledge base terintegrasi
│   └── vector/{knowledge.pkl,embeddings.pkl}     # index untuk semantic search
└── src/
    ├── preprocessing.py       # cleaning dataset mentah -> data/cleaned
    ├── load_dataset.py        # loader dataset (raw / cleaned)
    ├── build_knowledge.py     # data/cleaned -> database/knowledge/knowledge.csv
    ├── embedding.py           # knowledge.csv -> embeddings (sentence-transformers)
    ├── retrieval.py           # semantic search (RAG - retrieval)
    ├── itinerary.py           # penyusun itinerary + estimasi biaya (RAG - generation, rule-based)
    ├── chatbot.py             # RAG chat + narasi LLM opsional (OpenAI)
    ├── utils.py                # parsing harga, format Rupiah, pembersihan teks
    └── explore_data.py        # eksplorasi data ad-hoc (EDA)
```

## 6. Prasyarat (Requirements)

- **Environment:** Python 3.10+ (dikembangkan & diuji dengan Python 3.12/3.13)
- **Package manager:** pip
- **Software tambahan:** tidak ada (tidak butuh Docker/database eksternal — knowledge base disimpan sebagai file CSV/pickle)
- **API Key Eksternal (opsional):** `OPENAI_API_KEY` — hanya diperlukan jika ingin jawaban chat & narasi itinerary dihasilkan oleh LLM (OpenAI). **Tanpa API key ini, aplikasi tetap berjalan penuh** lewat mode fallback berbasis retrieval (jawaban disusun langsung dari knowledge base). **Jangan commit API key asli ke repository.**

## 7. Environment Variables

Salin `.env.example` menjadi `.env`:

```env
OPENAI_API_KEY=isi_dengan_api_key_anda_opsional
OPENAI_MODEL=gpt-4o-mini
```

## 8. Langkah Instalasi & Menjalankan Project Secara Lokal

```bash
# 1. Clone repository
git clone <URL_REPO_ANDA>
cd <NAMA_REPO_ANDA>

# 2. Buat virtual environment
python -m venv venv
source venv/bin/activate      # Mac/Linux
# venv\Scripts\activate       # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Salin file environment variable (opsional, lihat bagian 7)
cp .env.example .env

# 5. (Opsional) Bangun ulang knowledge base & embedding dari dataset mentah.
#    Knowledge base & embedding hasil jadi SUDAH tersedia di database/,
#    jadi langkah ini hanya perlu dijalankan bila dataset mentah diganti.
#    PENTING: jalankan dari root folder project ini (bukan dari dalam src/).
python src/preprocessing.py
python src/build_knowledge.py
python src/embedding.py

# 6. Jalankan aplikasi
streamlit run app.py
```

Aplikasi akan terbuka di `http://localhost:8501`.

## 9. Cara Menggunakan / Testing (Evaluasi Model)

Setelah `streamlit run app.py` berjalan, buka `http://localhost:8501`. Ada dua tab:

1. **💬 Chat dengan AI** — ketik pertanyaan bebas, misalnya:
   - `hotel murah dekat Danau Toba di bawah 200 ribu`
   - `rekomendasi kuliner khas Batak di Balige`
   - `transportasi umum dari Medan ke Parapat`

   Jawaban akan menampilkan sumber data (knowledge base) yang dipakai beserta skor relevansinya (klik "📚 sumber data").

2. **🗺️ Buat Itinerary** — isi budget, lama liburan, kota asal, jumlah orang, dan minat, lalu klik **✨ Generate Trip**. Sistem menampilkan rencana per hari, rekomendasi akomodasi & kuliner, serta rincian estimasi biaya (tiket masuk, akomodasi, kuliner, transportasi) dan status terhadap budget yang dimasukkan.

Untuk menguji modul secara terpisah tanpa UI (mis. dari notebook evaluasi):

```bash
cd src
python retrieval.py    # contoh semantic search
python itinerary.py    # contoh generate itinerary + estimasi biaya
python chatbot.py      # contoh RAG chat (mode fallback jika tanpa API key)
```

## 10. Known Issues / Batasan

- Estimasi biaya bersifat perkiraan (rata-rata dari kandidat teratas hasil retrieval), bukan harga real-time — beberapa entri dataset tidak memiliki harga yang bisa diparse sehingga memakai nilai fallback konservatif.
- Sebagian data dataset mentah (ulasan, deskripsi) belum sepenuhnya terintegrasi lintas sumber (mis. tempat yang sama bisa muncul di beberapa sheet dengan penulisan nama sedikit berbeda) — belum ada *entity resolution* penuh pada versi purwarupa ini.
- Tanpa `OPENAI_API_KEY`, jawaban chat & narasi itinerary bersifat ekstraktif (langsung dari knowledge base), bukan generatif penuh — namun tetap akurat karena berbasis data asli.
- Model embedding (`all-MiniLM-L6-v2`) diunduh otomatis saat pertama kali dijalankan sehingga membutuhkan koneksi internet pada run pertama.

---

## 📋 Aturan Submission (Wajib Dibaca & Dipatuhi)
1. **Hak Akses:** Repository harus bersifat **Private**. Peserta **WAJIB** mengundang akun email **aicenter.itdel@gmail.com** sebagai *Collaborator/Viewer* agar juri dapat mengakses kode.
2. **Kesesuaian Instruksi:** Panitia dan juri akan menjalankan _project_ secara lokal murni berdasarkan instruksi di *Langkah Instalasi* pada README ini. Pastikan langkah tersebut valid dan komplit.
3. **Keamanan:** Dilarang keras men-_commit_ API key, _credential_, atau file `.env` asli ke repository.
4. **Kelengkapan Kode:** Sertakan seluruh _source code_ yang relevan. Tidak boleh ada dependensi yang memaksa kode mengambil dari server privat peserta yang tidak bisa diakses panitia.
5. **Batas Waktu:** Perubahan/commit pada _repository_ setelah batas waktu submisi _Preliminary Round_ ditutup tidak akan dinilai, kecuali untuk penyesuaian akses atas permintaan panitia.
