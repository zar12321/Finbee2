import streamlit as st

from state.session import (
    get,
    set
)


PROVIDER_MODELS = {
    "Gemini": [
        "gemini-2.5-flash",
        "gemini-2.5-pro"
    ],

    "OpenRouter": [
        "openai/gpt-4o-mini",
        "google/gemini-2.5-flash",
        "anthropic/claude-sonnet-4"
    ],

    "Groq": [
        "llama-3.3-70b-versatile",
        "llama3-8b-8192",
        "mixtral-8x7b-32768"
    ],

    "Ollama Local": [
        "llama3",
        "mistral",
        "deepseek-r1"
    ]
}


def render_ai_settings():

    st.title("⚙️ AI Settings")

    current_provider = get(
        "ai_provider",
        "Gemini"
    )

    provider = st.selectbox(
        "AI Provider",
        list(PROVIDER_MODELS.keys()),
        index=list(PROVIDER_MODELS.keys()).index(
            current_provider
        )
    )

    model = st.selectbox(
        "Model",
        PROVIDER_MODELS[provider]
    )

    api_key = st.text_input(
        "API Key",
        value=get("api_key", ""),
        type="password"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💾 Simpan",
            use_container_width=True
        ):

            set(
                "ai_provider",
                provider
            )

            set(
                "ai_model",
                model
            )

            set(
                "api_key",
                api_key
            )

            st.success(
                "AI Setting berhasil disimpan."
            )

    with col2:

        if st.button(
            "🗑️ Reset",
            use_container_width=True
        ):

            set(
                "api_key",
                ""
            )

            st.success(
                "API Key berhasil dihapus."
            )

    st.markdown("---")

    st.info(
        """
        API Key hanya disimpan di session aplikasi.
        Tidak disimpan ke database.
        """
    )