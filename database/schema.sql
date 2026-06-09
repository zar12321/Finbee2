CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    login_identifier VARCHAR(100) UNIQUE NOT NULL,
    login_type VARCHAR(20) NOT NULL,
    password_hash TEXT NOT NULL,
    umur INT,
    pekerjaan VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    category_type VARCHAR(20) DEFAULT 'expense',
    CONSTRAINT unique_category_name_type UNIQUE (category_name, category_type)
);

CREATE TABLE import_files (
    import_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    file_name VARCHAR(255),
    file_type VARCHAR(50),
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50),
    total_rows INT,
    imported_rows INT,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT,
    import_id INT,
    tanggal_input DATE DEFAULT CURRENT_DATE,
    tanggal_transaksi DATE NOT NULL,
    transaction_type VARCHAR(20) DEFAULT 'expense',
    tujuan_transaksi VARCHAR(100),
    keterangan TEXT,
    payment_method VARCHAR(50),
    amount FLOAT NOT NULL,
    source VARCHAR(50) DEFAULT 'manual',
    raw_category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (import_id) REFERENCES import_files(import_id)
);

CREATE TABLE staging_transactions (
    staging_id SERIAL PRIMARY KEY,
    import_id INT,
    user_id INT,
    raw_tanggal VARCHAR(100),
    raw_keterangan TEXT,
    raw_amount VARCHAR(100),
    raw_payment_method VARCHAR(100),
    raw_category VARCHAR(100),
    parsed_tanggal DATE,
    parsed_amount FLOAT,
    predicted_category_id INT,
    is_valid BOOLEAN DEFAULT FALSE,
    error_message TEXT,

    FOREIGN KEY (import_id) REFERENCES import_files(import_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (predicted_category_id) REFERENCES categories(category_id)
);

CREATE TABLE ai_recommendations (
    recommendation_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    period_start DATE,
    period_end DATE,
    summary TEXT,
    recommendation TEXT,
    provider VARCHAR(50),
    model_name VARCHAR(100),

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE chat_history (
    chat_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    role VARCHAR(20),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    provider VARCHAR(50),
    model_name VARCHAR(100),

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE monthly_plans (
    plan_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    bulan INT NOT NULL,
    tahun INT NOT NULL,
    pemasukan_bulanan FLOAT NOT NULL,
    target_bulanan FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id),
    CONSTRAINT unique_monthly_plan_user_period UNIQUE (user_id, bulan, tahun)
);
