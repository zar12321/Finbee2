import streamlit as st
from modules.db import (
    test_connection,
    load_users,
    load_categories,
    load_transactions,
    insert_user,
    insert_transaction
)

st.set_page_config(
    page_title="FinBee",
    page_icon="🐝",
    layout="wide"
)
import plotly.express as px
from modules.analysis import (
    get_summary_metrics,
    analyze_by_category,
    analyze_by_payment_method,
    get_monthly_trend,
    get_top_transactions
)
# =========================
# SESSION STATE DEFAULT
# =========================

if "main_page" not in st.session_state:
    st.session_state.main_page = "Dashboard"

if "dashboard_page" not in st.session_state:
    st.session_state.dashboard_page = "Home Dashboard"

if "insight_page" not in st.session_state:
    st.session_state.insight_page = "Home Insight AI"


# =========================
# SIDEBAR UTAMA
# =========================

st.sidebar.title("🐝 FinBee")

main_page = st.sidebar.radio(
    "Menu Utama",
    ["Dashboard", "Insight AI"],
    index=["Dashboard", "Insight AI"].index(st.session_state.main_page)
)

st.session_state.main_page = main_page


# =========================
# TOMBOL KEMBALI
# =========================

def back_to_dashboard_home():
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.dashboard_page = "Home Dashboard"
        st.rerun()


def back_to_insight_home():
    if st.button("⬅️ Kembali ke Insight AI"):
        st.session_state.insight_page = "Home Insight AI"
        st.rerun()


# =========================
# DASHBOARD HOME
# =========================

def dashboard_home():
    st.title("🐝 FinBee Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("👤 Profil User", use_container_width=True):
            st.session_state.dashboard_page = "Profil User"
            st.rerun()

    with col2:
        if st.button("➕ Tambah Transaksi", use_container_width=True):
            st.session_state.dashboard_page = "Tambah Transaksi"
            st.rerun()

    with col3:
        if st.button("📁 Import File", use_container_width=True):
            st.session_state.dashboard_page = "Import File"
            st.rerun()

    with col4:
        if st.button("📊 Analisis & Prediksi", use_container_width=True):
            st.session_state.dashboard_page = "Analisis & Prediksi"
            st.rerun()

    st.divider()

    try:
        users_df = load_users()
        categories_df = load_categories()
        transactions_df = load_transactions()

        st.subheader("Ringkasan Data")

        summary = get_summary_metrics(transactions_df)

        m1, m2, m3, m4, m5 = st.columns(5)

        m1.metric("Jumlah User", len(users_df))
        m2.metric("Jumlah Transaksi", summary["transaction_count"])
        m3.metric("Total Pemasukan", f"Rp {summary['total_income']:,.0f}")
        m4.metric("Total Pengeluaran", f"Rp {summary['total_expense']:,.0f}")
        m5.metric("Saldo Bersih", f"Rp {summary['balance']:,.0f}")

        st.divider()

        if transactions_df.empty:
            st.info("Belum ada transaksi. Tambahkan transaksi terlebih dahulu.")
            return

        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("Pengeluaran per Kategori")

            category_df = analyze_by_category(transactions_df)

            if category_df.empty:
                st.info("Belum ada data pengeluaran.")
            else:
                fig = px.bar(
                    category_df,
                    x="category_name",
                    y="amount",
                    title="Total Pengeluaran Berdasarkan Kategori",
                    labels={
                        "category_name": "Kategori",
                        "amount": "Total Pengeluaran"
                    }
                )

                st.plotly_chart(fig, use_container_width=True)

        with col_right:
            st.subheader("Penggunaan Metode Pembayaran")

            payment_df = analyze_by_payment_method(transactions_df)

            if payment_df.empty:
                st.info("Belum ada data metode pembayaran.")
            else:
                fig = px.pie(
                    payment_df,
                    names="payment_method",
                    values="amount",
                    title="Distribusi Transaksi Berdasarkan Metode Pembayaran"
                )

                st.plotly_chart(fig, use_container_width=True)

        st.subheader("Top 5 Transaksi Terbesar")

        top_df = get_top_transactions(transactions_df)

        st.dataframe(top_df, use_container_width=True)

    except Exception as e:
        st.error(f"Gagal memuat dashboard: {e}")


# =========================
# HALAMAN PROFIL USER
# =========================

def page_profil_user():
    back_to_dashboard_home()

    st.title("👤 Profil User")
    st.write("Tambahkan user yang akan menggunakan aplikasi FinBee.")

    with st.form("form_tambah_user"):
        nama = st.text_input("Nama User")
        umur = st.number_input("Umur", min_value=0, max_value=120, step=1)
        pekerjaan = st.text_input("Pekerjaan")
        pemasukan_bulanan = st.number_input(
            "Pemasukan Bulanan",
            min_value=0.0,
            step=10000.0
        )
        target_tabungan = st.number_input(
            "Target Tabungan",
            min_value=0.0,
            step=10000.0
        )

        submitted = st.form_submit_button("Simpan User")

        if submitted:
            if nama.strip() == "":
                st.warning("Nama user tidak boleh kosong.")
            else:
                try:
                    insert_user(
                        nama=nama,
                        umur=umur,
                        pekerjaan=pekerjaan,
                        pemasukan_bulanan=pemasukan_bulanan,
                        target_tabungan=target_tabungan
                    )

                    st.success("User berhasil ditambahkan.")
                    st.rerun()

                except Exception as e:
                    st.error(f"Gagal menambahkan user: {e}")

    st.divider()

    st.subheader("Daftar User")

    try:
        users_df = load_users()

        if users_df.empty:
            st.info("Belum ada user.")
        else:
            st.dataframe(users_df, use_container_width=True)

    except Exception as e:
        st.error(f"Gagal memuat data user: {e}")


# =========================
# HALAMAN PLACEHOLDER
# =========================

def page_tambah_transaksi():
    back_to_dashboard_home()

    st.title("➕ Tambah Transaksi")
    st.write("Tambahkan transaksi baru untuk user yang sudah terdaftar.")

    try:
        users_df = load_users()
        categories_df = load_categories()
    except Exception as e:
        st.error(f"Gagal memuat data user atau kategori: {e}")
        return

    if users_df.empty:
        st.warning("Belum ada user. Tambahkan user terlebih dahulu di menu Profil User.")
        return

    if categories_df.empty:
        st.warning("Belum ada kategori. Jalankan seed_data.sql terlebih dahulu.")
        return

    with st.form("form_tambah_transaksi"):
        selected_user = st.selectbox(
            "Pilih User",
            users_df["nama"].tolist()
        )

        selected_category = st.selectbox(
            "Pilih Kategori",
            categories_df["category_name"].tolist()
        )

        tanggal_transaksi = st.date_input("Tanggal Transaksi")

        transaction_type = st.selectbox(
            "Tipe Transaksi",
            ["expense", "income"]
        )

        payment_method = st.selectbox(
            "Metode Pembayaran",
            ["Cash", "Debit", "E-Wallet", "Bank Transfer", "Credit Card", "Other"]
        )

        tujuan_transaksi = st.text_input(
            "Tujuan Transaksi",
            placeholder="Contoh: makan siang, bayar kos, gaji bulanan"
        )

        keterangan = st.text_area(
            "Keterangan",
            placeholder="Contoh: beli nasi ayam di kantin"
        )

        amount = st.number_input(
            "Nominal",
            min_value=0.0,
            step=1000.0
        )

        submitted = st.form_submit_button("Simpan Transaksi")

        if submitted:
            if amount <= 0:
                st.warning("Nominal transaksi harus lebih dari 0.")
            elif tujuan_transaksi.strip() == "":
                st.warning("Tujuan transaksi tidak boleh kosong.")
            else:
                try:
                    user_id = int(
                        users_df.loc[
                            users_df["nama"] == selected_user,
                            "user_id"
                        ].iloc[0]
                    )

                    category_id = int(
                        categories_df.loc[
                            categories_df["category_name"] == selected_category,
                            "category_id"
                        ].iloc[0]
                    )

                    insert_transaction(
                        user_id=user_id,
                        category_id=category_id,
                        tanggal_transaksi=tanggal_transaksi,
                        transaction_type=transaction_type,
                        tujuan_transaksi=tujuan_transaksi,
                        keterangan=keterangan,
                        payment_method=payment_method,
                        amount=amount,
                        source="manual"
                    )

                    st.success("Transaksi berhasil disimpan.")
                    st.rerun()

                except Exception as e:
                    st.error(f"Gagal menyimpan transaksi: {e}")

    st.divider()

    st.subheader("Daftar Transaksi")

    try:
        transactions_df = load_transactions()

        if transactions_df.empty:
            st.info("Belum ada transaksi.")
        else:
            st.dataframe(transactions_df, use_container_width=True)

    except Exception as e:
        st.error(f"Gagal memuat transaksi: {e}")

def page_import_file():
    back_to_dashboard_home()
    st.title("📁 Import File")
    st.info("Tahap berikutnya: membuat fitur upload CSV/Excel/PDF/TXT.")


def page_analisis_prediksi():
    back_to_dashboard_home()

    st.title("📊 Analisis & Prediksi")

    pilihan = st.selectbox(
        "Pilih jenis analisis",
        [
            "Analisis Kategori",
            "Analisis Metode Pembayaran",
            "Tren Bulanan",
            "Prediksi Bulan Depan"
        ]
    )

    try:
        transactions_df = load_transactions()

        if transactions_df.empty:
            st.info("Belum ada transaksi untuk dianalisis.")
            return

        if pilihan == "Analisis Kategori":
            st.subheader("Analisis Kategori")

            category_df = analyze_by_category(transactions_df)

            if category_df.empty:
                st.info("Belum ada data pengeluaran.")
            else:
                fig = px.bar(
                    category_df,
                    x="category_name",
                    y="amount",
                    title="Pengeluaran Berdasarkan Kategori",
                    labels={
                        "category_name": "Kategori",
                        "amount": "Total Pengeluaran"
                    }
                )

                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(category_df, use_container_width=True)

        elif pilihan == "Analisis Metode Pembayaran":
            st.subheader("Analisis Metode Pembayaran")

            payment_df = analyze_by_payment_method(transactions_df)

            fig = px.bar(
                payment_df,
                x="payment_method",
                y="amount",
                title="Total Transaksi Berdasarkan Metode Pembayaran",
                labels={
                    "payment_method": "Metode Pembayaran",
                    "amount": "Total Nominal"
                }
            )

            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(payment_df, use_container_width=True)

        elif pilihan == "Tren Bulanan":
            st.subheader("Tren Bulanan")

            monthly_df = get_monthly_trend(transactions_df)

            fig = px.line(
                monthly_df,
                x="tanggal_transaksi",
                y="amount",
                color="transaction_type",
                markers=True,
                title="Tren Bulanan Pemasukan dan Pengeluaran",
                labels={
                    "tanggal_transaksi": "Bulan",
                    "amount": "Total Nominal",
                    "transaction_type": "Tipe Transaksi"
                }
            )

            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(monthly_df, use_container_width=True)

        elif pilihan == "Prediksi Bulan Depan":
            st.subheader("Prediksi Bulan Depan")
            st.info("Tahap berikutnya: kita buat model prediksi sederhana dengan moving average atau linear regression.")

    except Exception as e:
        st.error(f"Gagal melakukan analisis: {e}")

# =========================
# INSIGHT AI HOME
# =========================

def insight_home():
    st.title("🤖 Insight AI")
    st.write("Pilih fitur AI yang ingin digunakan.")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⚙️ Pengaturan", use_container_width=True):
            st.session_state.insight_page = "Pengaturan"
            st.rerun()

    with col2:
        if st.button("💬 Chatbot AI", use_container_width=True):
            st.session_state.insight_page = "Chatbot AI"
            st.rerun()

    with col3:
        if st.button("🧠 Rekomendasi AI", use_container_width=True):
            st.session_state.insight_page = "Rekomendasi AI"
            st.rerun()


def page_pengaturan():
    back_to_insight_home()
    st.title("⚙️ Pengaturan AI")
    st.info("Tahap berikutnya: input provider AI, model, dan API key user.")


def page_chatbot_ai():
    back_to_insight_home()
    st.title("💬 Chatbot AI")
    st.info("Tahap berikutnya: membuat chatbot berbasis ringkasan transaksi.")


def page_rekomendasi_ai():
    back_to_insight_home()
    st.title("🧠 Rekomendasi AI")
    st.info("Tahap berikutnya: membuat rekomendasi finansial berbasis data.")


# =========================
# ROUTING UTAMA
# =========================

if st.session_state.main_page == "Dashboard":

    if st.session_state.dashboard_page == "Home Dashboard":
        dashboard_home()

    elif st.session_state.dashboard_page == "Profil User":
        page_profil_user()

    elif st.session_state.dashboard_page == "Tambah Transaksi":
        page_tambah_transaksi()

    elif st.session_state.dashboard_page == "Import File":
        page_import_file()

    elif st.session_state.dashboard_page == "Analisis & Prediksi":
        page_analisis_prediksi()


elif st.session_state.main_page == "Insight AI":

    if st.session_state.insight_page == "Home Insight AI":
        insight_home()

    elif st.session_state.insight_page == "Pengaturan":
        page_pengaturan()

    elif st.session_state.insight_page == "Chatbot AI":
        page_chatbot_ai()

    elif st.session_state.insight_page == "Rekomendasi AI":
        page_rekomendasi_ai()