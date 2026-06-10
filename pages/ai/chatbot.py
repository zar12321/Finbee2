import streamlit as st

from state.session import (
    get,
    append_chat,
    clear_chat_history
)

from modules.ai_provider import (
    generate_ai_response
)


def render_chatbot():

    st.title("🤖 FinBee AI Chatbot")

    provider = get("ai_provider")
    model = get("ai_model")
    api_key = get("api_key")

    if provider != "Ollama Local":

        if not api_key:

            st.warning(
                "Silakan isi API Key terlebih dahulu."
            )

            return

    st.caption(
        f"Provider : {provider} | Model : {model}"
    )

    st.markdown("---")

    history = get(
        "chat_history",
        []
    )

    for chat in history:

        with st.chat_message(
            chat["role"]
        ):

            st.markdown(
                chat["content"]
            )

    prompt = st.chat_input(
        "Tanyakan sesuatu tentang keuangan..."
    )

    if prompt:

        append_chat(
            "user",
            prompt
        )

        with st.chat_message(
            "user"
        ):
            st.markdown(prompt)

        try:

            response = generate_ai_response(
                provider=provider,
                api_key=api_key,
                model_name=model,
                prompt=prompt
            )

        except Exception as e:

            response = (
                f"Error: {str(e)}"
            )

        append_chat(
            "assistant",
            response
        )

        with st.chat_message(
            "assistant"
        ):
            st.markdown(response)

    st.markdown("---")

    if st.button(
        "🗑️ Bersihkan Chat"
    ):

        clear_chat_history()

        st.rerun()