from sqlalchemy import text
from modules.db import get_engine

engine = get_engine()

with engine.begin() as conn:
    result = conn.execute(
        text("""
            DELETE FROM transactions
            WHERE user_id IN (
                SELECT user_id
                FROM users
                WHERE login_identifier = :login_identifier
            )
        """),
        {
            "login_identifier": "ldruszardii@gmail.com"
        }
    )

print(f"{result.rowcount} transaksi berhasil dihapus")