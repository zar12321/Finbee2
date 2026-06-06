import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def prepare_monthly_expense(transactions_df):
    if transactions_df.empty:
        return pd.DataFrame()

    df = transactions_df.copy()

    df["tanggal_transaksi"] = pd.to_datetime(df["tanggal_transaksi"])

    expense_df = df[df["transaction_type"] == "expense"]

    if expense_df.empty:
        return pd.DataFrame()

    monthly_expense = (
        expense_df
        .set_index("tanggal_transaksi")
        .resample("M")["amount"]
        .sum()
        .reset_index()
    )

    monthly_expense = monthly_expense.rename(
        columns={
            "tanggal_transaksi": "bulan",
            "amount": "total_pengeluaran"
        }
    )

    monthly_expense["month_index"] = np.arange(len(monthly_expense))

    return monthly_expense


def predict_next_month_expense(transactions_df):
    monthly_expense = prepare_monthly_expense(transactions_df)

    if monthly_expense.empty:
        return {
            "prediction": 0,
            "method": "Tidak ada data",
            "monthly_data": monthly_expense,
            "message": "Belum ada data pengeluaran untuk diprediksi."
        }

    if len(monthly_expense) < 3:
        prediction = monthly_expense["total_pengeluaran"].mean()

        return {
            "prediction": round(float(prediction), 2),
            "method": "Rata-rata pengeluaran bulanan",
            "monthly_data": monthly_expense,
            "message": "Data kurang dari 3 bulan, sehingga prediksi menggunakan rata-rata pengeluaran bulanan."
        }

    X = monthly_expense[["month_index"]]
    y = monthly_expense["total_pengeluaran"]

    model = LinearRegression()
    model.fit(X, y)

    next_month_index = pd.DataFrame(
        {"month_index": [len(monthly_expense)]}
    )

    prediction = model.predict(next_month_index)[0]
    prediction = max(prediction, 0)

    return {
        "prediction": round(float(prediction), 2),
        "method": "Linear Regression sederhana",
        "monthly_data": monthly_expense,
        "message": "Data minimal 3 bulan, sehingga prediksi menggunakan Linear Regression sederhana."
    }