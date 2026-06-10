import streamlit as st

from utils.format_currency import format_currency


import streamlit as st


def render_metric_card(
    title,
    value,
    icon,
    color_class="green"
):

    with st.container(border=True):
        st.metric(
            label=f"{icon} {title}",
            value=value
        )


def render_financial_metrics(
    total_income,
    total_expense,
    balance,
    transaction_count
):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_metric_card(
            "Total Income",
            format_currency(total_income),
            "💰",
            "green"
        )

    with col2:
        render_metric_card(
            "Total Expense",
            format_currency(total_expense),
            "📉",
            "red"
        )

    with col3:
        render_metric_card(
            "Balance",
            format_currency(balance),
            "🏦",
            "blue"
        )

    with col4:
        render_metric_card(
            "Transactions",
            transaction_count,
            "📋",
            "orange"
        )