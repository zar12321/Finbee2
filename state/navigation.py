import streamlit as st


PAGE_ROUTES = {
    # Auth
    "login": "Login",
    "register": "Register",
    "reset_password": "Reset Password",

    # Dashboard
    "dashboard": "Dashboard",
    "tambah_transaksi": "Tambah Transaksi",
    "import_file": "Import File",
    "analisis_prediksi": "Analisis & Prediksi",

    # Profile
    "profil": "Profil Saya",

    # AI
    "ai_home": "AI Home",
    "chatbot": "AI Chatbot",
    "recommendation": "AI Recommendation",
    "ai_settings": "AI Settings"
}


def init_navigation():
    """
    Inisialisasi halaman pertama.
    """

    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"


def navigate(page_name):
    """
    Pindah halaman.
    """

    if page_name not in PAGE_ROUTES:
        raise ValueError(
            f"Halaman '{page_name}' tidak ditemukan."
        )

    st.session_state.current_page = page_name


def current_page():
    """
    Ambil halaman aktif.
    """

    return st.session_state.get(
        "current_page",
        "dashboard"
    )


def get_page_title():
    """
    Ambil nama halaman untuk ditampilkan.
    """

    page = current_page()

    return PAGE_ROUTES.get(
        page,
        "Unknown Page"
    )


def is_page(page_name):
    """
    Cek apakah halaman aktif sama.
    """

    return current_page() == page_name


def get_available_pages():
    """
    Daftar seluruh route.
    """

    return PAGE_ROUTES