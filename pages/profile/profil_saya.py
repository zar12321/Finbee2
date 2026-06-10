# pages/profile/profil_saya.py

import streamlit as st
import pandas as pd
from datetime import datetime

from modules.db import (
    load_users,
    load_transactions,
    load_monthly_plan,
    save_monthly_plan
)

from state.session import (
    is_logged_in,
    get_current_user_id,
    get_current_user_name,
    get_login_identifier,
    get_login_type
)

from components.hero_card import render_hero_card
from utils.format_currency import format_currency


def render_profile_page():

    if not is_logged_in():

        st.warning(
            "Silakan login terlebih dahulu."
        )

        return

    user_id = get_current_user_id()

    user_name = get_current_user_name()

    login_identifier = get_login_identifier()

    login_type = get_login_type()

    render_hero_card(
        title="Profil Saya",
        subtitle="Kelola informasi akun dan target keuangan bulanan Anda.",
        user_name=user_name,
        emoji="👤"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    try:

        users_df = load_users()

        current_user = users_df[
            users_df["user_id"] == user_id
        ]

        if current_user.empty:

            st.error(
                "Data user tidak ditemukan."
            )

            return

        user_data = current_user.iloc[0]

    except Exception as e:

        st.error(
            f"Gagal memuat profil: {str(e)}"
        )

        return

    # =====================================================
    # PROFILE CARD
    # =====================================================

    st.markdown(
        """
        <div class="profile-card">
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 2])

    with col1:

        st.markdown(
            f"""
            <div style="
                background:#111827;
                border-radius:50%;
                width:140px;
                height:140px;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:50px;
                font-weight:bold;
                margin:auto;
                border:3px solid #22c55e;
            ">
                {user_name[0].upper()}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown("### Informasi Akun")

        st.text_input(
            "Nama Lengkap",
            value=user_data["nama"],
            disabled=True
        )

        st.text_input(
            "Email / Username",
            value=login_identifier,
            disabled=True
        )

        st.text_input(
            "Tipe Login",
            value=login_type,
            disabled=True
        )

        st.text_input(
            "Pekerjaan",
            value=str(
                user_data["pekerjaan"]
            ),
            disabled=True
        )

        st.text_input(
            "Umur",
            value=str(
                user_data["umur"]
            ),
            disabled=True
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # STATISTIK USER
    # =====================================================

    transactions_df = load_transactions()

    transactions_df = transactions_df[
        transactions_df["user_id"] == user_id
    ]

    total_income = transactions_df[
        transactions_df["transaction_type"] == "income"
    ]["amount"].sum()

    total_expense = transactions_df[
        transactions_df["transaction_type"] == "expense"
    ]["amount"].sum()

    balance = total_income - total_expense

    total_transaction = len(
        transactions_df
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Transaksi",
            f"{total_transaction:,}"
        )

    with col2:

        st.metric(
            "Total Pemasukan",
            format_currency(
                total_income
            )
        )

    with col3:

        st.metric(
            "Total Pengeluaran",
            format_currency(
                total_expense
            )
        )

    with col4:

        st.metric(
            "Saldo Bersih",
            format_currency(
                balance
            )
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # TARGET BULANAN
    # =====================================================

    st.subheader(
        "🎯 Target Pengeluaran Bulanan"
    )

    current_month = datetime.now().month

    current_year = datetime.now().year

    current_plan = load_monthly_plan(
        user_id,
        current_month,
        current_year
    )

    current_target = 0

    current_income_plan = 0

    if current_plan:

        current_target = float(
            current_plan.target_bulanan
        )

        current_income_plan = float(
            current_plan.pemasukan_bulanan
        )

    with st.form(
        "monthly_target_form"
    ):

        pemasukan_bulanan = st.number_input(
            "Target Pemasukan Bulanan",
            min_value=0.0,
            value=float(
                current_income_plan
            ),
            step=100000.0
        )

        target_bulanan = st.number_input(
            "Batas Maksimal Pengeluaran",
            min_value=0.0,
            value=float(
                current_target
            ),
            step=100000.0
        )

        submit_target = (
            st.form_submit_button(
                "💾 Simpan Target Bulanan"
            )
        )

    if submit_target:

        try:

            save_monthly_plan(
                user_id=user_id,
                bulan=current_month,
                tahun=current_year,
                target_bulanan=target_bulanan,
                pemasukan_bulanan=pemasukan_bulanan
            )

            st.success(
                "Target bulanan berhasil diperbarui."
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"Gagal menyimpan target: {str(e)}"
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # HISTORY TARGET
    # =====================================================

    st.subheader(
        "📅 Informasi Target Saat Ini"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            f"""
            Bulan:
            {datetime.now().strftime('%B %Y')}
            """
        )

    with col2:

        st.success(
            f"""
            Target:
            {format_currency(current_target)}
            """
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # USER SUMMARY
    # =====================================================

    st.subheader(
        "📈 Ringkasan Keuangan"
    )

    if total_income > 0:

        saving_rate = (
            (balance / total_income)
            * 100
        )

    else:

        saving_rate = 0

    st.markdown(
        f"""
        <div style="
            background:#0f172a;
            padding:20px;
            border-radius:18px;
            border:1px solid #1e293b;
        ">

        <h4>Financial Health Summary</h4>

        <ul>

        <li>
        Total pemasukan:
        <b>{format_currency(total_income)}</b>
        </li>

        <li>
        Total pengeluaran:
        <b>{format_currency(total_expense)}</b>
        </li>

        <li>
        Saldo saat ini:
        <b>{format_currency(balance)}</b>
        </li>

        <li>
        Saving Rate:
        <b>{saving_rate:.2f}%</b>
        </li>

        <li>
        Jumlah transaksi:
        <b>{total_transaction}</b>
        </li>

        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)