import streamlit as st

from modules.db import register_user

from state.navigation import navigate

from utils.validation import (
    validate_name,
    validate_email,
    validate_username,
    validate_password,
    validate_confirm_password
)

from components.hero_card import render_hero_card


def render_register_page():

    render_hero_card(
        title="Create Your FinBee Account",
        subtitle="Mulai perjalanan finansial yang lebih teratur bersama FinBee.",
        user_name="Guest",
        emoji="🐝"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown("## Registrasi Akun")

        nama = st.text_input(
            "Nama Lengkap",
            placeholder="Masukkan nama lengkap"
        )

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

        col_a, col_b = st.columns(2)

        with col_a:

            umur = st.number_input(
                "Umur",
                min_value=0,
                max_value=120,
                value=18
            )

        with col_b:

            pekerjaan = st.text_input(
                "Pekerjaan",
                placeholder="Mahasiswa, Karyawan, dll"
            )

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Konfirmasi Password",
            type="password"
        )

        col_register, col_login = st.columns(2)

        with col_register:

            register_clicked = st.button(
                "Daftar",
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

        if register_clicked:

            valid, message = validate_name(nama)

            if not valid:
                st.error(message)
                return

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
                password
            )

            if not valid:
                st.error(message)
                return

            valid, message = validate_confirm_password(
                password,
                confirm_password
            )

            if not valid:
                st.error(message)
                return

            try:

                register_user(
                    nama=nama.strip(),
                    login_identifier=login_identifier.strip(),
                    login_type=login_type,
                    password=password,
                    umur=int(umur),
                    pekerjaan=pekerjaan.strip()
                )

                st.success(
                    "Registrasi berhasil. Silakan login."
                )

                st.balloons()

                navigate("login")

                st.rerun()

            except Exception as e:

                if "duplicate" in str(e).lower():

                    st.error(
                        "Email atau username sudah digunakan."
                    )

                else:

                    st.error(
                        f"Gagal registrasi: {str(e)}"
                    )