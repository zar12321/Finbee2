import streamlit as st


def primary_button(
    label,
    key=None,
    use_container_width=True
):

    return st.button(
        label,
        key=key,
        use_container_width=use_container_width
    )


def secondary_button(
    label,
    key=None,
    use_container_width=True
):

    return st.button(
        label,
        key=key,
        use_container_width=use_container_width
    )


def danger_button(
    label,
    key=None,
    use_container_width=True
):

    return st.button(
        label,
        key=key,
        use_container_width=use_container_width
    )


def success_button(
    label,
    key=None,
    use_container_width=True
):

    return st.button(
        label,
        key=key,
        use_container_width=use_container_width
    )