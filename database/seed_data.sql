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