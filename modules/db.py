import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text



def get_engine():
    db_url = st.secrets["database"]["url"]
    return create_engine(db_url)


def test_connection():
    engine = get_engine()

    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1 AS status"))
        return result.fetchone()


def load_users():
    engine = get_engine()

    query = """
        SELECT
            user_id,
            nama,
            umur,
            pekerjaan,
            pemasukan_bulanan,
            target_tabungan,
            created_at
        FROM users
        ORDER BY user_id;
    """

    return pd.read_sql(query, engine)


def load_categories():
    engine = get_engine()

    query = """
        SELECT
            category_id,
            category_name,
            category_type
        FROM categories
        ORDER BY category_id;
    """

    return pd.read_sql(query, engine)


def load_transactions():
    engine = get_engine()

    query = """
        SELECT
            t.transaction_id,
            t.user_id,
            u.nama AS user_name,
            t.category_id,
            c.category_name,
            t.import_id,
            t.tanggal_input,
            t.tanggal_transaksi,
            t.transaction_type,
            t.tujuan_transaksi,
            t.keterangan,
            t.payment_method,
            t.amount,
            t.source,
            t.created_at
        FROM transactions t
        JOIN users u
            ON t.user_id = u.user_id
        LEFT JOIN categories c
            ON t.category_id = c.category_id
        ORDER BY t.tanggal_transaksi DESC;
    """

    df = pd.read_sql(query, engine)

    if not df.empty:
        df["tanggal_input"] = pd.to_datetime(df["tanggal_input"])
        df["tanggal_transaksi"] = pd.to_datetime(df["tanggal_transaksi"])
        df["created_at"] = pd.to_datetime(df["created_at"])
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    return df

def insert_user(nama, umur, pekerjaan, pemasukan_bulanan, target_tabungan):
    engine = get_engine()

    query = text("""
        INSERT INTO users
            (nama, umur, pekerjaan, pemasukan_bulanan, target_tabungan)
        VALUES
            (:nama, :umur, :pekerjaan, :pemasukan_bulanan, :target_tabungan)
    """)

    with engine.begin() as conn:
        conn.execute(query, {
            "nama": nama,
            "umur": umur,
            "pekerjaan": pekerjaan,
            "pemasukan_bulanan": pemasukan_bulanan,
            "target_tabungan": target_tabungan
        })

def insert_transaction(
    user_id,
    category_id,
    tanggal_transaksi,
    transaction_type,
    tujuan_transaksi,
    keterangan,
    payment_method,
    amount,
    source="manual"
):
    engine = get_engine()

    query = text("""
        INSERT INTO transactions
            (
                user_id,
                category_id,
                tanggal_transaksi,
                transaction_type,
                tujuan_transaksi,
                keterangan,
                payment_method,
                amount,
                source
            )
        VALUES
            (
                :user_id,
                :category_id,
                :tanggal_transaksi,
                :transaction_type,
                :tujuan_transaksi,
                :keterangan,
                :payment_method,
                :amount,
                :source
            )
    """)

    with engine.begin() as conn:
        conn.execute(query, {
            "user_id": user_id,
            "category_id": category_id,
            "tanggal_transaksi": tanggal_transaksi,
            "transaction_type": transaction_type,
            "tujuan_transaksi": tujuan_transaksi,
            "keterangan": keterangan,
            "payment_method": payment_method,
            "amount": amount,
            "source": source
        })

def insert_imported_transactions(user_id, imported_df):
    engine = get_engine()

    categories_df = load_categories()

    category_map = dict(
        zip(categories_df["category_name"], categories_df["category_id"])
    )

    query = text("""
        INSERT INTO transactions
            (
                user_id,
                category_id,
                tanggal_transaksi,
                transaction_type,
                tujuan_transaksi,
                keterangan,
                payment_method,
                amount,
                source
            )
        VALUES
            (
                :user_id,
                :category_id,
                :tanggal_transaksi,
                :transaction_type,
                :tujuan_transaksi,
                :keterangan,
                :payment_method,
                :amount,
                :source
            )
    """)

    with engine.begin() as conn:
        for _, row in imported_df.iterrows():
            category_name = row["category_name"]
            category_id = category_map.get(category_name)

            if category_id is None:
                raise ValueError(f"Kategori tidak ditemukan di database: {category_name}")

            conn.execute(query, {
                "user_id": user_id,
                "category_id": int(category_id),
                "tanggal_transaksi": row["tanggal_transaksi"],
                "transaction_type": row["transaction_type"],
                "tujuan_transaksi": row["tujuan_transaksi"],
                "keterangan": row["keterangan"],
                "payment_method": row["payment_method"],
                "amount": float(row["amount"]),
                "source": "import_file"
            })