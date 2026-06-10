import streamlit as st

from modules.db import reset_user_password

from state.navigation import navigate

from utils.validation import (
    validate_email,
    validate_username,
    validate_password,
    validate_confirm_password
)

from components.hero_card import render_hero_card


def render_reset_password_page():

    render_hero_card(
        title="Reset Password",
        subtitle="Buat password baru untuk akun FinBee Anda.",
        user_name="Guest",
        emoji="🔑"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown("## Reset Password")

        login_type = st.radio(
            "Jenis Login",
            [
                "Email",
                "Username"
            ],
            horizontal=True
        )

        login_identifier = st.text_input(
            "Email / Username",
            placeholder="Masukkan email atau username"
        )

        new_password = st.text_input(
            "Password Baru",
            type="password"
        )

        confirm_password = st.text_input(
            "Konfirmasi Password Baru",
            type="password"
        )

        col_reset, col_login = st.columns(2)

        with col_reset:

            reset_clicked = st.button(
                "Reset Password",
                use_container_width=True,
                type="primary"
            )

        with col_login:

            login_clicked = st.button(
                "Kembali ke Login",
                use_container_width=True
            )

        if login_clicked:

            navigate("login")

            st.rerun()

        if reset_clicked:

            if login_type == "Email":

                valid, message = validate_email(
                    login_identifier
                )

            else:

                valid, message = validate_username(
                    login_identifier
                )

            if not valid:

                st.error(message)

                return

            valid, message = validate_password(
                new_password
            )

            if not valid:

                st.error(message)

                return

            valid, message = validate_confirm_password(
                new_password,
                confirm_password
            )

            if not valid:

                st.error(message)

                return

            try:

                updated = reset_user_password(
                    login_identifier,
                    new_password
                )

                if updated == 0:

                    st.error(
                        "Akun tidak ditemukan."
                    )

                    return

                st.success(
                    "Password berhasil diperbarui."
                )

                st.toast(
                    "Silakan login menggunakan password baru."
                )

                navigate("login")

                st.rerun()

            except Exception as e:

                st.error(
                    f"Gagal reset password: {str(e)}"
                )