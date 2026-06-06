import requests
from google import genai


def call_gemini(api_key, model_name, prompt):
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    return response.text


def call_openrouter(api_key, model_name, prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": "Kamu adalah asisten finansial pribadi berbasis data. Jawab berdasarkan data yang diberikan."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    result = response.json()
    return result["choices"][0]["message"]["content"]


def call_groq(api_key, model_name, prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": "Kamu adalah asisten finansial pribadi berbasis data. Jawab berdasarkan data yang diberikan."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    result = response.json()
    return result["choices"][0]["message"]["content"]


def call_ollama(model_name, prompt):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()

    result = response.json()
    return result["response"]


def generate_ai_response(provider, api_key, model_name, prompt):
    if provider == "Gemini":
        return call_gemini(api_key, model_name, prompt)

    elif provider == "OpenRouter":
        return call_openrouter(api_key, model_name, prompt)

    elif provider == "Groq":
        return call_groq(api_key, model_name, prompt)

    elif provider == "Ollama Local":
        return call_ollama(model_name, prompt)

    else:
        raise ValueError("Provider AI belum didukung.")


def build_financial_summary(transactions_df, prediction_result=None):
    if transactions_df.empty:
        return "Belum ada data transaksi."

    total_expense = transactions_df[
        transactions_df["transaction_type"] == "expense"
    ]["amount"].sum()

    total_income = transactions_df[
        transactions_df["transaction_type"] == "income"
    ]["amount"].sum()

    balance = total_income - total_expense

    category_summary = (
        transactions_df[transactions_df["transaction_type"] == "expense"]
        .groupby("category_name")["amount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    payment_summary = (
        transactions_df
        .groupby("payment_method")["amount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    top_transactions = (
        transactions_df
        .sort_values("amount", ascending=False)
        .head(5)
    )

    category_text = "\n".join(
        [
            f"- {row['category_name']}: Rp {row['amount']:,.0f}"
            for _, row in category_summary.iterrows()
        ]
    )

    payment_text = "\n".join(
        [
            f"- {row['payment_method']}: Rp {row['amount']:,.0f}"
            for _, row in payment_summary.iterrows()
        ]
    )

    top_transaction_text = "\n".join(
        [
            f"- {row['tanggal_transaksi']} | {row['category_name']} | {row['tujuan_transaksi']} | Rp {row['amount']:,.0f}"
            for _, row in top_transactions.iterrows()
        ]
    )

    prediction_text = ""

    if prediction_result is not None:
        prediction_text = f"""
Prediksi pengeluaran bulan depan:
Rp {prediction_result['prediction']:,.0f}
"""

    summary = f"""
Ringkasan Keuangan User

Total pemasukan:
Rp {total_income:,.0f}

Total pengeluaran:
Rp {total_expense:,.0f}

Saldo bersih:
Rp {balance:,.0f}

Pengeluaran berdasarkan kategori:
{category_text}

Nominal berdasarkan metode pembayaran:
{payment_text}

Top 5 transaksi terbesar:
{top_transaction_text}

{prediction_text}
"""

    return summary