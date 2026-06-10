import streamlit as st

from modules.db import login_user_by_identifier

from state.session import login_user
from state.navigation import navigate

from utils.validation import (
    validate_password
)

from components.hero_card import render_hero_card


def render_login_page():

    st.markdown(
        """
        <div class="auth-page">
        """,
        unsafe_allow_html=True
    )

    render_hero_card(
        title="Welcome Back",
        subtitle="Masuk ke akun FinBee dan kelola keuanganmu dengan lebih cerdas.",
        user_name="Guest",
        emoji="🔐"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown(
            """
            <div class="auth-card">
            <h2>Login</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        login_identifier = st.text_input(
            label="Email atau Username",
            placeholder="Masukkan email atau username",
            key="login_identifier_input"
        )

        password = st.text_input(
            label="Password",
            type="password",
            placeholder="Masukkan password",
            key="login_password"
        )

        col_login, col_reset = st.columns(2)

        with col_login:

            login_clicked = st.button(
                "Masuk",
                use_container_width=True,
                type="primary"
            )

        with col_reset:

            reset_clicked = st.button(
                "Lupa Password",
                use_container_width=True
            )

        register_clicked = st.button(
            "Belum punya akun? Register",
            use_container_width=True
        )

        if reset_clicked:
            navigate("reset_password")
            st.rerun()

        if register_clicked:
            navigate("register")
            st.rerun()

        if login_clicked:

            if not login_identifier.strip():

                st.error(
                    "Email atau username wajib diisi."
                )

                return

            valid_password, message = validate_password(
                password
            )

            if not valid_password:

                st.error(message)

                return

            try:

                user = login_user_by_identifier(
                    login_identifier,
                    password
                )

                if user is None:

                    st.error(
                        "Username/email atau password salah."
                    )

                    return

                login_user(user)

                st.success(
                    f"Selamat datang kembali, {user.nama}"
                )

                navigate("dashboard")

                st.rerun()

            except Exception as e:

                st.error(
                    f"Gagal login: {str(e)}"
                )