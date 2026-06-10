# app.py

import streamlit as st

# ==========================================================
# CONFIG
# ==========================================================

from config.settings import (
    APP_NAME,
    APP_ICON,
    APP_LAYOUT,
    APP_SIDEBAR_STATE
)

from config.theme import (
    apply_theme
)

# ==========================================================
# SESSION
# ==========================================================

from state.session import (
    init_session,
    is_logged_in,
    logout_user,
    get_current_user_name
)

# ==========================================================
# COMPONENTS
# ==========================================================

from components.sidebar import (
    render_sidebar
)

from components.navbar import (
    render_navbar
)

from components.footer import (
    render_footer
)

# ==========================================================
# AUTH PAGES
# ==========================================================

from pages.auth.login import (
    render_login_page
)

from pages.auth.register import (
    render_register_page
)

from pages.auth.reset_password import (
    render_reset_password_page
)

# ==========================================================
# DASHBOARD PAGES
# ==========================================================

from pages.dashboard.dashboard_home import (
    render_dashboard_home
)

from pages.dashboard.tambah_transaksi import (
    render_tambah_transaksi
)

from pages.dashboard.import_file import (
    render_import_file
)

from pages.dashboard.analisis_prediksi import (
    render_analisis_prediksi
)

# ==========================================================
# PROFILE PAGE
# ==========================================================

from pages.profile.profil_saya import (
    render_profile_page
)

# ==========================================================
# AI PAGES
# ==========================================================

from pages.ai.ai_home import (
    render_ai_home
)

from pages.ai.chatbot import (
    render_chatbot
)

from pages.ai.recommendation import (
    render_recommendation
)

from pages.ai.settings import (
    render_ai_settings
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout=APP_LAYOUT,
    initial_sidebar_state="expanded"
)

# ==========================================================
# INIT
# ==========================================================

init_session()

apply_theme()

st.markdown(
    """
    <h1 style="color:red;">
        TEST HTML GLOBAL
    </h1>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# HIDE STREAMLIT DEFAULT
# ==========================================================

# ==========================================================
# ROUTER AUTH
# ==========================================================

if not is_logged_in():

    page = st.session_state.get(
        "current_page",
        "login"
    )

    if page == "login":

        render_login_page()

    elif page == "register":

        render_register_page()

    elif page == "reset_password":

        render_reset_password_page()

    else:

        render_login_page()

    st.stop()

# ==========================================================
# SIDEBAR
# ==========================================================
st.sidebar.markdown("# SIDEBAR TEST")
selected_page = render_sidebar()

# ==========================================================
# NAVBAR
# ==========================================================

user_name = get_current_user_name()

render_navbar(user_name)

# ==========================================================
# DASHBOARD MENU
# ==========================================================

if selected_page == "dashboard":

    render_dashboard_home()

elif selected_page == "tambah_transaksi":

    render_tambah_transaksi()

elif selected_page == "import_file":

    render_import_file()

elif selected_page == "analisis_prediksi":

    render_analisis_prediksi()

# ==========================================================
# PROFILE MENU
# ==========================================================

elif selected_page == "Profil Saya":

    render_profile_page()

# ==========================================================
# AI MENU
# ==========================================================

elif selected_page == "AI Home":

    render_ai_home()

elif selected_page == "AI Chatbot":

    render_chatbot()

elif selected_page == "AI Recommendation":

    render_recommendation()

elif selected_page == "AI Settings":

    render_ai_settings()

# ==========================================================
# LOGOUT
# ==========================================================

elif selected_page == "Logout":

    logout_user()

    st.success(
        "Logout berhasil."
    )

    st.rerun()

# ==========================================================
# FOOTER
# ==========================================================

render_footer()