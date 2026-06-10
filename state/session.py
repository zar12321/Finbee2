import streamlit as st


SESSION_DEFAULTS = {
    # Authentication
    "logged_in": False,
    "user_id": None,
    "user_name": "",
    "login_identifier": "",
    "login_type": "",

    # Navigation
    "current_page": "dashboard",

    # AI
    "ai_provider": "Gemini",
    "ai_model": "",
    "api_key": "",

    # Dashboard Filter
    "selected_month": None,
    "selected_year": None,

    # Cache Data
    "transactions_df": None,
    "categories_df": None,

    # Chat History
    "chat_history": [],

    # Theme
    "theme": "dark"
}


def init_session():
    """
    Inisialisasi seluruh session state.
    Dipanggil sekali saat app pertama kali dijalankan.
    """

    for key, value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get(key, default=None):
    """
    Ambil nilai session.
    """

    return st.session_state.get(key, default)


def set(key, value):
    """
    Simpan nilai ke session.
    """

    st.session_state[key] = value


def delete(key):
    """
    Hapus session tertentu.
    """

    if key in st.session_state:
        del st.session_state[key]


def clear_all():
    """
    Hapus seluruh session.
    """

    for key in list(st.session_state.keys()):
        del st.session_state[key]

    init_session()


def is_logged_in():
    """
    Cek status login.
    """

    return st.session_state.get("logged_in", False)


def login_user(user):
    """
    Simpan data user setelah login berhasil.
    """

    st.session_state.logged_in = True
    st.session_state.user_id = user.user_id
    st.session_state.user_name = user.nama
    st.session_state.login_identifier = user.login_identifier
    st.session_state.login_type = user.login_type


def logout_user():
    """
    Logout user.
    """

    auth_keys = [
        "logged_in",
        "user_id",
        "user_name",
        "login_identifier",
        "login_type",
        "api_key",
        "chat_history"
    ]

    for key in auth_keys:
        if key in st.session_state:
            del st.session_state[key]

    init_session()


def get_current_user():
    """
    Ambil informasi user yang sedang login.
    """

    if not is_logged_in():
        return None

    return {
        "user_id": st.session_state.user_id,
        "user_name": st.session_state.user_name,
        "login_identifier": st.session_state.login_identifier,
        "login_type": st.session_state.login_type
    }

def get_current_user_id():
    return st.session_state.get("user_id")


def get_current_user_name():
    return st.session_state.get("user_name")


def append_chat(role, content):
    """
    Tambah riwayat chat AI.
    """

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.session_state.chat_history.append({
        "role": role,
        "content": content
    })


def clear_chat_history():
    """
    Bersihkan riwayat chat.
    """

    st.session_state.chat_history = []