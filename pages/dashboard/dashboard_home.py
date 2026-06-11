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

    # ======================================================
    # FILTER BULAN & TAHUN
    # ======================================================

    filter_col1, filter_col2 = st.columns([2,1])

    with filter_col1:

        selected_month = st.selectbox(
            "📅 Bulan",
            options=list(range(1,13)),
            index=datetime.now().month - 1,
            format_func=lambda x: datetime(
                2026,
                x,
                1
            ).strftime("%B")
        )

    with filter_col2:

        selected_year = st.selectbox(
            "📆 Tahun",
            options=[
                datetime.now().year - 1,
                datetime.now().year,
                datetime.now().year + 1
            ],
            index=1
        )

    render_hero_card(
        title=f"Halo, {user_name}",
        subtitle="Pantau kondisi keuanganmu secara real-time bersama FinBee.",
        user_name=user_name,
        emoji="🐝"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    try:

        transactions_df = load_user_transactions()
        
        if not transactions_df.empty:

            transactions_df["tanggal_transaksi"] = pd.to_datetime(
                transactions_df["tanggal_transaksi"]
            )

            transactions_df = transactions_df[
                (
                    transactions_df["tanggal_transaksi"].dt.month
                    == selected_month
                )
                &
                (
                    transactions_df["tanggal_transaksi"].dt.year
                    == selected_year
                )
            ]

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

    avg_transaction = (
        total_expense / transaction_count
        if transaction_count > 0 
        else 0
    )

    days_in_month = max(
        datetime.now().day,
        1
    )

    avg_daily = (
        total_expense / days_in_month
    )

    render_financial_metrics(
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        transaction_count=transaction_count, 
        avg_transaction=avg_transaction, 
        avg_daily=avg_daily
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
                hole=0.65
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent+label" 
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                showlegend=True,
                margin=dict(
                    l=0,
                    r=0,
                    t=20,
                    b=0
                ),
                height=350
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
                y="amount",
                text="amount"
            )

            fig.update_traces(
                textposition="outside"
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                xaxis_title="",
                yaxis_title="Total Pengeluaran",
                showlegend=False,
                margin=dict(
                    l=0,
                    r=0,
                    t=20,
                    b=0
                ),
                height=350
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
    # CASH FLOW TIMELINE
    # ======================================================

    render_chart_card(
        "📈 Cash Flow Timeline"
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

        colors = {
            "income": "#22C55E",
            "expense": "#EF4444"
        }

        for trace in fig.data:

            if trace.name in colors:

                trace.line.color = colors[
                    trace.name
                ]

                trace.marker.color = colors[
                    trace.name
                ]

                trace.line.width = 5

                trace.marker.size = 10

        fig.update_layout(

            height=500,

            paper_bgcolor="#08130D",
            plot_bgcolor="#08130D",

            font_color="white",

            hovermode="x unified",

            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            ),

            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),

            xaxis=dict(
                title="",
                showgrid=False,
                zeroline=False
            ),

            yaxis=dict(
                title="Nominal",
                gridcolor="rgba(255,255,255,0.08)",
                zeroline=False
            )
        )

        fig.update_xaxes(
            tickformat="%d %b"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "Belum ada data tren."
        )

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )

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
        )

        # ==========================================
        # FILTER
        # ==========================================

        filter1, filter2 = st.columns(2)

        with filter1:

            periode = st.selectbox(
                "📅 Periode",
                [
                    "Hari Ini",
                    "7 Hari Terakhir",
                    "30 Hari Terakhir",
                    "Semua"
                ]
            )

        with filter2:

            kategori_filter = st.multiselect(
                "📂 Kategori",
                sorted(
                    recent_df["category_name"]
                    .dropna()
                    .unique()
                )
            )

        filter3, filter4 = st.columns(2)

        with filter3:

            metode_filter = st.multiselect(
                "💳 Metode Pembayaran",
                sorted(
                    recent_df["payment_method"]
                    .dropna()
                    .unique()
                )
            )

        with filter4:

            tipe_filter = st.multiselect(
                "📊 Jenis",
                [
                    "income",
                    "expense"
                ],
                default=[
                    "income",
                    "expense"
                ]
            )

        search_text = st.text_input(
            "🔍 Cari tujuan transaksi"
        )

        # ==========================================
        # FILTERING
        # ==========================================

        filtered_df = recent_df.copy()

        today = pd.Timestamp.now().normalize()

        if periode == "Hari Ini":

            filtered_df = filtered_df[
                filtered_df["tanggal_transaksi"].dt.normalize()
                == today
            ]

        elif periode == "7 Hari Terakhir":

            filtered_df = filtered_df[
                filtered_df["tanggal_transaksi"]
                >= today - pd.Timedelta(days=7)
            ]

        elif periode == "30 Hari Terakhir":

            filtered_df = filtered_df[
                filtered_df["tanggal_transaksi"]
                >= today - pd.Timedelta(days=30)
            ]

        filtered_df = filtered_df[
            filtered_df["transaction_type"]
            .isin(tipe_filter)
        ]

        if kategori_filter:

            filtered_df = filtered_df[
                filtered_df["category_name"]
                .isin(kategori_filter)
            ]

        if metode_filter:

            filtered_df = filtered_df[
                filtered_df["payment_method"]
                .isin(metode_filter)
            ]

        if search_text:

            filtered_df = filtered_df[
                filtered_df["tujuan_transaksi"]
                .str.contains(
                    search_text,
                    case=False,
                    na=False
                )
            ]

        # ==========================================
        # SUMMARY
        # ==========================================

        income_filtered = (
            filtered_df[
                filtered_df["transaction_type"]
                == "income"
            ]["amount"]
            .sum()
        )

        expense_filtered = (
            filtered_df[
                filtered_df["transaction_type"]
                == "expense"
            ]["amount"]
            .sum()
        )

        summary1, summary2, summary3, summary4 = st.columns(4)

        with summary1:
            st.metric(
                "💰 Income",
                format_currency(income_filtered)
            )

        with summary2:
            st.metric(
                "📉 Expense",
                format_currency(expense_filtered)
            )

        with summary3:
            st.metric(
                "🏦 Balanced",
                format_currency(
                    income_filtered -
                    expense_filtered
                )
            )

        with summary4:
            st.metric(
                "📋 Transactions",
                len(filtered_df)
            )

        st.markdown("---")

        # ==========================================
        # LIST TRANSAKSI
        # ==========================================

        if not filtered_df.empty:

            for _, row in filtered_df.iterrows():

                icon = (
                    "📈"
                    if row["transaction_type"] == "income"
                    else "📉"
                )

                with st.container(border=True):

                    col1, col2 = st.columns(
                        [4,1]
                    )

                    with col1:

                        st.markdown(
                            f"""
                            <div style="
                                font-size:30px;
                                font-weight:800;
                                color:white;
                                margin-bottom:12px;
                            ">
                                {icon} {row['category_name']}
                            </div>

                            <div style="
                                font-size:24px;
                                font-weight:700;
                                color:#E2E8F0;
                                margin-bottom:14px;
                            ">
                                {row['tujuan_transaksi']}
                            </div>

                            <div style="
                                font-size:18px;
                                color:#CBD5E1;
                                line-height:1.7;
                                margin-bottom:22px;
                            ">
                                {row['keterangan']}
                            </div>

                            <div style="
                                font-size:18px;
                                font-weight:600;
                                color:#CBD5E1;
                                margin-bottom:12px;
                            ">
                                💳 {row['payment_method']}
                            </div>

                            <div style="
                                font-size:21px;
                                color:#94A3B8;
                                margin-bottom:30px;
                            ">
                                📅 {row['tanggal_transaksi'].strftime('%d %B %Y')}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                                        
                    with col2:

                        st.metric(
                            "Nominal",
                            format_currency(
                                row["amount"]
                            )
                        )

        else:

            st.info(
                "Tidak ada transaksi sesuai filter."
            )

    else:

        st.info(
            "Belum ada aktivitas."
        )