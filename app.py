import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="FinBee",
    page_icon="🐝",
    layout="wide"
)

from modules.analysis import (
    get_summary_metrics,
    analyze_by_category,
    analyze_by_payment_method,
    get_monthly_trend,
    get_top_transactions
)

from modules.prediction import predict_next_month_expense
from modules.db import (
    load_categories,
    load_transactions,
    insert_transaction,
    insert_imported_transactions,
    update_transaction,
    delete_transactions,
    register_user,
    login_user_by_identifier,
    reset_user_password,
    save_monthly_plan,
    load_monthly_plan
)

from modules.import_file import auto_clean_financial_file
from modules.ai_provider import generate_ai_response, build_financial_summary
from modules.prediction import predict_next_month_expense

# =========================
# SESSION STATE DEFAULT
# =========================

if "main_page" not in st.session_state:
    st.session_state.main_page = "Dashboard"

if "dashboard_page" not in st.session_state:
    st.session_state.dashboard_page = "Home Dashboard"

if "insight_page" not in st.session_state:
    st.session_state.insight_page = "Home Insight AI"

if "import_success" not in st.session_state:
    st.session_state.import_success = False

if "import_message" not in st.session_state:
    st.session_state.import_message = ""

if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "login_identifier" not in st.session_state:
    st.session_state.login_identifier = None

if "login_type" not in st.session_state:
    st.session_state.login_type = None

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "Login"

valid_auth_pages = ["Login", "Register", "Reset Password"]

if st.session_state.auth_page not in valid_auth_pages:
    st.session_state.auth_page = "Login"

if "monthly_plan_message" not in st.session_state:
    st.session_state.monthly_plan_message = ""

#API MODEL AI
AI_MODEL_OPTIONS = {
    "Gemini": [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "Custom Model"
    ],
    "OpenRouter": [
        "openai/gpt-4o-mini",
        "meta-llama/llama-3.1-8b-instruct",
        "google/gemini-flash-1.5",
        "Custom Model"
    ],
    "Groq": [
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile",
        "Custom Model"
    ],
    "Ollama Local": [
        "llama3.1",
        "mistral",
        "qwen2.5",
        "Custom Model"
    ]
}

if "ai_provider" not in st.session_state:
    st.session_state.ai_provider = "Gemini"

if "ai_model_name" not in st.session_state:
    st.session_state.ai_model_name = AI_MODEL_OPTIONS[st.session_state.ai_provider][0]

if "ai_api_key" not in st.session_state:
    st.session_state.ai_api_key = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def page_login():
    st.title("🐝 FinBee Login")
    st.write("Masuk menggunakan email atau username yang sudah didaftarkan.")

    with st.form("form_login"):
        login_identifier = st.text_input("Email atau Username")
        password = st.text_input("Password", type="password")

        st.caption("Tekan Enter atau klik tombol Login untuk masuk.")

        submitted = st.form_submit_button("Login")

        if submitted:
            login_identifier = login_identifier.strip().lower()

            if login_identifier == "" or password.strip() == "":
                st.warning("Email/username dan password wajib diisi.")
                return

            try:
                user = login_user_by_identifier(login_identifier,password)

                if user is None:
                    st.error("Email/username atau password salah.")
                    return

                st.session_state.is_logged_in = True
                st.session_state.user_id = int(user.user_id)
                st.session_state.user_name = user.nama
                st.session_state.login_identifier = user.login_identifier
                st.session_state.login_type = user.login_type

                st.session_state.main_page = "Dashboard"
                st.session_state.dashboard_page = "Home Dashboard"
                st.session_state.insight_page = "Home Insight AI"

                st.success("Login berhasil.")
                st.rerun()

            except Exception as e:
                st.error(f"Gagal login: {e}")

    st.divider()

    if st.button("Lupa Password?"):
        st.session_state.auth_page = "Reset Password"
        st.rerun()

    if st.button("Belum punya akun? Daftar"):
        st.session_state.auth_page = "Register"
        st.rerun()

def page_register():
    st.title("🐝 Daftar Akun FinBee")
    st.write("Buat akun baru untuk menyimpan dan menganalisis data keuanganmu.")

    with st.form("form_register"):
        nama = st.text_input("Nama Lengkap")
        login_identifier = st.text_input("Email atau Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Konfirmasi Password", type="password")

        umur = st.number_input(
            "Umur",
            min_value=0,
            max_value=120,
            step=1
        )

        pekerjaan = st.text_input("Pekerjaan")

        submitted = st.form_submit_button("Daftar")

        if submitted:
            nama = nama.strip()
            login_identifier = login_identifier.strip().lower()

            if nama == "":
                st.warning("Nama wajib diisi.")
                return

            if login_identifier == "":
                st.warning("Email atau username wajib diisi.")
                return

            if password.strip() == "":
                st.warning("Password wajib diisi.")
                return

            if password != confirm_password:
                st.warning("Konfirmasi password tidak cocok.")
                return

            if "@" in login_identifier:
                login_type = "email"
            else:
                login_type = "username"

            try:
                register_user(
                    nama=nama,
                    login_identifier=login_identifier,
                    login_type=login_type,
                    password=password,
                    umur=umur,
                    pekerjaan=pekerjaan
                )

                st.success("Akun berhasil dibuat. Silakan login.")
                st.session_state.auth_page = "Login"
                st.rerun()

            except Exception as e:
                st.error(f"Gagal membuat akun: {e}")

    st.divider()

    if st.button("Sudah punya akun? Login"):
        st.session_state.auth_page = "Login"
        st.rerun()

def page_reset_password():
    st.title("🔐 Reset Password FinBee")
    st.write("Masukkan email atau username akun, lalu buat password baru.")

    with st.form("form_reset_password"):
        login_identifier = st.text_input("Email atau Username")
        new_password = st.text_input("Password Baru", type="password")
        confirm_password = st.text_input("Konfirmasi Password Baru", type="password")

        submitted = st.form_submit_button("Reset Password")

        if submitted:
            login_identifier = login_identifier.strip().lower()

            if login_identifier == "":
                st.warning("Email atau username wajib diisi.")
                return

            if new_password.strip() == "":
                st.warning("Password baru wajib diisi.")
                return

            if new_password != confirm_password:
                st.warning("Konfirmasi password tidak cocok.")
                return

            try:
                affected_rows = reset_user_password(
                    login_identifier=login_identifier,
                    new_password=new_password
                )

                if affected_rows == 0:
                    st.error("Akun tidak ditemukan.")
                    return

                st.success("Password berhasil direset. Silakan login dengan password baru.")
                st.session_state.auth_page = "Login"
                st.rerun()

            except Exception as e:
                st.error(f"Gagal reset password: {e}")

    st.divider()

    if st.button("Kembali ke Login"):
        st.session_state.auth_page = "Login"
        st.rerun()

# =========================
# TOMBOL KEMBALI
# =========================
def back_to_dashboard_home(key="back_dashboard"):
    if st.button("⬅️ Kembali ke Dashboard", key=key):
        st.session_state.dashboard_page = "Home Dashboard"
        st.rerun()

def back_to_insight_home(key="back_insight"):
    if st.button("⬅️ Kembali ke Insight AI", key=key):
        st.session_state.insight_page = "Home Insight AI"
        st.rerun()

#PROFIL SAYA
def page_profil_saya():
    st.title("👤 Profil Saya")
    st.divider()

    st.subheader("Rencana Bulanan")

    if st.session_state.monthly_plan_message != "":
        st.success(st.session_state.monthly_plan_message)

    today = pd.Timestamp.today()
    bulan = int(today.month)
    tahun = int(today.year)

    try:
        existing_plan = load_monthly_plan(
            user_id=st.session_state.user_id,
            bulan=int(bulan),
            tahun=int(tahun)
        )

        if existing_plan is not None:
            default_pemasukan = float(existing_plan.pemasukan_bulanan)
            default_target = float(existing_plan.target_bulanan)
        else:
            default_pemasukan = 0.0
            default_target = 0.0

    except Exception as e:
        st.error(f"Gagal memuat rencana bulanan: {e}")
        return

    target_bulanan = money_input(
        "Pengeluaran Maksimal",
        key=f"target_bulanan_{bulan}_{int(tahun)}",
        default_value=int(default_target)
    )

    if st.button("Simpan Rencana Bulanan"):
        if target_bulanan is None:
            st.warning("Target bulanan tidak valid.")
            return

        if target_bulanan <= 0:
            st.warning("Target bulanan harus lebih dari 0.")
            return

        try:
            save_monthly_plan(
                user_id=st.session_state.user_id,
                bulan=bulan,
                tahun=tahun,
                target_bulanan=target_bulanan
            )

            st.session_state.monthly_plan_message = "Rencana bulanan berhasil disimpan."

            key_target = f"pengeluaran_maksimal{bulan}_{tahun}"

            if key_target in st.session_state:
                del st.session_state[key_target]

            st.rerun()

        except Exception as e:
            st.error(f"Gagal menyimpan rencana bulanan: {e}")

    st.info(
        "Pengeluaran Maksimal disimpan berdasarkan bulan dan tahun, "
        "jadi nilainya bisa diubah setiap bulan."
    )

# =========================
# DASHBOARD HOME
# =========================
def dashboard_home():
    st.title("🐝 FinBee Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("➕ Tambah Transaksi", use_container_width=True):
            st.session_state.dashboard_page = "Tambah Transaksi"
            st.rerun()

    with col2:
        if st.button("📁 Import File", use_container_width=True):
            st.session_state.dashboard_page = "Import File"
            st.rerun()

    with col3:
        if st.button("📊 Analisis & Prediksi", use_container_width=True):
            st.session_state.dashboard_page = "Analisis & Prediksi"
            st.rerun()

    st.divider()

    try:
        categories_df = load_categories()
        transactions_df = load_transactions()

        if st.session_state.user_id is not None:
            transactions_df = transactions_df[
            transactions_df["user_id"] == st.session_state.user_id
    ]
       
        st.subheader("Ringkasan Data")

        summary = get_summary_metrics(transactions_df)

        today = pd.Timestamp.today()
        current_month = int(today.month)
        current_year = int(today.year)

        monthly_plan = load_monthly_plan(
            user_id=st.session_state.user_id,
            bulan=current_month,
            tahun=current_year
        )

        if monthly_plan is not None:
            pemasukan_bulanan = float(monthly_plan.pemasukan_bulanan)
            target_bulanan = float(monthly_plan.target_bulanan)
        else:
            pemasukan_bulanan = 0.0
            target_bulanan = 0.0

        m1, m2, m3, m4, m5 = st.columns(5)

        m1.metric("Jumlah Transaksi", summary["transaction_count"])
        m2.metric("Total Pemasukan", f"Rp {summary['total_income']:,.0f}")
        m3.metric("Total Pengeluaran", f"Rp {summary['total_expense']:,.0f}")
        m4.metric("Saldo Bersih", f"Rp {summary['balance']:,.0f}")

        if target_bulanan > 0:
            m5.metric("Pengeluaran Maksimal", f"Rp {target_bulanan:,.0f}")
        else:
            m5.metric("Pengeluaran Maksimal", "Belum diatur")

        st.subheader("Pengeluaran Maksimal Bulanan")

        if target_bulanan <= 0:
            st.warning("Pengeluaran Maksimal belum diatur. Atur di menu Profil Saya.")
        else:
            total_pengeluaran = summary["total_expense"]
            persentase_target = (total_pengeluaran / target_bulanan) * 100

            sisa_target = target_bulanan - total_pengeluaran

            if persentase_target < 80:
                st.success(
                    f"Aman. Pengeluaran saat ini Rp {total_pengeluaran:,.0f}, "
                    f"masih tersisa Rp {sisa_target:,.0f} dari Pengeluaran Maksimal."
                )

            elif persentase_target <= 100:
                st.warning(
                    f"Waspada. Pengeluaran sudah mencapai {persentase_target:.1f}% "
                    f"Sisa Pengeluaran Maksimal Rp {sisa_target:,.0f}."
                )

            else:
                kelebihan = total_pengeluaran - target_bulanan

                if persentase_target <= 110:
                    st.error(
                        f"Melebihi sedikit. Pengeluaran melewati target sebesar "
                        f"Rp {kelebihan:,.0f}. Perlu dikendalikan."
                    )
                else:
                    st.error(
                        f"Melebihi target. Pengeluaran sudah mencapai {persentase_target:.1f}% "
                        f"dari Pengeluaran Maksimal dan melewati batas sebesar Rp {kelebihan:,.0f}."
                    )

        prediction_result = predict_next_month_expense(transactions_df)

        st.metric(
            "Prediksi Pengeluaran Bulan Depan",
            f"Rp {prediction_result['prediction']:,.0f}"
        )

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

def money_input(label, key, default_value=0):
    default_text = f"{int(default_value):,}" if default_value else ""

    value_text = st.text_input(
        label,
        value=default_text,
        key=key,
        placeholder="Contoh: 10000"
    )

    cleaned_value = value_text.replace(",", "").strip()

    if cleaned_value == "":
        return 0

    if not cleaned_value.isdigit():
        st.warning(f"{label} hanya boleh berisi angka.")
        return None

    return int(cleaned_value)

# =========================
# HALAMAN PLACEHOLDER
# =========================
def page_tambah_transaksi():
    back_to_dashboard_home(key="back_from_transaction")

    st.title("➕ Tambah Transaksi")

    user_id = st.session_state.user_id

    try:
        categories_df = load_categories()
    except Exception as e:
        st.error(f"Gagal memuat kategori: {e}")
        return

    if categories_df.empty:
        st.warning("Belum ada kategori. Jalankan seed_data.sql terlebih dahulu.")
        return

    # =========================
    # INPUT TRANSAKSI
    # tidak memakai st.form agar bagian Other bisa langsung tampil
    # =========================
    selected_category = st.selectbox(
        "Pilih Kategori",
        categories_df["category_name"].tolist()
    )

    tanggal_transaksi = st.date_input("Tanggal Transaksi")

    transaction_type = st.selectbox(
        "Tipe Transaksi",
        ["expense", "income"]
    )

    payment_method_option = st.selectbox(
        "Metode Pembayaran",
        ["Cash", "Debit", "E-Wallet", "Bank Transfer", "Credit Card", "Other"]
    )

    if payment_method_option == "Other":
        custom_payment_method = st.text_input(
            "Masukkan Metode Pembayaran Lainnya",
            placeholder="Contoh: QRIS, GoPay, Dana, ShopeePay, PayLater"
        )

        payment_method = custom_payment_method.strip()
    else:
        payment_method = payment_method_option

    tujuan_transaksi = st.text_input(
        "Tujuan Transaksi",
        placeholder="Contoh: makan siang, bayar kos, gaji bulanan"
    )

    keterangan = st.text_area(
        "Keterangan",
        placeholder="Contoh: beli nasi ayam di kantin"
    )

    amount = money_input(
        "Nominal",
        key="manual_transaction_amount"
    )

    if st.button("Simpan Transaksi"):
        if amount is None:
            st.warning("Nominal transaksi tidak valid.")
            return

        if amount <= 0:
            st.warning("Nominal transaksi harus lebih dari 0.")
            return

        if tujuan_transaksi.strip() == "":
            st.warning("Tujuan transaksi tidak boleh kosong.")
            return

        if payment_method == "":
            st.warning("Metode pembayaran lainnya tidak boleh kosong.")
            return

        try:
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
            st.cache_data.clear()

            if "manual_transaction_amount" in st.session_state:
                del st.session_state.manual_transaction_amount

            st.rerun()

        except Exception as e:
            st.error(f"Gagal menyimpan transaksi: {e}")
  
    st.divider()

    st.subheader("Daftar Transaksi Saya")

    try:
        transactions_df = load_transactions()

        user_transactions = transactions_df[
            transactions_df["user_id"] == st.session_state.user_id
        ].copy()

        if user_transactions.empty:
            st.info("Belum ada transaksi untuk akun ini.")
        else:
            categories_df = load_categories()
            category_options = sorted(
                categories_df["category_name"].dropna().unique().tolist()
            )

            category_id_map = dict(
                zip(categories_df["category_name"], categories_df["category_id"])
            )

            display_df = user_transactions[
                [
                    "transaction_id",
                    "tanggal_transaksi",
                    "category_name",
                    "raw_category",
                    "transaction_type",
                    "tujuan_transaksi",
                    "keterangan",
                    "payment_method",
                    "amount",
                    "source"
                ]
            ].copy()

            display_df["Hapus"] = False

            display_df = display_df[
                [
                    "Hapus",
                    "transaction_id",
                    "tanggal_transaksi",
                    "category_name",
                    "raw_category",
                    "transaction_type",
                    "tujuan_transaksi",
                    "keterangan",
                    "payment_method",
                    "amount",
                    "source"
                ]
            ]

            edited_transactions = st.data_editor(
                display_df,
                use_container_width=True,
                hide_index=True,
                key="transaction_editor",
                disabled=[
                    "transaction_id",
                    "source"
                ],
                column_config={
                    "Hapus": st.column_config.CheckboxColumn(
                        "Hapus",
                        help="Centang transaksi yang ingin dihapus."
                    ),
                    "transaction_id": st.column_config.NumberColumn(
                        "ID",
                        disabled=True
                    ),
                    "tanggal_transaksi": st.column_config.DateColumn(
                        "Tanggal Transaksi",
                        required=True
                    ),
                    "category_name": st.column_config.SelectboxColumn(
                        "Kategori",
                        options=category_options,
                        required=True
                    ),
                    "raw_category": st.column_config.TextColumn(
                        "Kategori Asli",
                        help="Kategori asli dari file import. Boleh dikosongkan untuk transaksi manual."
                    ),
                    "transaction_type": st.column_config.SelectboxColumn(
                        "Tipe",
                        options=["expense", "income"],
                        required=True
                    ),
                    "tujuan_transaksi": st.column_config.TextColumn(
                        "Tujuan Transaksi",
                        required=True
                    ),
                    "keterangan": st.column_config.TextColumn(
                        "Keterangan"
                    ),
                    "payment_method": st.column_config.TextColumn(
                        "Metode Pembayaran",
                        required=True
                    ),
                    "amount": st.column_config.NumberColumn(
                        "Nominal",
                        min_value=0,
                        step=1000,
                        required=True
                    ),
                    "source": st.column_config.TextColumn(
                        "Sumber",
                        disabled=True
                    )
                }
            )

            st.caption(
                "Edit data langsung di tabel, lalu klik Simpan Perubahan. "
                "Untuk menghapus, centang kolom Hapus lalu klik Hapus Baris Terpilih."
            )

            col_save, col_delete = st.columns(2)

            with col_save:
                if st.button("Simpan Perubahan", use_container_width=True):
                    try:
                        updated_count = 0

                        for _, row in edited_transactions.iterrows():
                            transaction_id = int(row["transaction_id"])

                            original_row = display_df[
                                display_df["transaction_id"] == transaction_id
                            ].iloc[0]

                            editable_columns = [
                                "tanggal_transaksi",
                                "category_name",
                                "raw_category",
                                "transaction_type",
                                "tujuan_transaksi",
                                "keterangan",
                                "payment_method",
                                "amount"
                            ]

                            has_changed = any(
                                str(row[col]) != str(original_row[col])
                                for col in editable_columns
                            )

                            if has_changed:
                                category_name = str(row["category_name"]).strip()
                                category_id = category_id_map.get(category_name)

                                if category_id is None:
                                    st.error(f"Kategori tidak valid: {category_name}")
                                    return

                                if str(row["tujuan_transaksi"]).strip() == "":
                                    st.error("Tujuan transaksi tidak boleh kosong.")
                                    return

                                if str(row["payment_method"]).strip() == "":
                                    st.error("Metode pembayaran tidak boleh kosong.")
                                    return

                                if float(row["amount"]) <= 0:
                                    st.error("Nominal harus lebih dari 0.")
                                    return

                                updated_rows = update_transaction(
                                    transaction_id=transaction_id,
                                    user_id=st.session_state.user_id,
                                    category_id=int(category_id),
                                    tanggal_transaksi=row["tanggal_transaksi"],
                                    transaction_type=row["transaction_type"],
                                    tujuan_transaksi=str(row["tujuan_transaksi"]).strip(),
                                    keterangan=str(row["keterangan"]).strip(),
                                    payment_method=str(row["payment_method"]).strip(),
                                    amount=float(row["amount"]),
                                    raw_category=str(row["raw_category"]).strip()
                                    if pd.notna(row["raw_category"])
                                    else None
                                )

                                updated_count += updated_rows

                        if updated_count == 0:
                            st.info("Tidak ada perubahan yang disimpan.")
                        else:
                            st.success(f"{updated_count} transaksi berhasil diperbarui.")
                            st.cache_data.clear()

                            if "transaction_editor" in st.session_state:
                                del st.session_state.transaction_editor

                            st.rerun()

                    except Exception as e:
                        st.error(f"Gagal menyimpan perubahan transaksi: {e}")

            with col_delete:
                selected_delete_df = edited_transactions[
                    edited_transactions["Hapus"] == True
                ]

                if st.button("Hapus Baris Terpilih", use_container_width=True):
                    if selected_delete_df.empty:
                        st.warning("Belum ada transaksi yang dipilih untuk dihapus.")
                        return

                    try:
                        transaction_ids = (
                            selected_delete_df["transaction_id"]
                            .astype(int)
                            .tolist()
                        )

                        deleted_rows = delete_transactions(
                            transaction_ids=transaction_ids,
                            user_id=st.session_state.user_id
                        )

                        st.success(f"{deleted_rows} transaksi berhasil dihapus.")
                        st.cache_data.clear()

                        if "transaction_editor" in st.session_state:
                            del st.session_state.transaction_editor

                        st.rerun()

                    except Exception as e:
                        st.error(f"Gagal menghapus transaksi: {e}")

    except Exception as e:
        st.error(f"Gagal memuat transaksi: {e}")

def apply_column_mapping(df, column_mapping):
    mapped_df = pd.DataFrame()

    for target_col, source_col in column_mapping.items():
        if source_col == "Tidak Ada":
            mapped_df[target_col] = ""
        else:
            mapped_df[target_col] = df[source_col]

    return mapped_df

def page_import_file():
    back_to_dashboard_home(key="back_from_import")

    user_id = st.session_state.user_id

    st.title("📁 Import File")
    st.write("Upload file transaksi dalam format CSV atau Excel. Sistem akan mencoba merapikan data secara otomatis.")

    uploaded_file = st.file_uploader(
        "Pilih file transaksi",
        type=["csv", "xlsx"]
    )

    if "last_uploaded_file" not in st.session_state:
        st.session_state.last_uploaded_file = None

    if "import_success" not in st.session_state:
        st.session_state.import_success = False

    if "import_message" not in st.session_state:
        st.session_state.import_message = ""

    if uploaded_file is None:
        st.info("Silakan upload file CSV atau Excel terlebih dahulu.")
        return

    if st.session_state.last_uploaded_file != uploaded_file.name:
        st.session_state.last_uploaded_file = uploaded_file.name
        st.session_state.import_success = False
        st.session_state.import_message = ""

    st.success(f"File berhasil diupload: {uploaded_file.name}")

    try:
        if uploaded_file.name.endswith(".csv"):
            df_original = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df_original = pd.read_excel(uploaded_file)
        else:
            st.error("Format file belum didukung.")
            return

        with st.expander("Lihat Data Asli"):
            st.dataframe(df_original, use_container_width=True)

        # =========================
        # AUTO CLEAN DATA
        # =========================

        try:
            df_clean = auto_clean_financial_file(df_original)
        except Exception as e:
            st.error(f"Gagal melakukan auto-clean: {e}")
            return

        st.subheader("Data Setelah Auto Clean")
        st.write("Periksa data berikut. Kamu bisa mengedit bagian yang salah atau kosong sebelum disimpan.")

        categories_df = load_categories()
        category_options = sorted(categories_df["category_name"].dropna().unique().tolist())

        transaction_type_options = [
            "expense",
            "income"
        ]

        st.warning(
            "Periksa data sebelum disimpan. Jangan biarkan kolom penting kosong, terutama tanggal, kategori, tipe transaksi, metode pembayaran, dan nominal."
        )

        edited_df = st.data_editor(
            df_clean,
            use_container_width=True,
            num_rows="dynamic",
            key="import_data_editor",
            hide_index=True,
            column_config={
                "tanggal_transaksi": st.column_config.DateColumn(
                    "Tanggal Transaksi",
                    help="Tanggal terjadinya transaksi."
                ),
                "raw_category": st.column_config.TextColumn(
                    "Kategori Asli",
                    help="Kategori asli dari file user. Kolom ini disimpan sebagai jejak data asli."
                ),
                "category_name": st.column_config.SelectboxColumn(
                    "Kategori",
                    help="Pilih kategori transaksi.",
                    options=category_options,
                    required=True
                ),
                "transaction_type": st.column_config.SelectboxColumn(
                    "Tipe Transaksi",
                    help="Pilih expense untuk pengeluaran atau income untuk pemasukan.",
                    options=transaction_type_options,
                    required=True
                ),
                "tujuan_transaksi": st.column_config.TextColumn(
                    "Tujuan Transaksi",
                    help="Ringkasan tujuan transaksi."
                ),
                "keterangan": st.column_config.TextColumn(
                    "Keterangan",
                    help="Detail transaksi."
                ),
                "payment_method": st.column_config.TextColumn(
                    "Metode Pembayaran",
                    help="Isi metode pembayaran. Contoh: Cash, Debit, E-Wallet, QRIS, GoPay, Dana.",
                    required=True
                ),
                "amount": st.column_config.NumberColumn(
                    "Nominal",
                    help="Jumlah nominal transaksi.",
                    min_value=0,
                    step=1000,
                    required=True
                )
            }
        )

        st.subheader("Preview Data Final yang Akan Disimpan")
        st.dataframe(edited_df, use_container_width=True)

        # =========================
        # VALIDASI DATA HASIL EDIT
        # =========================

        st.subheader("Validasi Data")
        
        required_not_empty_columns = [
            "tanggal_transaksi",
            "category_name",
            "transaction_type",
            "tujuan_transaksi",
            "keterangan",
            "payment_method",
            "amount"
        ]

        empty_columns = []

        for col in required_not_empty_columns:
            if edited_df[col].isna().any() or (edited_df[col].astype(str).str.strip() == "").any():
                empty_columns.append(col)

        if len(empty_columns) > 0:
            st.error("Masih ada kolom penting yang kosong. Lengkapi dulu sebelum menyimpan.")
            st.write("Kolom yang masih memiliki nilai kosong:")
            for col in empty_columns:
                st.write(f"- {col}")
            return

        edited_df["tanggal_transaksi"] = pd.to_datetime(
            edited_df["tanggal_transaksi"],
            errors="coerce"
        )

        edited_df["amount"] = pd.to_numeric(
            edited_df["amount"],
            errors="coerce"
        )

        invalid_date_count = edited_df["tanggal_transaksi"].isna().sum()
        invalid_amount_count = edited_df["amount"].isna().sum()

        if invalid_date_count > 0:
            st.error(f"Ada {invalid_date_count} baris dengan tanggal kosong atau tidak valid. Silakan perbaiki di tabel.")
            return

        if invalid_amount_count > 0:
            st.error(f"Ada {invalid_amount_count} baris dengan nominal kosong atau tidak valid. Silakan perbaiki di tabel.")
            return

        allowed_types = ["expense", "income"]

        invalid_type = edited_df[
            ~edited_df["transaction_type"].isin(allowed_types)
        ]

        if not invalid_type.empty:
            st.error("Ada transaction_type yang tidak valid. Gunakan hanya 'expense' atau 'income'.")
            st.dataframe(invalid_type, use_container_width=True)
            return

        categories_df = load_categories()
        valid_categories = categories_df["category_name"].tolist()

        invalid_categories = edited_df[
            ~edited_df["category_name"].isin(valid_categories)
        ]

        if not invalid_categories.empty:
            st.warning("Ada kategori yang tidak sesuai. Sistem akan mengubahnya menjadi 'Other'.")

            if "Other" not in valid_categories:
                st.error("Kategori 'Other' tidak ditemukan di database. Jalankan seed_data.sql terlebih dahulu.")
                return

            edited_df.loc[
                ~edited_df["category_name"].isin(valid_categories),
                "category_name"
            ]= "Other"
           
        st.success("Data valid dan siap disimpan.")

        # =========================
        # PILIH USER PEMILIK DATA
        # =========================
        st.divider()

        if st.session_state.import_success:
            st.success(st.session_state.import_message)
            st.info("Data file ini sudah disimpan. Upload file baru jika ingin import data lain.")
        else:
            if st.button("Simpan Data Import ke Database"):
                try:
                    insert_imported_transactions(
                        user_id=user_id,
                        imported_df=edited_df
                    )

                    st.session_state.import_success = True
                    st.session_state.import_message = "Data import berhasil disimpan ke database."

                    st.cache_data.clear()

                    st.success(st.session_state.import_message)
                    st.info("Data sudah masuk ke database. Jangan tekan simpan ulang untuk file yang sama.")

                except Exception as e:
                    st.error(f"Gagal menyimpan data import: {e}")

    except Exception as e:
        st.error(f"Gagal membaca atau memproses file: {e}")

def page_analisis_prediksi():
    back_to_dashboard_home(key="back_from_analysis")
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
        
        transactions_df = transactions_df[
            transactions_df["user_id"] == st.session_state.user_id
        ]

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

            if payment_df.empty:
                st.info("Belum ada data metode pembayaran.")
            else:
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

            if monthly_df.empty:
                st.info("Belum ada data bulanan.")
            else:
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

            prediction_result = predict_next_month_expense(transactions_df)

            predicted_value = prediction_result["prediction"]
            method = prediction_result["method"]
            monthly_df = prediction_result["monthly_data"]
            message = prediction_result["message"]

            st.metric(
                "Prediksi Pengeluaran Bulan Depan",
                f"Rp {predicted_value:,.0f}"
            )

            st.write(f"Metode: {method}")
            st.info(message)

            if monthly_df.empty:
                st.warning("Belum ada data bulanan yang dapat ditampilkan.")
            else:
                fig = px.line(
                    monthly_df,
                    x="bulan",
                    y="total_pengeluaran",
                    markers=True,
                    title="Total Pengeluaran Bulanan",
                    labels={
                        "bulan": "Bulan",
                        "total_pengeluaran": "Total Pengeluaran"
                    }
                )

                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(monthly_df, use_container_width=True)

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
    back_to_insight_home(key="back_from_settings")

    st.title("⚙️ Pengaturan AI")
    st.write(
        "Atur provider AI, model, dan API key. "
        "Data ini hanya disimpan sementara selama sesi aplikasi berjalan."
    )

    provider_options = [
        "Gemini",
        "OpenRouter",
        "Groq",
        "Ollama Local"
    ]

    previous_provider = st.session_state.ai_provider

    provider = st.selectbox(
        "Pilih Provider AI",
        provider_options,
        index=provider_options.index(st.session_state.ai_provider),
        key="provider_selectbox"
    )

    # Jika provider berubah, model otomatis diganti ke default provider baru
    if provider != previous_provider:
        st.session_state.ai_provider = provider
        st.session_state.ai_model_name = AI_MODEL_OPTIONS[provider][0]
        st.session_state.ai_api_key = ""
        st.rerun()

    model_options = AI_MODEL_OPTIONS[provider]

    if st.session_state.ai_model_name in model_options:
        model_index = model_options.index(st.session_state.ai_model_name)
    else:
        model_index = 0

    selected_model_option = st.selectbox(
        "Pilih Model AI",
        model_options,
        index=model_index
    )

    if selected_model_option == "Custom Model":
        model_name = st.text_input(
            "Masukkan Nama Model Custom",
            value=st.session_state.ai_model_name
            if st.session_state.ai_model_name != "Custom Model"
            else "",
            placeholder="Contoh: provider/model-name"
        )
    else:
        model_name = selected_model_option

    # =========================
    # INPUT API KEY
    # =========================

    if provider == "Ollama Local":
        api_key = ""
        st.info(
            "Ollama Local tidak membutuhkan API key, "
            "tetapi Ollama harus berjalan di komputer lokal."
        )
    else:
        api_key = st.text_input(
            "API Key",
            value=st.session_state.ai_api_key,
            type="password",
            placeholder="Masukkan API key milik user"
        )

    if st.button("Simpan Pengaturan AI"):
        if provider != "Ollama Local" and api_key.strip() == "":
            st.warning("API key belum diisi.")
            return

        if model_name.strip() == "":
            st.warning("Nama model belum diisi.")
            return

        st.session_state.ai_provider = provider
        st.session_state.ai_model_name = model_name
        st.session_state.ai_api_key = api_key

        st.success("Pengaturan AI berhasil disimpan sementara.")

    st.divider()

    st.subheader("Status Pengaturan Saat Ini")

    st.write(f"Provider aktif: {st.session_state.ai_provider}")
    st.write(f"Model aktif: {st.session_state.ai_model_name}")

    if st.session_state.ai_provider == "Ollama Local":
        st.info("Mode lokal aktif. API key tidak diperlukan.")
    elif st.session_state.ai_api_key.strip() == "":
        st.warning("API key belum diisi.")
    else:
        st.success("API key sudah diisi.")

    st.divider()

    st.subheader("Tes Koneksi AI")

    test_prompt = "Jawab singkat dalam Bahasa Indonesia: koneksi AI berhasil."

    if st.button("Tes AI"):
        try:
            if provider != "Ollama Local" and api_key.strip() == "":
                st.warning("API key belum diisi.")
                return

            if model_name.strip() == "":
                st.warning("Nama model belum diisi.")
                return

            response = generate_ai_response(
                provider=provider,
                api_key=api_key,
                model_name=model_name,
                prompt=test_prompt
            )

            st.success("AI berhasil merespons.")
            st.write(response)

        except Exception as e:
            st.error(f"Gagal menghubungi AI: {e}")

def page_chatbot_ai():
    back_to_insight_home(key="back_from_chatbot")


    st.title("💬 Chatbot AI")
    st.write("Tanyakan kondisi keuangan berdasarkan data transaksi yang sudah tersimpan.")


    try:
        transactions_df = load_transactions()


        transactions_df = transactions_df[
            transactions_df["user_id"] == st.session_state.user_id
        ]

        if transactions_df.empty:
            st.info("Belum ada transaksi. Tambahkan transaksi atau import file terlebih dahulu.")
            return

        prediction_result = predict_next_month_expense(transactions_df)

        financial_summary = build_financial_summary(
            transactions_df,
            prediction_result
        )

        with st.expander("Lihat ringkasan data yang diberikan ke chatbot"):
            st.text(financial_summary)

        for chat in st.session_state.chat_history:
            with st.chat_message(chat["role"]):
                st.write(chat["content"])

        user_question = st.chat_input("Tanyakan sesuatu tentang keuanganmu...")

        if user_question:
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_question
            })

            with st.chat_message("user"):
                st.write(user_question)

            provider = st.session_state.ai_provider
            model_name = st.session_state.ai_model_name
            api_key = st.session_state.ai_api_key

            if provider != "Ollama Local" and api_key.strip() == "":
                answer = "API key belum diisi. Isi dulu di menu Pengaturan AI."
                with st.chat_message("assistant"):
                    st.warning(answer)

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })
                return

            prompt = f"""
Kamu adalah FinBee, chatbot finansial pribadi berbasis data.

Aturan:
- Jawab hanya berdasarkan ringkasan data yang diberikan.
- Jangan mengarang transaksi atau angka baru.
- Jika data tidak cukup, katakan data belum cukup.
- Gunakan Bahasa Indonesia yang jelas dan praktis.
- Jangan memberi saran investasi berisiko tinggi.

Ringkasan data user:
{financial_summary}

Pertanyaan user:
{user_question}
"""

            with st.chat_message("assistant"):
                try:
                    with st.spinner("AI sedang menjawab..."):
                        answer = generate_ai_response(
                            provider=provider,
                            api_key=api_key,
                            model_name=model_name,
                            prompt=prompt
                        )

                    st.write(answer)

                except Exception as e:
                    answer = f"Gagal menghubungi AI: {e}"
                    st.error(answer)

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer
            })

    except Exception as e:
        st.error(f"Gagal menjalankan chatbot AI: {e}")

def page_rekomendasi_ai():
    back_to_insight_home(key="back_from_recommendation")


    st.title("🧠 Rekomendasi AI")
    st.write("AI akan memberi rekomendasi berdasarkan ringkasan transaksi yang sudah tersimpan di database.")
    

    try:
        transactions_df = load_transactions()
    
        transactions_df = transactions_df[
            transactions_df["user_id"] == st.session_state.user_id
        ]

        if transactions_df.empty:
            st.info("Belum ada transaksi. Tambahkan transaksi atau import file terlebih dahulu.")
            return

        prediction_result = predict_next_month_expense(transactions_df)

        financial_summary = build_financial_summary(
            transactions_df,
            prediction_result
        )

        with st.expander("Lihat ringkasan data yang diberikan ke AI"):
            st.text(financial_summary)

        prompt = f"""
Kamu adalah FinBee, asisten finansial pribadi berbasis data.

Tugas:
1. Buat kesimpulan kondisi keuangan user.
2. Jelaskan kategori pengeluaran terbesar.
3. Berikan rekomendasi penghematan yang realistis.
4. Berikan saran prioritas tindakan untuk minggu depan.
5. Jangan mengarang angka di luar ringkasan data.
6. Jika data belum cukup, katakan data belum cukup.

Gunakan Bahasa Indonesia yang jelas dan praktis.

Data keuangan:
{financial_summary}
"""

        if st.button("Buat Rekomendasi AI"):
            provider = st.session_state.ai_provider
            model_name = st.session_state.ai_model_name
            api_key = st.session_state.ai_api_key

            if provider != "Ollama Local" and api_key.strip() == "":
                st.warning("API key belum diisi. Isi dulu di menu Pengaturan AI.")
                return

            with st.spinner("AI sedang membuat rekomendasi..."):
                response = generate_ai_response(
                    provider=provider,
                    api_key=api_key,
                    model_name=model_name,
                    prompt=prompt
                )

            st.subheader("Hasil Rekomendasi AI")
            st.write(response)

    except Exception as e:
        st.error(f"Gagal membuat rekomendasi AI: {e}")

# =========================
# ROUTING UTAMA
# =========================

if not st.session_state.is_logged_in:
    if st.session_state.auth_page == "Login":
        page_login()

    elif st.session_state.auth_page == "Register":
        page_register()

    elif st.session_state.auth_page == "Reset Password":
        page_reset_password()

    st.stop()

# =========================
# SIDEBAR UTAMA
# =========================

st.sidebar.title("🐝 FinBee")
st.sidebar.write(f"Login sebagai: {st.session_state.user_name}")

main_page_options = ["Profil Saya", "Dashboard", "Insight AI"]

main_page = st.sidebar.radio(
    "Menu Utama",
    main_page_options,
    index=main_page_options.index(st.session_state.main_page)
    if st.session_state.main_page in main_page_options
    else 0
)

st.session_state.main_page = main_page

if st.sidebar.button("Logout"):
    st.session_state.is_logged_in = False
    st.session_state.user_id = None
    st.session_state.user_name = None
    st.session_state.login_identifier = None
    st.session_state.login_type = None
    st.session_state.chat_history = []

    st.session_state.auth_page = "Login"
    st.session_state.main_page = "Dashboard"
    st.session_state.dashboard_page = "Home Dashboard"
    st.session_state.insight_page = "Home Insight AI"

    st.rerun()

#ROUTING
if st.session_state.main_page == "Profil Saya":
    page_profil_saya()

elif st.session_state.main_page == "Dashboard":
    if st.session_state.dashboard_page == "Home Dashboard":
        dashboard_home()

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