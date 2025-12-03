````
# Dashboard Prediksi Curah Hujan & Risiko Banjir

Aplikasi Streamlit untuk memantau curah hujan di beberapa stasiun, memprediksi nilai ke depan dengan regresi linear, dan mengkaitkannya dengan tingkat risiko banjir per wilayah.

## Fitur

- Filter interaktif berdasarkan wilayah, tahun, dan bulan.
- Prediksi curah hujan per kombinasi tahun–bulan menggunakan `LinearRegression`.
- Klasifikasi risiko banjir sederhana (rendah/sedang/tinggi) berdasar hasil prediksi.
- Tabel dan grafik prediksi, serta tabel agregasi kejadian banjir historis.

## Struktur Data

- `curah_hujan_stasiun_cisadea_cibareno.csv` dan `curah_hujan_stasiun_citarum.csv`
  Kolom utama: `tahun`, `bulan`, `jumlah_curah_hujan`.
- `banjir.csv`
  Kolom: `tahun`, `wilayah`, `jumlah_kejadian`.

Pastikan nama kolom tetap konsisten agar proses pemrosesan berjalan.

## Persyaratan

- Python 3.10+
- Dependencies pada `requirements.txt` (Streamlit, pandas, scikit-learn, matplotlib, dll.)

Install:

```bash
pip install -r requirements.txt
````

## Menjalankan Aplikasi

```bash
streamlit run app.py
```

Secara default Streamlit berjalan di `http://localhost:8501`.

## Catatan

- Fungsi `load_data()` saat ini membaca dua file stasiun secara terpisah tetapi variabelnya tertimpa; gabungkan `df_stasiun` bila ingin memakai kedua dataset.
- Mapping bulan sudah disediakan; pastikan nama bulan di CSV memakai huruf kapital agar konversi sukses.
- Model regresi linear sederhana; pertimbangkan metode lain bila akurasi kurang.

```

```
