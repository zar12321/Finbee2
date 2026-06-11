from sqlalchemy import create_engine, text, bindparam

DATABASE_URL = 'postgresql://neondb_owner:npg_2TCjZwGNFR8c@ep-super-lake-aoslfgfv-pooler.c-2.ap-southeast-1.aws.neon.tech/finbee2_db?sslmode=require&channel_binding=require'

engine = create_engine(DATABASE_URL)

transaction_id = 1   # ganti dengan ID transaksi yang ada
user_id = 1            # ganti user_id kamu

query = text("""
    DELETE FROM transactions
    WHERE transaction_id IN :transaction_ids
      AND user_id = :user_id
""").bindparams(
    bindparam("transaction_ids", expanding=True)
)

with engine.begin() as conn:
    result = conn.execute(
        query,
        {
            "transaction_ids": [transaction_id],
            "user_id": user_id
        }
    )

print("Deleted:", result.rowcount)