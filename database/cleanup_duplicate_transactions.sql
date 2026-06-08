DELETE FROM transactions
WHERE transaction_id IN (
    SELECT transaction_id
    FROM (
        SELECT
            transaction_id,
            ROW_NUMBER() OVER (
                PARTITION BY
                    user_id,
                    category_id,
                    tanggal_transaksi,
                    transaction_type,
                    tujuan_transaksi,
                    keterangan,
                    payment_method,
                    amount,
                    source
                ORDER BY transaction_id
            ) AS row_num
        FROM transactions
    ) duplicated
    WHERE duplicated.row_num > 1
);