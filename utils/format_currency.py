from config.settings import (
    CURRENCY_SYMBOL
)


def format_currency(amount):

    if amount is None:
        amount = 0

    try:
        amount = float(amount)
    except Exception:
        amount = 0

    return f"{CURRENCY_SYMBOL} {amount:,.0f}"


def format_currency_short(amount):

    if amount is None:
        amount = 0

    amount = float(amount)

    if amount >= 1_000_000_000:
        return f"{amount / 1_000_000_000:.1f}B"

    if amount >= 1_000_000:
        return f"{amount / 1_000_000:.1f}M"

    if amount >= 1_000:
        return f"{amount / 1_000:.1f}K"

    return f"{amount:.0f}"


def parse_currency(value):

    if value is None:
        return 0

    value = str(value)

    value = (
        value
        .replace("Rp", "")
        .replace(",", "")
        .replace(".", "")
        .strip()
    )

    try:
        return float(value)
    except Exception:
        return 0


def calculate_percentage(value, total):

    if total == 0:
        return 0

    return round(
        (value / total) * 100,
        2
    )


def calculate_balance(
    total_income,
    total_expense
):

    return total_income - total_expense


def determine_budget_status(
    total_expense,
    target_budget
):

    if target_budget <= 0:
        return "Tidak Ada Target"

    ratio = total_expense / target_budget

    if ratio <= 0.80:
        return "Aman"

    elif ratio <= 1.00:
        return "Waspada"

    elif ratio <= 1.10:
        return "Melebihi Sedikit"

    else:
        return "Melebihi Target"