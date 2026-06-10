import streamlit as st

from state.session import (
    get
)

from components.hero_card import (
    render_hero_card
)


def render_ai_home():

    render_hero_card(
        title="FinBee AI",
        subtitle="Asisten Keuangan Pribadi Berbasis Artificial Intelligence",
        user_name="",
        emoji="🤖"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    provider = get(
        "ai_provider",
        "Gemini"
    )

    model = get(
        "ai_model",
        "-"
    )

    api_key = get(
        "api_key",
        ""
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Provider",
            provider
        )

    with col2:

        st.metric(
            "Model",
            model
        )

    with col3:

        st.metric(
            "API Key",
            "Configured"
            if api_key
            else "Not Set"
        )

    st.markdown("---")

    st.markdown(
        """
### 🚀 Fitur AI FinBee

✅ Chatbot AI

✅ Financial Recommendation

✅ Pengeluaran Analysis

✅ Saving Recommendation

✅ Financial Summary

✅ Multi AI Provider

- Gemini
- OpenRouter
- Groq
- Ollama Local

---

Gunakan menu di sidebar untuk mulai berinteraksi dengan AI.
"""
    )