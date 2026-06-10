import streamlit as st

from state.navigation import navigate
from state.navigation import current_page


def render_sidebar():

    with st.sidebar:

        st.markdown("## 🐝 FinBee")

        if st.button("🏠 Dashboard"):
            navigate("dashboard")

        if st.button("➕ Tambah Transaksi"):
            navigate("tambah_transaksi")

        if st.button("📂 Import File"):
            navigate("import_file")

        if st.button("📊 Analisis"):
            navigate("analisis_prediksi")

        st.divider()

        if st.button("👤 Profil"):
            navigate("profil")

        st.divider()

        if st.button("🤖 AI Home"):
            navigate("ai_home")

        if st.button("💬 Chatbot"):
            navigate("chatbot")

        if st.button("🧠 Recommendation"):
            navigate("recommendation")

        if st.button("⚙️ AI Settings"):
            navigate("ai_settings")