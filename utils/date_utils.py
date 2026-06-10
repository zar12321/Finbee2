from datetime import datetime
from datetime import date

import pandas as pd

from config.settings import (
    DATE_FORMAT,
    DATETIME_FORMAT,
    MONTH_FORMAT
)


def to_datetime(value):

    if value is None:
        return None

    try:
        return pd.to_datetime(value)
    except Exception:
        return None


def to_date(value):

    dt = to_datetime(value)

    if dt is None:
        return None

    return dt.date()


def format_date(value):

    dt = to_datetime(value)

    if dt is None:
        return "-"

    return dt.strftime(DATE_FORMAT)


def format_datetime(value):

    dt = to_datetime(value)

    if dt is None:
        return "-"

    return dt.strftime(DATETIME_FORMAT)


def format_month(value):

    dt = to_datetime(value)

    if dt is None:
        return "-"

    return dt.strftime(MONTH_FORMAT)


def get_current_date():

    return date.today()


def get_current_datetime():

    return datetime.now()


def get_current_month():

    return datetime.now().month


def get_current_year():

    return datetime.now().year


def get_month_name(month_number):

    months = {
        1: "Januari",
        2: "Februari",
        3: "Maret",
        4: "April",
        5: "Mei",
        6: "Juni",
        7: "Juli",
        8: "Agustus",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "Desember"
    }

    return months.get(month_number, "-")


def get_month_year_label(month, year):

    return f"{get_month_name(month)} {year}"


def get_month_start(month=None, year=None):

    if month is None:
        month = get_current_month()

    if year is None:
        year = get_current_year()

    return pd.Timestamp(year=year, month=month, day=1)


def get_month_end(month=None, year=None):

    start = get_month_start(month, year)

    return start + pd.offsets.MonthEnd(1)


def extract_month(value):

    dt = to_datetime(value)

    if dt is None:
        return None

    return dt.month


def extract_year(value):

    dt = to_datetime(value)

    if dt is None:
        return None

    return dt.year


def create_month_filter_options(transactions_df):

    if transactions_df.empty:
        return []

    df = transactions_df.copy()

    df["tanggal_transaksi"] = pd.to_datetime(
        df["tanggal_transaksi"]
    )

    options = (
        df["tanggal_transaksi"]
        .dt.to_period("M")
        .astype(str)
        .unique()
        .tolist()
    )

    options.sort(reverse=True)

    return options


def filter_by_month_year(
    transactions_df,
    month,
    year
):

    if transactions_df.empty:
        return transactions_df

    df = transactions_df.copy()

    df["tanggal_transaksi"] = pd.to_datetime(
        df["tanggal_transaksi"]
    )

    return df[
        (df["tanggal_transaksi"].dt.month == month)
        &
        (df["tanggal_transaksi"].dt.year == year)
    ]