import re

from config.settings import (
    MIN_PASSWORD_LENGTH,
    MAX_PASSWORD_LENGTH,
    MAX_NAME_LENGTH,
    MAX_LOGIN_IDENTIFIER_LENGTH
)


def validate_name(name):

    if not name:
        return False, "Nama wajib diisi."

    name = str(name).strip()

    if len(name) == 0:
        return False, "Nama wajib diisi."

    if len(name) > MAX_NAME_LENGTH:
        return (
            False,
            f"Nama maksimal {MAX_NAME_LENGTH} karakter."
        )

    return True, ""


def validate_email(email):

    if not email:
        return False, "Email wajib diisi."

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.match(pattern, email):
        return False, "Format email tidak valid."

    return True, ""


def validate_username(username):

    if not username:
        return False, "Username wajib diisi."

    username = username.strip()

    if len(username) > MAX_LOGIN_IDENTIFIER_LENGTH:
        return (
            False,
            f"Username maksimal {MAX_LOGIN_IDENTIFIER_LENGTH} karakter."
        )

    if len(username) < 3:
        return False, "Username minimal 3 karakter."

    return True, ""


def validate_password(password):

    if not password:
        return False, "Password wajib diisi."

    if len(password) < MIN_PASSWORD_LENGTH:
        return (
            False,
            f"Password minimal {MIN_PASSWORD_LENGTH} karakter."
        )

    if len(password) > MAX_PASSWORD_LENGTH:
        return (
            False,
            f"Password maksimal {MAX_PASSWORD_LENGTH} karakter."
        )

    return True, ""


def validate_confirm_password(
    password,
    confirm_password
):

    if password != confirm_password:
        return (
            False,
            "Konfirmasi password tidak cocok."
        )

    return True, ""


def validate_age(age):

    try:
        age = int(age)
    except Exception:
        return False, "Umur harus berupa angka."

    if age < 0:
        return False, "Umur tidak valid."

    if age > 120:
        return False, "Umur tidak valid."

    return True, ""


def validate_amount(amount):

    try:
        amount = float(amount)
    except Exception:
        return False, "Nominal harus berupa angka."

    if amount <= 0:
        return False, "Nominal harus lebih besar dari 0."

    return True, ""


def validate_transaction_form(
    category_id,
    tanggal_transaksi,
    payment_method,
    amount
):

    if category_id is None:
        return False, "Kategori wajib dipilih."

    if tanggal_transaksi is None:
        return False, "Tanggal transaksi wajib diisi."

    if payment_method is None:
        return False, "Metode pembayaran wajib diisi."

    valid_amount, message = validate_amount(amount)

    if not valid_amount:
        return False, message

    return True, ""


def validate_login_identifier(
    login_identifier,
    login_type
):

    if login_type == "Email":
        return validate_email(login_identifier)

    return validate_username(login_identifier)