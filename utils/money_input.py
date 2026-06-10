import re


def clean_money_input(value):

    if value is None:
        return 0

    value = str(value)

    value = re.sub(
        r"[^0-9]",
        "",
        value
    )

    if value == "":
        return 0

    return int(value)


def format_money_input(value):

    value = clean_money_input(value)

    return f"{value:,}"


def money_to_float(value):

    value = clean_money_input(value)

    return float(value)


def money_to_int(value):

    value = clean_money_input(value)

    return int(value)


def is_valid_amount(value):

    try:
        value = float(value)
        return value > 0
    except Exception:
        return False


def sanitize_amount(value):

    if value is None:
        return 0

    try:
        value = float(value)
    except Exception:
        return 0

    if value < 0:
        value = abs(value)

    return value