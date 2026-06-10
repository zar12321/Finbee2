import streamlit as st


def render_ai_card(
    title,
    description,
    icon="🤖"
):

    st.markdown(
        f"""
        <div class="ai-card">

            <div class="ai-icon">
                {icon}
            </div>

            <div class="ai-content">

                <div class="ai-title">
                    {title}
                </div>

                <div class="ai-description">
                    {description}
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )