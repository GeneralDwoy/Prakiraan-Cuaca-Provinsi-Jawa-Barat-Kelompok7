import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px

#judul page
st.set_page_config(
    page_title="Prakiraan Cuaca Provinsi Jawa Barat",
    page_icon="awan.png",
    layout="wide"
)

#judul tema
st.title ("Prakiraan Cuaca Provinsi Jawa Barat Periode : 27-01-2026")
st.caption ("Sumber Data : BMKG (Prakiraan Cuaca)")

# Baca Data  CSV
@st.cache_data
def load_data():
    df = pd.read_csv("Prakiraan_cuaca_jabar.csv")
    return df

df = load_data()

# Sidebar
st.sidebar.header("Filter Data Prakiraan Cuaca")

# Filter kota/kab dan cuaca
daftar_kota = ["Semua Kota"] + sorted(df["Kota"].unique().tolist())
pilih_kota = st.sidebar.selectbox("Pilih Kota/Kabupaten",daftar_kota)

daftar_cuaca = ["Semua Cuaca"] + sorted(df["Kondisi Cuaca"].unique().tolist())
pilih_cuaca = st.sidebar.selectbox("Pilih Kondisi Cuaca",daftar_cuaca)

st.sidebar.markdown("-----")
st.sidebar.markdown("Keterangan Warna Cuaca")
st.sidebar.markdown("""
- 🟠 Cerah  
- 🟡 Cerah Berawan  
- 🔘 Berawan  
- 🔵 Hujan Ringan  
- 🟣 Hujan Sedang  
- 🔴 Hujan Lebat  
- ⚫ Hujan Petir
""")

# Filter Data
df_filter = df.copy()

if pilih_kota != "Semua Kota":
    df_filter = df_filter[df_filter["Kota"] == pilih_kota]

if pilih_cuaca != "Semua Cuaca":
    df_filter = df_filter[df_filter["Kondisi Cuaca"] == pilih_cuaca]

# Warna Marker
def warna_marker(kondisi):
    kondisi = kondisi.lower()
    if "cerah" in kondisi and "berawan" not in kondisi:
        return "#FF8C00"
    elif "cerah berawan" in kondisi:
        return "#FFD700"
    elif "berawan" in kondisi:
        return "#808080"
    elif "hujan ringan" in kondisi:
        return "#1E90FF"
    elif "hujan sedang" in kondisi:
        return "#8A2BE2"
    elif "hujan lebat" in kondisi:
        return "#FF0000"
    elif "hujan petir" in kondisi:
        return "#000000"
    else:
        return "#FFFFFF"
    
# folium
st.subheader("Peta Prakiraan Cuaca")
map_jabar = folium.Map(location=[-6.9, 107.6], zoom_start=8)

for _, row in df_filter.iterrows():
    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=5,
        color=warna_marker(row["Kondisi Cuaca"]),
        fill=True,
        fill_opacity=0.8,
        popup=folium.Popup(
            f"""
            <b>{row['Kota']}</b><br>
            <b>Kecamatan</b>       : {row['Kecamatan']}<br>
            <b>Kelurahan</b>       : {row['Kelurahan']}<br><hr>
            <b>Kondisi</b>         : {row['Kondisi Cuaca']}<br>
            <b>Suhu</b>            : {row['Suhu (°C)']} °C<br>
            <b>Kelembapan</b>      : {row['Kelembapan (%)']} %<br>
            <b>Angin</b>           : {row['Kecepatan Angin (km/jam)']} km/jam<br>
            <b>Waktu Prakiraan</b> : {row['Waktu Prakiraan']} <br>
            <b>Latitude</b>        : {row['Latitude']} <br>
            <b>Longitude</b>       : {row['Longitude']} 
            """,
            max_width=350 
        )
    ).add_to(map_jabar)

st_folium(map_jabar, width='stretch', height=500)

# grafik
st.subheader("Statistik Kondisi Cuaca Provinsi Jawa Barat")
warna_cuaca = {
    "Cerah": "#FF8C00",         
    "Cerah Berawan": "#FFD700",  
    "Berawan": "#808080",       
    "Hujan Ringan": "#1E90FF",  
    "Hujan Sedang": "#8A2BE2",  
    "Hujan Lebat": "#FF0000",    
    "Hujan Petir": "#000000"     
}
if not df_filter.empty:
    kondisi_count = (
        df_filter["Kondisi Cuaca"]
        .value_counts()
        .reset_index()
    )
    kondisi_count.columns = ["Kondisi Cuaca", "Jumlah Lokasi"]

    fig = px.bar(
        kondisi_count,
        x="Jumlah Lokasi",
        y="Kondisi Cuaca",
        orientation="h",
        text="Jumlah Lokasi",
        title="Grafik Prakiraan Cuaca",
        color="Kondisi Cuaca",
        color_discrete_map=warna_cuaca
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Jumlah Lokasi",
        yaxis_title="Kondisi Cuaca",
        title_x=0.5,
        showlegend=False,
        height=450
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(fig, width='stretch')

else:
    st.info("Tidak ada data untuk ditampilkan.")

# tabel data + search
st.subheader("Tabel Data Prakiraan Cuaca Provinsi Jawa Barat")

search = st.text_input("Cari Kecamatan dan Kelurahan")
df_tabel = df_filter.copy()

if search:
    df_tabel = df_tabel[
        df_tabel["Kecamatan"].str.contains(search, case=False, na=False) |
        df_tabel["Kelurahan"].str.contains(search, case=False, na=False)
    ]

df_tabel = df_tabel.reset_index(drop=True)
df_tabel.index = df_tabel.index + 1

st.dataframe(
    df_tabel,
    width='stretch'
)

st.caption(f"Total Data Di Tampilkan: {len(df_tabel)}")
