INSERT INTO categories (category_name, category_type) VALUES
('Food', 'expense'),
('Transport', 'expense'),
('Bills', 'expense'),
('Shopping', 'expense'),
('Education', 'expense'),
('Health', 'expense'),
('Entertainment', 'expense'),
('Other', 'expense'),
('Salary', 'income'),
('Allowance', 'income');

SELECT * FROM categories;


SELECT * FROM users;

SELECT * FROM transactions;


SELECT
    t.transaction_id,
    u.nama,
    c.category_name,
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
ORDER BY t.transaction_id;




SELECT
    DATE_TRUNC('month', tanggal_transaksi) AS bulan,
    SUM(amount) AS total_pengeluaran
FROM transactions
WHERE transaction_type = 'expense'
GROUP BY bulan
ORDER BY bulan;





SELECT
    user_id,
    category_id,
    tanggal_transaksi,
    transaction_type,
    tujuan_transaksi,
    keterangan,
    payment_method,
    amount,
    source,
    COUNT(*) AS jumlah_duplikat
FROM transactions
GROUP BY
    user_id,
    category_id,
    tanggal_transaksi,
    transaction_type,
    tujuan_transaksi,
    keterangan,
    payment_method,
    amount,
    source
HAVING COUNT(*) > 1
ORDER BY jumlah_duplikat DESC;





SELECT
    user_id,
    category_id,
    tanggal_transaksi,
    transaction_type,
    tujuan_transaksi,
    keterangan,
    payment_method,
    amount,
    source,
    COUNT(*) AS jumlah_duplikat
FROM transactions
GROUP BY
    user_id,
    category_id,
    tanggal_transaksi,
    transaction_type,
    tujuan_transaksi,
    keterangan,
    payment_method,
    amount,
    source
HAVING COUNT(*) > 1
ORDER BY jumlah_duplikat DESC;




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



SELECT
    t.transaction_id,
    u.nama,
    c.category_name,
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