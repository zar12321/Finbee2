import streamlit as st


def render_hero_card(
    title,
    subtitle,
    user_name,
    emoji="🐝"
):

    avatar = (
        user_name[0].upper()
        if user_name
        else "G"
    )

    html = f"""
<div class="hero-card">

    <div class="hero-left">

        <div class="hero-badge">
            {emoji} FINBEE
        </div>

        <h1 class="hero-title">
            {title}
        </h1>

        <p class="hero-subtitle">
            {subtitle}
        </p>

    </div>

    <div class="hero-right">

        <div class="hero-avatar">
            {avatar}
        </div>

        <div class="hero-user-info">

            <span class="hero-label">
                Welcome Back
            </span>

            <span class="hero-name">
                {user_name}
            </span>

        </div>

    </div>

</div>
"""

    st.markdown(
        html,
        unsafe_allow_html=True
    )