import streamlit as st

from modules.db import (
    load_transactions
)

from modules.prediction import (
    predict_next_month_expense
)

from modules.ai_provider import (
    build_financial_summary,
    generate_ai_response
)

from state.session import (
    get,
    get_current_user
)


def render_recommendation():

    st.title(
        "💡 AI Recommendation"
    )

    user = get_current_user()

    if not user:
        return

    provider = get("ai_provider")
    model = get("ai_model")
    api_key = get("api_key")

    if provider != "Ollama Local":

        if not api_key:

            st.warning(
                "Isi API Key terlebih dahulu."
            )

            return

    user_id = user["user_id"]

    transactions_df = (
        load_transactions()
    )

    transactions_df = (
        transactions_df[
            transactions_df["user_id"]
            == user_id
        ]
    )

    if transactions_df.empty:

        st.info(
            "Belum ada transaksi."
        )

        return

    prediction = (
        predict_next_month_expense(
            transactions_df
        )
    )

    financial_summary = (
        build_financial_summary(
            transactions_df,
            prediction
        )
    )

    st.subheader(
        "Ringkasan Data"
    )

    st.text_area(
        "",
        financial_summary,
        height=250
    )

    if st.button(
        "🚀 Generate Recommendation",
        use_container_width=True
    ):

        with st.spinner(
            "Menganalisis data..."
        ):

            prompt = f"""
Analisis data keuangan berikut.

Berikan:

1. Kondisi keuangan user
2. Kategori boros
3. Rekomendasi penghematan
4. Strategi meningkatkan tabungan
5. Kesimpulan

Data:

{financial_summary}
"""

            try:

                result = (
                    generate_ai_response(
                        provider,
                        api_key,
                        model,
                        prompt
                    )
                )

                st.markdown(
                    result
                )

            except Exception as e:

                st.error(
                    str(e)
                )