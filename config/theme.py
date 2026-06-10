from pathlib import Path

import streamlit as st

from config.settings import (
    APP_NAME,
    APP_ICON,
    APP_LAYOUT,
    APP_SIDEBAR_STATE,
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    SUCCESS_COLOR,
    WARNING_COLOR,
    DANGER_COLOR,
    INFO_COLOR,
    BACKGROUND_COLOR,
    CARD_BACKGROUND_COLOR,
    TEXT_COLOR,
    TEXT_MUTED_COLOR,
    BORDER_COLOR
)


def configure_page():

    st.set_page_config(
        page_title=APP_NAME,
        page_icon=APP_ICON,
        layout=APP_LAYOUT,
        initial_sidebar_state=APP_SIDEBAR_STATE
    )


def load_css(css_path):

    css_file = Path(css_path)

    if not css_file.exists():
        return

    with open(css_file, "r", encoding="utf-8") as file:

        st.markdown(
            f"<style>{file.read()}</style>",
            unsafe_allow_html=True
        )


def load_all_styles():

    style_files = [
        "styles/main.css",
        "styles/dashboard.css",
        "styles/auth.css",
        "styles/ai.css"
    ]

    for style_file in style_files:
        load_css(style_file)


def inject_theme_variables():

    st.markdown(
        f"""
        <style>

        :root {{

            --primary-color: {PRIMARY_COLOR};

            --secondary-color: {SECONDARY_COLOR};

            --success-color: {SUCCESS_COLOR};

            --warning-color: {WARNING_COLOR};

            --danger-color: {DANGER_COLOR};

            --info-color: {INFO_COLOR};

            --background-color: {BACKGROUND_COLOR};

            --card-background-color: {CARD_BACKGROUND_COLOR};

            --text-color: {TEXT_COLOR};

            --text-muted-color: {TEXT_MUTED_COLOR};

            --border-color: {BORDER_COLOR};

        }}

        </style>
        """,
        unsafe_allow_html=True
    )


def inject_base_theme():

    st.markdown(
        f"""
        <style>

        .stApp {{
            background: linear-gradient(
                135deg,
                #08130D,
                #0C1C12
            );
            color: {TEXT_COLOR};
        }}

        header {{
            visibility: hidden;
        }}

        footer {{
            visibility: hidden;
        }}

        #MainMenu {{
            visibility: hidden;
        }}

        .block-container {{
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 1600px;
        }}

        div[data-testid="stMetric"] {{
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 20px;
        }}

        div[data-testid="stMetric"]:hover {{
            border-color: {PRIMARY_COLOR};
            transition: 0.3s ease;
        }}

        div[data-baseweb="select"] > div {{
            background-color: rgba(255,255,255,0.03);
        }}

        div[data-baseweb="input"] > div {{
            background-color: rgba(255,255,255,0.03);
        }}

        .stButton > button {{

            width: 100%;

            border-radius: 12px;

            border: none;

            background-color: {PRIMARY_COLOR};

            color: black;

            font-weight: 600;

            transition: 0.3s ease;

        }}

        .stButton > button:hover {{

            transform: translateY(-2px);

            box-shadow: 0 8px 20px rgba(124,255,91,0.3);

        }}

        .stDataFrame {{
            border-radius: 15px;
            overflow: hidden;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


def apply_theme():

    inject_theme_variables()

    inject_base_theme()

    load_all_styles()