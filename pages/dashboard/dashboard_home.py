# pages/dashboard/dashboard_home.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

from modules.db import (
    load_transactions,
    load_monthly_plan
)

from modules.analysis import (
    get_summary_metrics,
    analyze_by_category,
    analyze_by_payment_method,
    get_monthly_trend,
    get_top_transactions
)

from state.session import (
    is_logged_in,
    get_current_user_id,
    get_current_user_name
)

from components.hero_card import render_hero_card
from components.metric_card import render_financial_metrics
from components.chart_card import (
    render_chart_card
)

from utils.format_currency import format_currency


# ==========================================================
# HELPERS
# ==========================================================

def get_status_pengeluaran(total_expense, target):

    if target <= 0:
        return (
            "⚪ Belum Ada Target",
            "#94a3b8",
            0
        )

    percentage = (total_expense / target) * 100

    if percentage <= 80:
        return (
            "🟢 Aman",
            "#22c55e",
            percentage
        )

    elif percentage <= 100:
        return (
            "🟡 Waspada",
            "#eab308",
            percentage
        )

    elif percentage <= 120:
        return (
            "🟠 Melebihi Sedikit",
            "#f97316",
            percentage
        )

    else:
        return (
            "🔴 Melebihi Target",
            "#ef4444",
            percentage
        )


def load_user_transactions():

    user_id = get_current_user_id()

    df = load_transactions()

    if df.empty:
        return df

    df = df[df["user_id"] == user_id]

    return df


# ==========================================================
# MAIN PAGE
# ==========================================================

def render_dashboard_home():

    if not is_logged_in():

        st.warning("Silakan login terlebih dahulu.")
        return

    user_id = get_current_user_id()
    user_name = get_current_user_name()

    render_hero_card(
        title=f"Halo, {user_name}",
        subtitle="Pantau kondisi keuanganmu secara real-time bersama FinBee.",
        user_name=user_name,
        emoji="🐝"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    try:

        transactions_df = load_user_transactions()

    except Exception as e:

        st.error(
            f"Gagal memuat transaksi: {str(e)}"
        )

        return

    metrics = get_summary_metrics(
        transactions_df
    )

    total_income = metrics["total_income"]
    total_expense = metrics["total_expense"]
    balance = metrics["balance"]
    transaction_count = metrics["transaction_count"]

    render_financial_metrics(
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        transaction_count=transaction_count
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ======================================================
    # TARGET BULANAN
    # ======================================================

    current_month = datetime.now().month
    current_year = datetime.now().year

    plan = load_monthly_plan(
        user_id,
        current_month,
        current_year
    )

    target_bulanan = 0

    if plan:
        target_bulanan = float(
            plan.target_bulanan
        )

    status_text, color, percentage = (
        get_status_pengeluaran(
            total_expense,
            target_bulanan
        )
    )

    with st.container(border=True):

        st.subheader(
            "🎯 Target Pengeluaran Bulanan"
        )

        st.metric(
            label="Target",
            value=format_currency(target_bulanan)
        )

        st.markdown(
            f"### :{color}[{status_text}]"
            if color in ["green", "red", "orange", "blue"]
            else f"### {status_text}"
        )

    progress_value = min(
        percentage / 100,
        1.0
    )

    st.progress(progress_value)

    st.caption(
        f"{percentage:.1f}% dari target bulanan"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ======================================================
    # CHARTS
    # ======================================================

    col1, col2 = st.columns(2)

    with col1:

        render_chart_card(
            "Pengeluaran Berdasarkan Kategori"
        )

        category_df = analyze_by_category(
            transactions_df
        )

        if not category_df.empty:

            fig = px.pie(
                category_df,
                values="amount",
                names="category_name",
                hole=0.45
            )

            fig.update_layout(
                height=400
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Belum ada data kategori."
            )


    with col2:

        render_chart_card(
            "Metode Pembayaran"
        )

        payment_df = (
            analyze_by_payment_method(
                transactions_df
            )
        )

        if not payment_df.empty:

            fig = px.bar(
                payment_df,
                x="payment_method",
                y="amount"
            )

            fig.update_layout(
                height=400
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Belum ada data pembayaran."
            )


    st.markdown("<br>", unsafe_allow_html=True)

    # ======================================================
    # TREND BULANAN
    # ======================================================

    render_chart_card(
        "Tren Bulanan"
    )

    trend_df = get_monthly_trend(
        transactions_df
    )

    if not trend_df.empty:

        fig = px.line(
            trend_df,
            x="tanggal_transaksi",
            y="amount",
            color="transaction_type",
            markers=True
        )

        fig.update_layout(
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "Belum ada data tren."
        )


    st.markdown("<br>", unsafe_allow_html=True)

    # ======================================================
    # TOP TRANSAKSI
    # ======================================================

    st.subheader(
        "🏆 Top 5 Transaksi Terbesar"
    )

    top_df = get_top_transactions(
        transactions_df,
        n=5
    )

    if not top_df.empty:

        display_df = top_df[
            [
                "tanggal_transaksi",
                "category_name",
                "tujuan_transaksi",
                "payment_method",
                "amount"
            ]
        ].copy()

        display_df.columns = [
            "Tanggal",
            "Kategori",
            "Tujuan",
            "Metode Pembayaran",
            "Nominal"
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Belum ada transaksi."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ======================================================
    # RECENT ACTIVITY
    # ======================================================

    st.subheader(
        "🕒 Aktivitas Terbaru"
    )

    if not transactions_df.empty:

        recent_df = (
            transactions_df
            .sort_values(
                "tanggal_transaksi",
                ascending=False
            )
            .head(10)
        )

        for _, row in recent_df.iterrows():

            icon = (
                "📈"
                if row["transaction_type"] == "income"
                else "📉"
            )

            st.markdown(
                f"""
                <div style="
                    background:#0f172a;
                    border:1px solid #1e293b;
                    border-radius:12px;
                    padding:14px;
                    margin-bottom:8px;
                ">

                    <b>{icon} {row['category_name']}</b>

                    <br>

                    {row['tujuan_transaksi']}

                    <br>

                    <small>
                    {row['tanggal_transaksi']}
                    </small>

                    <br>

                    <b>
                    {format_currency(row['amount'])}
                    </b>

                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info(
            "Belum ada aktivitas."
        )

    st.markdown("<br><br>", unsafe_allow_html=True)