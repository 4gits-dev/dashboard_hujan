import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# --------------------------------------------
# Load Dataset
# --------------------------------------------
@st.cache_data
def load_data():
    # Dataset stasiun hujan
    df_stasiun = pd.read_csv("curah_hujan_stasiun_cisadea_cibareno.csv")
    df_stasiun['wilayah'] = 'Bogor'  # sesuaikan wilayah
    
    df_stasiun = pd.read_csv("curah_hujan_stasiun_citarum.csv")
    df_stasiun['wilayah'] = 'Bandung'  # sesuaikan wilayah
    
    # Mapping bulan ke angka
    bulan_mapping = {
        "JANUARI": 1, "FEBRUARI": 2, "MARET": 3, "APRIL": 4,
        "MEI": 5, "JUNI": 6, "JULI": 7, "AGUSTUS": 8,
        "SEPTEMBER": 9, "OKTOBER": 10, "NOVEMBER": 11, "DESEMBER": 12
    }
    df_stasiun['bulan'] = df_stasiun['bulan'].str.upper().map(bulan_mapping)
    
    # Hapus baris NaN di 'bulan' atau 'curah_hujan'
    df_stasiun = df_stasiun.dropna(subset=['bulan','jumlah_curah_hujan'])
    
    # Dataset kejadian banjir (hanya tahun dan jumlah_kejadian)
    df_banjir = pd.read_csv("banjir.csv")  # kolom: tahun, wilayah, jumlah_kejadian
    
    return df_stasiun, df_banjir

df_stasiun, df_banjir = load_data()

# --------------------------------------------
# Sidebar: Filter Wilayah, Tahun, Bulan
# --------------------------------------------
st.sidebar.title("Filter Data")
wilayah_options = df_stasiun['wilayah'].unique()
selected_wilayah = st.sidebar.multiselect("Pilih Wilayah:", options=wilayah_options, default=wilayah_options)

year_options = list(range(2015,2031))
selected_years = st.sidebar.multiselect("Pilih Tahun:", options=year_options, default=year_options)

bulan_mapping_display = {
    "Januari":1, "Februari":2, "Maret":3, "April":4,
    "Mei":5, "Juni":6, "Juli":7, "Agustus":8,
    "September":9, "Oktober":10, "November":11, "Desember":12
}
selected_months = st.sidebar.multiselect("Pilih Bulan:", options=list(bulan_mapping_display.keys()), default=list(bulan_mapping_display.keys()))

# Filter data stasiun sesuai pilihan
df_filtered = df_stasiun[
    (df_stasiun['wilayah'].isin(selected_wilayah)) &
    (df_stasiun['tahun'].isin(selected_years)) &
    (df_stasiun['bulan'].isin([bulan_mapping_display[m] for m in selected_months]))
]

# --------------------------------------------
# Fungsi Risiko Banjir
# --------------------------------------------
def risiko_banjir(mm):
    if mm < 100:
        return "Rendah"
    elif mm < 200:
        return "Sedang"
    else:
        return "Tinggi"

# --------------------------------------------
# Prediksi Curah Hujan per Wilayah
# --------------------------------------------
st.subheader("Prediksi Curah Hujan dan Risiko Banjir")

pred_dfs = []

for wilayah in selected_wilayah:
    df_w = df_stasiun[df_stasiun['wilayah']==wilayah]
    
    if df_w.empty:
        continue
    
    # Linear Regression: curah_hujan ~ tahun + bulan
    X = df_w[['tahun','bulan']]
    y = df_w['jumlah_curah_hujan']
    
    # Hapus baris NaN jika masih ada
    mask = X.notna().all(axis=1) & y.notna()
    X = X[mask]
    y = y[mask]
    
    if len(y) == 0:
        continue  # skip jika tidak ada data
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Prediksi curah hujan untuk pilihan tahun & bulan
    pred_input = pd.DataFrame([
        {'tahun': y_, 'bulan': bulan_mapping_display[m]} 
        for y_ in selected_years
        for m in selected_months
    ])
    pred_values = model.predict(pred_input)
    pred_input['curah_hujan_prediksi'] = pred_values
    pred_input['wilayah'] = wilayah
    pred_input['risiko_banjir'] = pred_input['curah_hujan_prediksi'].apply(risiko_banjir)
    
    pred_dfs.append(pred_input)

# Gabungkan prediksi semua wilayah
if pred_dfs:
    pred_df = pd.concat(pred_dfs, ignore_index=True)
    st.dataframe(pred_df[['tahun','bulan','wilayah','curah_hujan_prediksi','risiko_banjir']])
else:
    st.warning("Tidak ada data prediksi untuk wilayah/tahun/bulan yang dipilih.")

# --------------------------------------------
# Grafik Prediksi Curah Hujan
# --------------------------------------------
st.subheader("Grafik Prediksi Curah Hujan")
plt.figure(figsize=(10,5))
for wilayah in selected_wilayah:
    df_plot = pred_df[pred_df['wilayah']==wilayah]
    plt.plot(df_plot['bulan'], df_plot['curah_hujan_prediksi'], marker='o', label=wilayah)

plt.xlabel("Bulan")
plt.ylabel("Curah Hujan Prediksi (mm)")
plt.title("Prediksi Curah Hujan Per Wilayah")
plt.legend()
st.pyplot(plt)

# --------------------------------------------
# Analisis Banjir Berdasarkan Tahun
# --------------------------------------------
st.subheader("Data Kejadian Banjir (Per Tahun)")

df_banjir_filtered = df_banjir[
    (df_banjir['tahun'].isin(selected_years))
]

if not df_banjir_filtered.empty:
    st.dataframe(df_banjir_filtered)
else:
    st.info("Tidak ada data kejadian banjir untuk filter saat ini.")
