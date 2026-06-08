INSERT INTO categories (category_name, category_type)
VALUES
    ('Food', 'expense'),
    ('Transport', 'expense'),
    ('Bills', 'expense'),
    ('Shopping', 'expense'),
    ('Education', 'expense'),
    ('Health', 'expense'),
    ('Entertainment', 'expense'),
    ('Other', 'expense'),
    ('Salary', 'income'),
    ('Allowance', 'income')
ON CONFLICT (category_name, category_type) DO NOTHING;