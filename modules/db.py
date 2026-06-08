import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import bcrypt



def get_engine():
    if "database" not in st.secrets:
        raise KeyError(
            "Secrets belum memiliki key [database]. "
            "Tambahkan [database] dengan url di Streamlit Cloud Secrets."
        )

    if "url" not in st.secrets["database"]:
        raise KeyError(
            "Secrets [database] belum memiliki key url."
        )

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
            login_identifier,
            login_type,
            umur,
            pekerjaan,
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
        ORDER BY category_type, category_name;
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
            t.raw_category,
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
        df["tanggal_transaksi"] = pd.to_datetime(df["tanggal_transaksi"])
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    return df

def insert_transaction(
    user_id,
    category_id,
    tanggal_transaksi,
    transaction_type,
    tujuan_transaksi,
    keterangan,
    payment_method,
    amount,
    source="manual",
    raw_category=None
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
                source,
                raw_category
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
                :source,
                :raw_category
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
            "source": source,
            "raw_category": raw_category
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
                source,
                raw_category
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
                :source,
                :raw_category
            )
    """)

    with engine.begin() as conn:
        for _, row in imported_df.iterrows():
            category_name = str(row["category_name"]).strip()
            category_id = category_map.get(category_name)

            if category_id is None:
                category_name = "Other"
                category_id = category_map.get("Other")

            if category_id is None:
                raise ValueError("Kategori 'Other' tidak ditemukan di database.")

            raw_category = row.get("raw_category", category_name)
            raw_category = str(raw_category).strip()

            conn.execute(query, {
                "user_id": user_id,
                "category_id": int(category_id),
                "tanggal_transaksi": row["tanggal_transaksi"],
                "transaction_type": row["transaction_type"],
                "tujuan_transaksi": row["tujuan_transaksi"],
                "keterangan": row["keterangan"],
                "payment_method": row["payment_method"],
                "amount": float(row["amount"]),
                "source": "import_file",
                "raw_category": raw_category
            })

def hash_password(password):
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode("utf-8")


def check_password(password, password_hash):
    password_bytes = password.encode("utf-8")
    hash_bytes = password_hash.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hash_bytes)


def register_user(
    nama,
    login_identifier,
    login_type,
    password,
    umur,
    pekerjaan
):
    engine = get_engine()

    login_identifier = login_identifier.strip().lower()
    password_hash = hash_password(password)

    query = text("""
        INSERT INTO users
            (
                nama,
                login_identifier,
                login_type,
                password_hash,
                umur,
                pekerjaan
            )
        VALUES
            (
                :nama,
                :login_identifier,
                :login_type,
                :password_hash,
                :umur,
                :pekerjaan
            )
        RETURNING user_id, nama, login_identifier, login_type
    """)

    with engine.begin() as conn:
        result = conn.execute(query, {
            "nama": nama,
            "login_identifier": login_identifier,
            "login_type": login_type,
            "password_hash": password_hash,
            "umur": umur,
            "pekerjaan": pekerjaan
        })

        user = result.fetchone()

    return user

def login_user_by_identifier(login_identifier, password):
    engine = get_engine()

    login_identifier = login_identifier.strip().lower()

    query = text("""
        SELECT
            user_id,
            nama,
            login_identifier,
            login_type,
            password_hash
        FROM users
        WHERE login_identifier = :login_identifier
        LIMIT 1
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {
            "login_identifier": login_identifier
        })

        user = result.fetchone()

    if user is None:
        return None

    if user.password_hash is None:
        return None

    if check_password(password, user.password_hash):
        return user

    return None

def reset_user_password(login_identifier, new_password):
    engine = get_engine()

    login_identifier = login_identifier.strip().lower()
    password_hash = hash_password(new_password)

    query = text("""
        UPDATE users
        SET password_hash = :password_hash
        WHERE login_identifier = :login_identifier
    """)

    with engine.begin() as conn:
        result = conn.execute(query, {
            "login_identifier": login_identifier,
            "password_hash": password_hash
        })

    return result.rowcount

def save_monthly_plan(
    user_id,
    bulan,
    tahun,
    target_bulanan,
    pemasukan_bulanan=0
):
    engine = get_engine()

    query = text("""
        INSERT INTO monthly_plans
            (
                user_id,
                bulan,
                tahun,
                pemasukan_bulanan,
                target_bulanan
            )
        VALUES
            (
                :user_id,
                :bulan,
                :tahun,
                :pemasukan_bulanan,
                :target_bulanan
            )
        ON CONFLICT (user_id, bulan, tahun)
        DO UPDATE SET
            pemasukan_bulanan = EXCLUDED.pemasukan_bulanan,
            target_bulanan = EXCLUDED.target_bulanan,
            updated_at = CURRENT_TIMESTAMP
    """)

    with engine.begin() as conn:
        conn.execute(query, {
            "user_id": user_id,
            "bulan": bulan,
            "tahun": tahun,
            "pemasukan_bulanan": pemasukan_bulanan,
            "target_bulanan": target_bulanan
        })


def load_monthly_plan(user_id, bulan, tahun):
    engine = get_engine()

    query = text("""
        SELECT
            plan_id,
            user_id,
            bulan,
            tahun,
            pemasukan_bulanan,
            target_bulanan
        FROM monthly_plans
        WHERE user_id = :user_id
          AND bulan = :bulan
          AND tahun = :tahun
        LIMIT 1
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {
            "user_id": user_id,
            "bulan": bulan,
            "tahun": tahun
        })

        row = result.fetchone()

    return row