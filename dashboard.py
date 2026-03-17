import streamlit as st
import pandas as pd

st.title("Dashboard Penjualan")

# =========================
# UPLOAD FILE
# =========================
uploaded_file = st.file_uploader("Upload File Excel", type=["xlsx"])

if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)
else:
    data = pd.read_excel("Penjualan.xlsx")

# =========================
# FILTER TANGGAL
# =========================
data["Tanggal"] = pd.to_datetime(data["Tanggal"])

start_date = st.date_input("Tanggal Awal", data["Tanggal"].min())
end_date = st.date_input("Tanggal Akhir", data["Tanggal"].max())

# filter data sesuai tanggal
filtered_data = data[
    (data["Tanggal"] >= pd.to_datetime(start_date)) &
    (data["Tanggal"] <= pd.to_datetime(end_date))
]

# =========================
# HITUNG TOTAL
# =========================
filtered_data["Total"] = filtered_data["Qty"] * filtered_data["Harga"]

# =========================
# SCORECARD
# =========================
total_omzet = filtered_data["Total"].sum()
total_barang = filtered_data["Qty"].sum()
total_transaksi = len(filtered_data)
total_produk = filtered_data["Nama Barang"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Omzet", f"Rp {total_omzet:,.0f}")
col2.metric("Total Barang Terjual", total_barang)
col3.metric("Total Transaksi", total_transaksi)
col4.metric("Jumlah Produk", total_produk)

st.divider()

# =========================
# TABEL
# =========================
st.subheader("Database Penjualan")
st.dataframe(filtered_data)

st.divider()

# =========================
# CHART 1: Penjualan per Produk
# =========================
st.subheader("Penjualan per Produk")
penjualan_produk = filtered_data.groupby("Nama Barang")["Qty"].sum().sort_values(ascending=False)
st.bar_chart(penjualan_produk)

# =========================
# CHART 2: Omzet per Produk
# =========================
st.subheader("Omzet per Produk")
omzet_produk = filtered_data.groupby("Nama Barang")["Total"].sum().sort_values(ascending=False)
st.bar_chart(omzet_produk)

# =========================
# CHART 3: Omzet per Tanggal
# =========================
st.subheader("Omzet per Tanggal")
penjualan_tanggal = filtered_data.groupby("Tanggal")["Total"].sum()
st.line_chart(penjualan_tanggal)

# =========================
# TOP 5 PRODUK TERLARIS
# =========================
st.subheader("Top 5 Produk Terlaris")
top_produk = penjualan_produk.head(5)
st.table(top_produk)

# =========================
# INSIGHT OTOMATIS
# =========================
produk_terlaris = penjualan_produk.idxmax()
st.success(f"🔥 Produk Terlaris: {produk_terlaris}")