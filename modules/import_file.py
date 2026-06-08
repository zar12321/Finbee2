import pandas as pd
import re


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

    try:
        amount = float(text)
    except ValueError:
        return None

    if is_negative:
        amount = abs(amount)

    return amount


def parse_flexible_date(value):
    if pd.isna(value):
        return pd.NaT

    date_value = pd.to_datetime(value, errors="coerce")

    if pd.isna(date_value):
        date_value = pd.to_datetime(value, errors="coerce", dayfirst=True)

    return date_value


def normalize_transaction_type(value):
    if pd.isna(value):
        return "expense"

    text = str(value).strip().lower()

    type_mapping = {
        "expense": "expense",
        "pengeluaran": "expense",
        "keluar": "expense",
        "debit": "expense",
        "debet": "expense",
        "out": "expense",
        "outcome": "expense",

        "income": "income",
        "pemasukan": "income",
        "masuk": "income",
        "credit": "income",
        "kredit": "income",
        "in": "income",
        "revenue": "income"
    }

    return type_mapping.get(text, "expense")


def standardize_category(raw_category, description="", transaction_type="expense"):
    raw_category = "" if pd.isna(raw_category) else str(raw_category)
    description = "" if pd.isna(description) else str(description)

    text = f"{raw_category} {description}".lower()

    if transaction_type == "income":
        if any(word in text for word in [
            "gaji", "salary", "income", "pemasukan", "upah", "freelance",
            "honor", "bonus", "komisi", "transfer gaji"
        ]):
            return "Salary"

        if any(word in text for word in [
            "allowance", "uang saku", "kiriman", "transfer orang tua",
            "uang bulanan"
        ]):
            return "Allowance"

        return "Salary"

    if any(word in text for word in [
        "food", "makan", "makanan", "minum", "minuman", "jajan",
        "groceries", "grocery", "belanja dapur", "sayur", "buah",
        "nasi", "ayam", "kopi", "cafe", "restoran", "restaurant",
        "warung", "kantin", "bakso", "mie", "gofood", "grabfood"
    ]):
        return "Food"

    if any(word in text for word in [
        "transport", "transportasi", "ojek", "grab", "gojek", "bus",
        "kereta", "bensin", "parkir", "tol", "angkot", "taxi",
        "taksi", "mrt", "lrt"
    ]):
        return "Transport"

    if any(word in text for word in [
        "bill", "bills", "tagihan", "listrik", "air", "internet",
        "wifi", "pulsa", "sewa", "kos", "kontrakan", "pln", "pdam"
    ]):
        return "Bills"

    if any(word in text for word in [
        "shopping", "belanja", "baju", "sepatu", "tas", "aksesoris",
        "skincare", "barang", "marketplace", "tokopedia", "shopee",
        "lazada", "mall"
    ]):
        return "Shopping"

    if any(word in text for word in [
        "education", "pendidikan", "kuliah", "buku", "kursus",
        "kelas", "seminar", "pelatihan", "modul", "kampus",
        "sertifikat"
    ]):
        return "Education"

    if any(word in text for word in [
        "health", "kesehatan", "obat", "vitamin", "dokter",
        "rumah sakit", "klinik", "apotek", "masker", "suplemen"
    ]):
        return "Health"

    if any(word in text for word in [
        "entertainment", "hiburan", "nonton", "bioskop", "game",
        "spotify", "netflix", "konser", "film", "popcorn"
    ]):
        return "Entertainment"

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
        cleaned_df["keterangan"] = (
            df[desc_col]
            .fillna("Transaksi tanpa keterangan")
            .astype(str)
            .str.strip()
        )
    else:
        cleaned_df["keterangan"] = "Transaksi tanpa keterangan"

    cleaned_df["tujuan_transaksi"] = cleaned_df["keterangan"]

    if payment_col is not None:
        cleaned_df["payment_method"] = (
            df[payment_col]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )
    else:
        cleaned_df["payment_method"] = "Unknown"

    cleaned_df.loc[
        cleaned_df["payment_method"].str.strip() == "",
        "payment_method"
    ] = "Unknown"

    cleaned_df["amount"] = df[amount_col].apply(clean_amount)

    if type_col is not None:
        cleaned_df["transaction_type"] = df[type_col].apply(normalize_transaction_type)
    else:
        cleaned_df["transaction_type"] = "expense"

    if category_col is not None:
        cleaned_df["raw_category"] = (
            df[category_col]
            .fillna("")
            .astype(str)
            .str.strip()
        )
    else:
        cleaned_df["raw_category"] = ""

    cleaned_df["category_name"] = cleaned_df.apply(
        lambda row: standardize_category(
            raw_category=row["raw_category"],
            description=row["keterangan"],
            transaction_type=row["transaction_type"]
        ),
        axis=1
    )

    cleaned_df = cleaned_df[
        [
            "tanggal_transaksi",
            "raw_category",
            "category_name",
            "transaction_type",
            "tujuan_transaksi",
            "keterangan",
            "payment_method",
            "amount"
        ]
    ]

    return cleaned_df