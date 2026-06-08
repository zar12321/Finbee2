# Finbee2
FinBee adalah aplikasi pencatatan dan analisis keuangan pribadi berbasis Streamlit. Aplikasi ini membantu user mencatat transaksi, mengimpor file transaksi, melihat ringkasan keuangan, memantau batas pengeluaran bulanan, melakukan analisis sederhana, prediksi pengeluaran bulan depan, serta mendapatkan insight menggunakan AI.

Fitur Utama
1. Autentikasi User
-Register akun menggunakan email atau username
-Login menggunakan email atau username
-Reset password
-Password disimpan dalam bentuk hash menggunakan bcrypt
2. Dashboard Keuangan
-Jumlah transaksi
-Total pemasukan
-Total pengeluaran
-Saldo bersih
-Pengeluaran maksimal bulanan
-Status target bulanan :
    -Aman
    -Waspada
    -Melebihi sedikit
    -Melebihi target
3. Profil Saya
-Nama user
-Email atau username login
-Tipe login
-Pengeluaran maksimal bulanan
   disimpan berdasarkan bulan berjalan dan dapat diperbarui setiap bulan.

4. Tambah Transaksi Manual
-Kategori
-Tanggal transaksi
-Tipe transaksi
-Metode pembayaran
-Tujuan transaksi
-Keterangan
-Nominal
-Other
  user dapat memasukkan metode pembayaran secara manual.

6. Import File Transaksi
-CSV
-Excel
Aplikasi melakukan:
-Mendeteksi kolom tanggal
-Mendeteksi kolom nominal
-Mendeteksi kolom kategori
-Mendeteksi kolom metode pembayaran
-Membersihkan format nominal
-Mengubah tipe transaksi menjadi income atau expense
-Menyimpan kategori asli user sebagai raw_category
-Mengelompokkan kategori ke kategori standar FinBee

7. Analisis dan Prediksi
Prediksi menggunakan pendekatan sederhana berbasis data pengeluaran bulanan yang tersedia.
Terdiri dari:
-Analisis kategori
-Analisis metode pembayaran
-Tren bulanan
-Prediksi pengeluaran bulan depan

8. Insight AI
-Pengaturan provider AI
-Chatbot AI
-Rekomendasi AI

API key disimpan sementara di session aplikasi dan tidak disimpan ke database.
Provider AI yang didukung:
-Gemini
-OpenRouter
-Groq
-Ollama Local



Finbee2/
├── app.py
├── requirements.txt
├── README.md
├── database/
│   ├── schema.sql
│   └── seed_data.sql
├── modules/
│   ├── db.py
│   ├── analysis.py
│   ├── prediction.py
│   ├── import_file.py
│   └── ai_provider.py
└── .gitignore
Teknologi yang Digunakan
Python
Streamlit
PostgreSQL
SQLAlchemy
Pandas
Plotly
bcrypt
Gemini / OpenRouter / Groq / Ollama Local
