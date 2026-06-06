import pandas as pd
import re


CATEGORY_KEYWORDS = {
    "Food": [
        "makan", "nasi", "ayam", "kopi", "roti", "bakso", "mie",
        "warung", "kantin", "resto", "restaurant", "gofood", "grabfood"
    ],
    "Transport": [
        "grab", "gojek", "ojek", "bensin", "parkir", "tol",
        "bus", "kereta", "transport", "angkot"
    ],
    "Bills": [
        "listrik", "air", "wifi", "pulsa", "internet", "tagihan",
        "pln", "pdam"
    ],
    "Shopping": [
        "baju", "sepatu", "barang", "belanja", "tokopedia",
        "shopee", "lazada", "mall"
    ],
    "Education": [
        "buku", "kuliah", "kursus", "kelas", "sertifikat",
        "kampus", "pendidikan"
    ],
    "Health": [
        "obat", "dokter", "klinik", "rumah sakit", "vitamin",
        "apotek"
    ],
    "Entertainment": [
        "bioskop", "game", "netflix", "spotify", "konser",
        "hiburan"
    ]
}


def find_column_by_keywords(columns, keywords):
    normalized_columns = {
        col: str(col).lower().strip()
        for col in columns
    }

    for original_col, normalized_col in normalized_columns.items():
        for keyword in keywords:
            if keyword in normalized_col:
                return original_col

    return None


def clean_amount(value):
    if pd.isna(value):
        return None

    text = str(value).strip()

    text = text.replace("Rp", "")
    text = text.replace("rp", "")
    text = text.replace("IDR", "")
    text = text.replace("idr", "")
    text = text.replace(" ", "")

    is_negative = "-" in text

    text = re.sub(r"[^0-9,\.]", "", text)

    if "," in text and "." in text:
        text = text.replace(".", "")
        text = text.replace(",", ".")
    elif "," in text:
        text = text.replace(",", "")
    elif "." in text:
        parts = text.split(".")
        if len(parts[-1]) == 3:
            text = text.replace(".", "")

    if text == "":
        return None

    amount = float(text)

    if is_negative:
        amount = abs(amount)

    return amount


def predict_category(text):
    if pd.isna(text):
        return "Other"

    text = str(text).lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return category

    return "Other"


def auto_clean_financial_file(df):
    cleaned_df = pd.DataFrame()

    columns = df.columns

    date_col = find_column_by_keywords(
        columns,
        ["tanggal", "date", "tgl", "waktu"]
    )

    amount_col = find_column_by_keywords(
        columns,
        ["amount", "nominal", "jumlah", "total", "harga", "pengeluaran", "pemasukan"]
    )

    desc_col = find_column_by_keywords(
        columns,
        ["deskripsi", "description", "keterangan", "tujuan", "catatan", "remark", "details"]
    )

    payment_col = find_column_by_keywords(
        columns,
        ["payment", "metode", "method", "pembayaran", "wallet", "bank"]
    )

    type_col = find_column_by_keywords(
        columns,
        ["type", "tipe", "jenis"]
    )

    category_col = find_column_by_keywords(
        columns,
        ["category", "kategori"]
    )

    if amount_col is None:
        raise ValueError("Kolom nominal tidak ditemukan. File harus memiliki kolom nominal/jumlah/amount.")

    if date_col is not None:
        cleaned_df["tanggal_transaksi"] = df[date_col].apply(parse_flexible_date)
    else:
        cleaned_df["tanggal_transaksi"] = pd.Timestamp.today().normalize()
        
    if desc_col is not None:
        cleaned_df["keterangan"] = df[desc_col].fillna("Transaksi tanpa keterangan").astype(str)
    else:
        cleaned_df["keterangan"] = "Transaksi tanpa keterangan"

    cleaned_df["tujuan_transaksi"] = cleaned_df["keterangan"]

    if payment_col is not None:
        cleaned_df["payment_method"] = df[payment_col].fillna("Unknown").astype(str)
    else:
        cleaned_df["payment_method"] = "Unknown"

    cleaned_df["amount"] = df[amount_col].apply(clean_amount)

    if type_col is not None:
        cleaned_df["transaction_type"] = (
            df[type_col]
            .fillna("expense")
            .astype(str)
            .str.lower()
        )
    else:
        cleaned_df["transaction_type"] = "expense"

    cleaned_df["transaction_type"] = cleaned_df["transaction_type"].replace({
        "pengeluaran": "expense",
        "keluar": "expense",
        "debit": "expense",
        "pemasukan": "income",
        "masuk": "income",
        "credit": "income",
        "kredit": "income"
    })

    if category_col is not None:
        cleaned_df["category_name"] = df[category_col].fillna("").astype(str)
        cleaned_df.loc[
            cleaned_df["category_name"].str.strip() == "",
            "category_name"
        ] = cleaned_df["keterangan"].apply(predict_category)
    else:
        cleaned_df["category_name"] = cleaned_df["keterangan"].apply(predict_category)

    cleaned_df = cleaned_df[
        [
            "tanggal_transaksi",
            "category_name",
            "transaction_type",
            "tujuan_transaksi",
            "keterangan",
            "payment_method",
            "amount"
        ]
    ]

    return cleaned_df

def parse_flexible_date(value):
    if pd.isna(value):
        return pd.NaT

    date_value = pd.to_datetime(value, errors="coerce")

    if pd.isna(date_value):
        date_value = pd.to_datetime(value, errors="coerce", dayfirst=True)

    return date_value