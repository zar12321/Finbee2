import streamlit as st
import pandas as pd

from modules.import_file import (
    auto_clean_financial_file
)

from modules.db import (
    insert_imported_transactions
)

from state.session import (
    get_current_user_id,
    is_logged_in
)


def render_import_file():

    if not is_logged_in():
        st.warning("Silakan login terlebih dahulu.")
        return

    st.title("📂 Import File Transaksi")

    uploaded_file = st.file_uploader(
        "Upload CSV atau Excel",
        type=[
            "csv",
            "xlsx",
            "xls"
        ]
    )

    if uploaded_file is None:
        return

    try:

        if uploaded_file.name.endswith(".csv"):

            raw_df = pd.read_csv(
                uploaded_file
            )

        else:

            raw_df = pd.read_excel(
                uploaded_file
            )

        st.subheader("Preview Data Asli")

        st.dataframe(
            raw_df.head(20),
            use_container_width=True
        )

        cleaned_df = (
            auto_clean_financial_file(
                raw_df
            )
        )

        st.subheader(
            "Preview Hasil Cleaning"
        )

        st.dataframe(
            cleaned_df.head(20),
            use_container_width=True
        )

        st.metric(
            "Jumlah Transaksi",
            len(cleaned_df)
        )

        if st.button(
            "🚀 Import ke Database",
            use_container_width=True
        ):

            insert_imported_transactions(
                get_current_user_id(),
                cleaned_df
            )

            st.success(
                f"{len(cleaned_df)} transaksi berhasil diimport."
            )

            st.balloons()

    except Exception as e:

        st.error(
            f"Gagal import file: {str(e)}"
        )