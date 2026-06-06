import streamlit as st
from modules.db import test_connection, load_users, load_categories, load_transactions

st.set_page_config(
    page_title="FinBee",
    page_icon="🐝",
    layout="wide"
)

st.title("🐝 FinBee - Test Koneksi Database")

if st.button("Tes Koneksi PostgreSQL"):
    try:
        result = test_connection()
        st.success(f"Koneksi berhasil. Status: {result.status}")
    except Exception as e:
        st.error(f"Koneksi gagal: {e}")

st.divider()

st.subheader("Data Categories")
try:
    categories_df = load_categories()
    st.dataframe(categories_df, use_container_width=True)
except Exception as e:
    st.error(f"Gagal load categories: {e}")

st.subheader("Data Users")
try:
    users_df = load_users()
    st.dataframe(users_df, use_container_width=True)
except Exception as e:
    st.error(f"Gagal load users: {e}")

st.subheader("Data Transactions")
try:
    transactions_df = load_transactions()
    st.dataframe(transactions_df, use_container_width=True)
except Exception as e:
    st.error(f"Gagal load transactions: {e}")