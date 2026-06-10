import streamlit as st
import plotly.express as px

from modules.db import (
    load_transactions
)

from modules.analysis import (
    analyze_by_category,
    analyze_by_payment_method,
    get_monthly_trend,
    get_top_transactions
)

from modules.prediction import (
    predict_next_month_expense
)

from state.session import (
    get_current_user_id,
    is_logged_in
)

from utils.format_currency import (
    format_currency
)


def render_analisis_prediksi():

    if not is_logged_in():
        st.warning(
            "Silakan login terlebih dahulu."
        )
        return

    st.title(
        "📊 Analisis & Prediksi"
    )

    user_id = get_current_user_id()

    df = load_transactions()

    df = df[
        df["user_id"] == user_id
    ]

    if df.empty:

        st.info(
            "Belum ada data transaksi."
        )

        return

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Kategori",
            "Pembayaran",
            "Tren",
            "Prediksi"
        ]
    )

    # ==========================
    # KATEGORI
    # ==========================

    with tab1:

        category_df = (
            analyze_by_category(df)
        )

        fig = px.pie(
            category_df,
            names="category_name",
            values="amount",
            hole=0.4
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            category_df,
            use_container_width=True
        )

    # ==========================
    # PAYMENT
    # ==========================

    with tab2:

        payment_df = (
            analyze_by_payment_method(df)
        )

        fig = px.bar(
            payment_df,
            x="payment_method",
            y="amount"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            payment_df,
            use_container_width=True
        )

    # ==========================
    # TREND
    # ==========================

    with tab3:

        trend_df = (
            get_monthly_trend(df)
        )

        fig = px.line(
            trend_df,
            x="tanggal_transaksi",
            y="amount",
            color="transaction_type",
            markers=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        top_df = (
            get_top_transactions(
                df,
                10
            )
        )

        st.subheader(
            "Top 10 Transaksi"
        )

        st.dataframe(
            top_df,
            use_container_width=True
        )

    # ==========================
    # PREDIKSI
    # ==========================

    with tab4:

        prediction = (
            predict_next_month_expense(
                df
            )
        )

        st.metric(
            "Prediksi Bulan Depan",
            format_currency(
                prediction["prediction"]
            )
        )

        st.info(
            prediction["message"]
        )

        monthly_df = (
            prediction[
                "monthly_data"
            ]
        )

        if not monthly_df.empty:

            fig = px.line(
                monthly_df,
                x="bulan",
                y="total_pengeluaran",
                markers=True
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.success(
            f"Metode Prediksi: {prediction['method']}"
        )