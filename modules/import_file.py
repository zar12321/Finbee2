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

    formats = [

        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y %H:%M:%S"

    ]

    for fmt in formats:

        try:
            return pd.to_datetime(
                value,
                format=fmt
            )
        except:
            pass

    return pd.to_datetime(
        value,
        errors="coerce"
    )

def normalize_transaction_type(value):

    print("RAW =", repr(value))

    if pd.isna(value):
        return "expense"

    text = str(value).strip().lower()

    print("NORMALIZED =", repr(text))

    type_mapping = {
        ...
    }

    result = type_mapping.get(text, "expense")

    print("RESULT =", result)

    return result


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

    # =====================================================
    # NORMALISASI NAMA KOLOM
    # =====================================================

    normalized_columns = {
        col: str(col).lower().strip()
        for col in df.columns
    }

    date_col = None

    priority_date_columns = [
        "tanggal transaksi",
        "transaction date",
        "date transaksi"
    ]

    for col in df.columns:

        col_lower = str(col).lower().strip()

        if col_lower in priority_date_columns:

            date_col = col
            break

    if date_col is None:

        date_col = find_column_by_keywords(
            df.columns,
            [
                "date",
                "tgl",
                "tanggal"
            ]
        )

    amount_col = find_column_by_keywords(
        df.columns,
        [
            "nominal",
            "amount",
            "jumlah",
            "total",
            "harga",
            "value",
            "nilai",
            "pengeluaran",
            "pemasukan"
        ]
    )

    tujuan_col = find_column_by_keywords(
        df.columns,
        [
            "tujuan transaksi",
            "tujuan"
        ]
    )

    desc_col = find_column_by_keywords(
        df.columns,
        [
            "keterangan",
            "deskripsi",
            "description",
            "catatan",
            "remark",
            "details"
        ]
    )

    payment_col = find_column_by_keywords(
        df.columns,
        [
            "bayar lewat",
            "metode pembayaran",
            "payment method",
            "payment",
            "metode",
            "wallet",
            "bank"
        ]
    )

    type_col = find_column_by_keywords(
        df.columns,
        [
            "transaction type",
            "jenis transaksi",
            "transaksi",
            "arus kas",
            "cashflow",
            "cash flow",
            "debit kredit",
            "debit/kredit",
            "type",
            "tipe",
            "jenis"
        ]
    )

    category_col = find_column_by_keywords(
        df.columns,
        [
            "kategori",
            "category"
        ]
    )

    if amount_col is None:
        raise ValueError(
            "Kolom nominal tidak ditemukan."
        )

    # =====================================================
    # TANGGAL
    # =====================================================

    if date_col:

        cleaned_df["tanggal_transaksi"] = (
            df[date_col]
            .apply(parse_flexible_date)
        )

    else:

        cleaned_df["tanggal_transaksi"] = (
            pd.Timestamp.today().normalize()
        )

    # =====================================================
    # KETERANGAN
    # =====================================================

    if desc_col:

        cleaned_df["keterangan"] = (
            df[desc_col]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    else:

        cleaned_df["keterangan"] = ""

    # =====================================================
    # TUJUAN TRANSAKSI
    # =====================================================

    if tujuan_col:

        cleaned_df["tujuan_transaksi"] = (
            df[tujuan_col]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    else:

        cleaned_df["tujuan_transaksi"] = (
            cleaned_df["keterangan"]
        )

    cleaned_df.loc[
        cleaned_df["tujuan_transaksi"] == "",
        "tujuan_transaksi"
    ] = cleaned_df["keterangan"]

    # =====================================================
    # PAYMENT METHOD
    # =====================================================

    if payment_col:

        cleaned_df["payment_method"] = (
            df[payment_col]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

    else:

        cleaned_df["payment_method"] = (
            "Unknown"
        )

    # =====================================================
    # AMOUNT
    # =====================================================

    cleaned_df["amount"] = (
        df[amount_col]
        .apply(clean_amount)
    )

    # =====================================================
    # TRANSACTION TYPE
    # =====================================================

    if type_col:

        cleaned_df["transaction_type"] = (
            df[type_col]
            .apply(normalize_transaction_type)
        )

    else:

        cleaned_df["transaction_type"] = (
            "expense"
        )

    # =====================================================
    # RAW CATEGORY
    # =====================================================

    if category_col:

        cleaned_df["raw_category"] = (
            df[category_col]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    else:

        cleaned_df["raw_category"] = ""

    # =====================================================
    # AUTO CATEGORY MAPPING
    # =====================================================

    cleaned_df["category_name"] = (
        cleaned_df.apply(
            lambda row: standardize_category(
                raw_category=row["raw_category"],
                description=(
                    str(row["tujuan_transaksi"])
                    + " "
                    + str(row["keterangan"])
                ),
                transaction_type=row["transaction_type"]
            ),
            axis=1
        )
    )

    # =====================================================
    # CLEAN DATA
    # =====================================================

    cleaned_df = cleaned_df.dropna(
        subset=["amount"]
    )

    cleaned_df = cleaned_df[
        cleaned_df["amount"] > 0
    ]

    # =====================================================
    # FINAL SCHEMA DATABASE
    # =====================================================

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