import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Membaca main_data.csv dari folder yang sama dengan dashboard.py
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, "main_data.csv")
all_df = pd.read_csv(data_path)

all_df["order_purchase_timestamp"] = pd.to_datetime(all_df["order_purchase_timestamp"])
all_df["year"] = all_df["order_purchase_timestamp"].dt.year

# Sidebar untuk filter interaktif
st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox("Pilih Tahun Transaksi:", options=[2018, 2017, 2016], index=0)

filtered_df = all_df[all_df["year"] == selected_year]

# Menyiapkan data visualisasi 1
revenue_per_category = filtered_df.groupby('product_category_name_english')['price'].sum().reset_index()

# Menyiapkan data visualisasi 2
customer_by_state = filtered_df.groupby('customer_state')['customer_id'].nunique().reset_index()
customer_by_state = customer_by_state.rename(columns={'customer_id': 'customer_count'})
customer_by_state = customer_by_state.sort_values(by='customer_count', ascending=False)

# Tampilan Utama Dashboard
st.title("E-Commerce Data Analytics Dashboard 📊")
st.text("Created by: I Putu Mahadi Putra Ananta")

st.subheader(f"1. Performa Kategori Produk ({selected_year})")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

top_5 = revenue_per_category.sort_values(by='price', ascending=False).head(5)
sns.barplot(x="price", y="product_category_name_english", data=top_5, palette=colors, ax=ax[0], hue="product_category_name_english", legend=False)
ax[0].set_title("5 Kategori Pendapatan Tertinggi", loc="center", fontsize=15)
ax[0].set_xlabel("Total Pendapatan")
ax[0].set_ylabel(None)

bottom_5 = revenue_per_category.sort_values(by='price', ascending=True).head(5)
sns.barplot(x="price", y="product_category_name_english", data=bottom_5, palette=colors, ax=ax[1], hue="product_category_name_english", legend=False)
ax[1].set_title("5 Kategori Pendapatan Terendah", loc="center", fontsize=15)
ax[1].set_xlabel("Total Pendapatan")
ax[1].set_ylabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()

st.pyplot(fig)

st.subheader(f"2. Demografi Pelanggan - Top 5 Negara Bagian ({selected_year})")
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(x="customer_count", y="customer_state", data=customer_by_state.head(5), palette=colors, hue="customer_state", legend=False, ax=ax2)
ax2.set_title("5 Negara Bagian dengan Pelanggan Terbanyak", fontsize=15)
ax2.set_xlabel("Jumlah Pelanggan")
ax2.set_ylabel("Negara Bagian (State)")
st.pyplot(fig2)

st.caption("Copyright (c) 2026 - Data Analysis Project")
