import streamlit as st
from modules.db import (
    test_connection,
    load_users,
    load_categories,
    load_transactions,
    insert_user
)

st.set_page_config(
    page_title="FinBee",
    page_icon="🐝",
    layout="wide"
)

# =========================
# SESSION STATE DEFAULT
# =========================

if "main_page" not in st.session_state:
    st.session_state.main_page = "Dashboard"

if "dashboard_page" not in st.session_state:
    st.session_state.dashboard_page = "Home Dashboard"

if "insight_page" not in st.session_state:
    st.session_state.insight_page = "Home Insight AI"


# =========================
# SIDEBAR UTAMA
# =========================

st.sidebar.title("🐝 FinBee")

main_page = st.sidebar.radio(
    "Menu Utama",
    ["Dashboard", "Insight AI"],
    index=["Dashboard", "Insight AI"].index(st.session_state.main_page)
)

st.session_state.main_page = main_page


# =========================
# TOMBOL KEMBALI
# =========================

def back_to_dashboard_home():
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.dashboard_page = "Home Dashboard"
        st.rerun()


def back_to_insight_home():
    if st.button("⬅️ Kembali ke Insight AI"):
        st.session_state.insight_page = "Home Insight AI"
        st.rerun()


# =========================
# DASHBOARD HOME
# =========================

def dashboard_home():
    st.title("🐝 FinBee Dashboard")
    st.write("Pilih fitur yang ingin digunakan.")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("👤 Profil User", use_container_width=True):
            st.session_state.dashboard_page = "Profil User"
            st.rerun()

    with col2:
        if st.button("➕ Tambah Transaksi", use_container_width=True):
            st.session_state.dashboard_page = "Tambah Transaksi"
            st.rerun()

    with col3:
        if st.button("📁 Import File", use_container_width=True):
            st.session_state.dashboard_page = "Import File"
            st.rerun()

    with col4:
        if st.button("📊 Analisis & Prediksi", use_container_width=True):
            st.session_state.dashboard_page = "Analisis & Prediksi"
            st.rerun()

    st.divider()

    st.subheader("Status Database")

    try:
        result = test_connection()
        st.success(f"Koneksi PostgreSQL berhasil. Status: {result.status}")
    except Exception as e:
        st.error(f"Koneksi PostgreSQL gagal: {e}")

    st.subheader("Ringkasan Data")

    try:
        users_df = load_users()
        categories_df = load_categories()
        transactions_df = load_transactions()

        col_a, col_b, col_c = st.columns(3)

        col_a.metric("Jumlah User", len(users_df))
        col_b.metric("Jumlah Kategori", len(categories_df))
        col_c.metric("Jumlah Transaksi", len(transactions_df))

    except Exception as e:
        st.error(f"Gagal memuat ringkasan data: {e}")


# =========================
# HALAMAN PROFIL USER
# =========================

def page_profil_user():
    back_to_dashboard_home()

    st.title("👤 Profil User")
    st.write("Tambahkan user yang akan menggunakan aplikasi FinBee.")

    with st.form("form_tambah_user"):
        nama = st.text_input("Nama User")
        umur = st.number_input("Umur", min_value=0, max_value=120, step=1)
        pekerjaan = st.text_input("Pekerjaan")
        pemasukan_bulanan = st.number_input(
            "Pemasukan Bulanan",
            min_value=0.0,
            step=10000.0
        )
        target_tabungan = st.number_input(
            "Target Tabungan",
            min_value=0.0,
            step=10000.0
        )

        submitted = st.form_submit_button("Simpan User")

        if submitted:
            if nama.strip() == "":
                st.warning("Nama user tidak boleh kosong.")
            else:
                try:
                    insert_user(
                        nama=nama,
                        umur=umur,
                        pekerjaan=pekerjaan,
                        pemasukan_bulanan=pemasukan_bulanan,
                        target_tabungan=target_tabungan
                    )

                    st.success("User berhasil ditambahkan.")
                    st.rerun()

                except Exception as e:
                    st.error(f"Gagal menambahkan user: {e}")

    st.divider()

    st.subheader("Daftar User")

    try:
        users_df = load_users()

        if users_df.empty:
            st.info("Belum ada user.")
        else:
            st.dataframe(users_df, use_container_width=True)

    except Exception as e:
        st.error(f"Gagal memuat data user: {e}")


# =========================
# HALAMAN PLACEHOLDER
# =========================

def page_tambah_transaksi():
    back_to_dashboard_home()
    st.title("➕ Tambah Transaksi")
    st.info("Tahap berikutnya: membuat form tambah transaksi.")


def page_import_file():
    back_to_dashboard_home()
    st.title("📁 Import File")
    st.info("Tahap berikutnya: membuat fitur upload CSV/Excel/PDF/TXT.")


def page_analisis_prediksi():
    back_to_dashboard_home()
    st.title("📊 Analisis & Prediksi")

    pilihan = st.selectbox(
        "Pilih jenis analisis",
        [
            "Analisis Kategori",
            "Analisis Metode Pembayaran",
            "Tren Bulanan",
            "Prediksi Bulan Depan"
        ]
    )

    st.info(f"Fitur {pilihan} akan dibuat setelah transaksi berhasil disimpan.")


# =========================
# INSIGHT AI HOME
# =========================

def insight_home():
    st.title("🤖 Insight AI")
    st.write("Pilih fitur AI yang ingin digunakan.")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⚙️ Pengaturan", use_container_width=True):
            st.session_state.insight_page = "Pengaturan"
            st.rerun()

    with col2:
        if st.button("💬 Chatbot AI", use_container_width=True):
            st.session_state.insight_page = "Chatbot AI"
            st.rerun()

    with col3:
        if st.button("🧠 Rekomendasi AI", use_container_width=True):
            st.session_state.insight_page = "Rekomendasi AI"
            st.rerun()


def page_pengaturan():
    back_to_insight_home()
    st.title("⚙️ Pengaturan AI")
    st.info("Tahap berikutnya: input provider AI, model, dan API key user.")


def page_chatbot_ai():
    back_to_insight_home()
    st.title("💬 Chatbot AI")
    st.info("Tahap berikutnya: membuat chatbot berbasis ringkasan transaksi.")


def page_rekomendasi_ai():
    back_to_insight_home()
    st.title("🧠 Rekomendasi AI")
    st.info("Tahap berikutnya: membuat rekomendasi finansial berbasis data.")


# =========================
# ROUTING UTAMA
# =========================

if st.session_state.main_page == "Dashboard":

    if st.session_state.dashboard_page == "Home Dashboard":
        dashboard_home()

    elif st.session_state.dashboard_page == "Profil User":
        page_profil_user()

    elif st.session_state.dashboard_page == "Tambah Transaksi":
        page_tambah_transaksi()

    elif st.session_state.dashboard_page == "Import File":
        page_import_file()

    elif st.session_state.dashboard_page == "Analisis & Prediksi":
        page_analisis_prediksi()


elif st.session_state.main_page == "Insight AI":

    if st.session_state.insight_page == "Home Insight AI":
        insight_home()

    elif st.session_state.insight_page == "Pengaturan":
        page_pengaturan()

    elif st.session_state.insight_page == "Chatbot AI":
        page_chatbot_ai()

    elif st.session_state.insight_page == "Rekomendasi AI":
        page_rekomendasi_ai()