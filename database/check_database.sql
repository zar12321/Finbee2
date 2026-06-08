SELECT * FROM categories;

SELECT * FROM users;

SELECT * FROM transactions;

SELECT
    t.transaction_id,
    u.nama,
    c.category_name,
    t.raw_category,
    t.tanggal_transaksi,
    t.transaction_type,
    t.tujuan_transaksi,
    t.keterangan,
    t.payment_method,
    t.amount,
    t.source
FROM transactions t
JOIN users u
    ON t.user_id = u.user_id
LEFT JOIN categories c
    ON t.category_id = c.category_id
ORDER BY t.transaction_id DESC;