import pandas as pd


def get_summary_metrics(transactions_df):
    if transactions_df.empty:
        return {
            "total_expense": 0,
            "total_income": 0,
            "balance": 0,
            "transaction_count": 0,
            "average_transaction": 0
        }

    expense_df = transactions_df[
        transactions_df["transaction_type"] == "expense"
    ]

    income_df = transactions_df[
        transactions_df["transaction_type"] == "income"
    ]

    total_expense = expense_df["amount"].sum()
    total_income = income_df["amount"].sum()
    balance = total_income - total_expense
    transaction_count = len(transactions_df)
    average_transaction = transactions_df["amount"].mean()

    return {
        "total_expense": total_expense,
        "total_income": total_income,
        "balance": balance,
        "transaction_count": transaction_count,
        "average_transaction": average_transaction
    }


def analyze_by_category(transactions_df):
    if transactions_df.empty:
        return pd.DataFrame()

    expense_df = transactions_df[
        transactions_df["transaction_type"] == "expense"
    ]

    if expense_df.empty:
        return pd.DataFrame()

    result = (
        expense_df
        .groupby("category_name")["amount"]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
    )

    return result


def analyze_by_payment_method(transactions_df):
    if transactions_df.empty:
        return pd.DataFrame()

    result = (
        transactions_df
        .groupby("payment_method")["amount"]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
    )

    return result


def get_monthly_trend(transactions_df):
    if transactions_df.empty:
        return pd.DataFrame()

    df = transactions_df.copy()
    df["tanggal_transaksi"] = pd.to_datetime(df["tanggal_transaksi"])

    monthly = (
        df
        .groupby([
            pd.Grouper(key="tanggal_transaksi", freq="ME"),
            "transaction_type"
        ])["amount"]
        .sum()
        .reset_index()
    )

    return monthly


def get_top_transactions(transactions_df, n=5):
    if transactions_df.empty:
        return pd.DataFrame()

    return (
        transactions_df
        .sort_values("amount", ascending=False)
        .head(n)
    )

