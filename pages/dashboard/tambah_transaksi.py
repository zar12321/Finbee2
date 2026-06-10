import streamlit as st
import pandas as pd

from modules.db import (
    load_categories,
    insert_transaction
)

from state.session import (
    is_logged_in,
    get_current_user_id
)

from utils.format_currency import (
    format_currency
)


def render_tambah_transaksi():

    if not is_logged_in():
        st.warning("Silakan login terlebih dahulu.")
        return

    st.title("➕ Tambah Transaksi")

    user_id = get_current_user_id()

    categories_df = load_categories()

    if categories_df.empty:
        st.error("Kategori belum tersedia.")
        return

    with st.form("form_tambah_transaksi"):

        col1, col2 = st.columns(2)

        with col1:

            tanggal_transaksi = st.date_input(
                "Tanggal Transaksi"
            )

            transaction_type = st.selectbox(
                "Tipe Transaksi",
                [
                    "expense",
                    "income"
                ]
            )

            category_type = (
                "expense"
                if transaction_type == "expense"
                else "income"
            )

            filtered_categories = (
                categories_df[
                    categories_df["category_type"]
                    == category_type
                ]
            )

            category_name = st.selectbox(
                "Kategori",
                filtered_categories["category_name"]
            )

        with col2:

            payment_method = st.selectbox(
                "Metode Pembayaran",
                [
                    "Cash",
                    "BCA",
                    "BRI",
                    "BNI",
                    "Mandiri",
                    "Dana",
                    "OVO",
                    "GoPay",
                    "ShopeePay",
                    "Lainnya"
                ]
            )

            tujuan_transaksi = st.text_input(
                "Tujuan Transaksi"
            )

        keterangan = st.text_area(
            "Keterangan"
        )

        amount = st.number_input(
            "Nominal",
            min_value=0.0,
            step=1000.0
        )

        submitted = st.form_submit_button(
            "💾 Simpan Transaksi"
        )

    if submitted:

        if amount <= 0:

            st.error(
                "Nominal harus lebih dari 0."
            )
            return

        category_id = int(
            filtered_categories[
                filtered_categories[
                    "category_name"
                ] == category_name
            ]["category_id"].iloc[0]
        )

        try:

            insert_transaction(
                user_id=user_id,
                category_id=category_id,
                tanggal_transaksi=tanggal_transaksi,
                transaction_type=transaction_type,
                tujuan_transaksi=tujuan_transaksi,
                keterangan=keterangan,
                payment_method=payment_method,
                amount=amount,
                source="manual",
                raw_category=category_name
            )

            st.success(
                "Transaksi berhasil disimpan."
            )

            st.balloons()

        except Exception as e:

            st.error(
                f"Gagal menyimpan transaksi: {str(e)}"
            )