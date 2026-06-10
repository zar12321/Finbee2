from pathlib import Path


# ==========================================================
# APPLICATION
# ==========================================================

APP_NAME = "FinBee"

APP_ICON = "🐝"

APP_VERSION = "1.0.0"

APP_LAYOUT = "wide"

APP_SIDEBAR_STATE = "collapsed"


# ==========================================================
# DIRECTORY
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_DIR = BASE_DIR / "config"

PAGES_DIR = BASE_DIR / "pages"

COMPONENTS_DIR = BASE_DIR / "components"

STYLES_DIR = BASE_DIR / "styles"

MODULES_DIR = BASE_DIR / "modules"

STATE_DIR = BASE_DIR / "state"

UTILS_DIR = BASE_DIR / "utils"

DATABASE_DIR = BASE_DIR / "database"

ASSETS_DIR = BASE_DIR / "assets"


# ==========================================================
# FILE IMPORT
# ==========================================================

SUPPORTED_FILE_TYPES = [
    "csv",
    "xlsx"
]

SUPPORTED_EXCEL_TYPES = [
    ".xlsx",
    ".xls"
]

SUPPORTED_CSV_TYPES = [
    ".csv"
]

MAX_UPLOAD_SIZE_MB = 20

MAX_IMPORTED_ROWS = 100000


# ==========================================================
# TRANSACTION
# ==========================================================

TRANSACTION_TYPES = [
    "expense",
    "income"
]

DEFAULT_TRANSACTION_TYPE = "expense"

DEFAULT_PAYMENT_METHOD = "Cash"

DEFAULT_CATEGORY = "Other"

TOP_TRANSACTION_LIMIT = 5


# ==========================================================
# PAYMENT METHODS
# ==========================================================

DEFAULT_PAYMENT_METHODS = [
    "Cash",
    "Debit Card",
    "Credit Card",
    "Bank Transfer",
    "QRIS",
    "E-Wallet",
    "Other"
]


# ==========================================================
# CATEGORY
# ==========================================================

STANDARD_CATEGORIES = [
    "Food",
    "Transport",
    "Bills",
    "Shopping",
    "Education",
    "Health",
    "Entertainment",
    "Salary",
    "Allowance",
    "Other"
]


# ==========================================================
# DASHBOARD
# ==========================================================

DEFAULT_CHART_HEIGHT = 450

DEFAULT_TABLE_HEIGHT = 400

DEFAULT_MONTH_FILTER = "All"

DEFAULT_YEAR_FILTER = "All"

MAX_DASHBOARD_RECORDS = 5000


# ==========================================================
# ANALYTICS
# ==========================================================

TOP_CATEGORY_LIMIT = 10

TOP_PAYMENT_METHOD_LIMIT = 10

MONTHLY_TREND_WINDOW = 12


# ==========================================================
# PREDICTION
# ==========================================================

MIN_MONTHS_FOR_REGRESSION = 3

DEFAULT_PREDICTION_METHOD = "Linear Regression"

PREDICTION_ROUND_DIGITS = 2


# ==========================================================
# AI
# ==========================================================

SUPPORTED_AI_PROVIDERS = [
    "Gemini",
    "OpenRouter",
    "Groq",
    "Ollama Local"
]

DEFAULT_AI_PROVIDER = "Gemini"

DEFAULT_AI_MODEL = ""

DEFAULT_TEMPERATURE = 0.3

MAX_CHAT_HISTORY = 20

AI_TIMEOUT_SECONDS = 120


# ==========================================================
# AUTH
# ==========================================================

MIN_PASSWORD_LENGTH = 8

MAX_PASSWORD_LENGTH = 128

MAX_NAME_LENGTH = 100

MAX_LOGIN_IDENTIFIER_LENGTH = 100

PASSWORD_HASH_ALGORITHM = "bcrypt"


# ==========================================================
# PROFILE
# ==========================================================

DEFAULT_AGE = 18

DEFAULT_JOB = "Belum Diisi"


# ==========================================================
# SESSION
# ==========================================================

SESSION_CHAT_KEY = "chat_history"

SESSION_USER_KEY = "user_id"

SESSION_LOGIN_KEY = "logged_in"

SESSION_PAGE_KEY = "current_page"


# ==========================================================
# FINANCIAL STATUS
# ==========================================================

STATUS_AMAN = "Aman"

STATUS_WASPADA = "Waspada"

STATUS_MELEBIHI_SEDIKIT = "Melebihi Sedikit"

STATUS_MELEBIHI_TARGET = "Melebihi Target"


# ==========================================================
# FINANCIAL THRESHOLD
# ==========================================================

SAFE_THRESHOLD = 0.80

WARNING_THRESHOLD = 1.00

OVER_LIMIT_THRESHOLD = 1.10


# ==========================================================
# COLORS
# ==========================================================

PRIMARY_COLOR = "#7CFF5B"

SECONDARY_COLOR = "#A3B5AA"

SUCCESS_COLOR = "#2ECC71"

WARNING_COLOR = "#F1C40F"

DANGER_COLOR = "#E74C3C"

INFO_COLOR = "#3498DB"

BACKGROUND_COLOR = "#08130D"

CARD_BACKGROUND_COLOR = "#102018"

TEXT_COLOR = "#FFFFFF"

TEXT_MUTED_COLOR = "#A3B5AA"

BORDER_COLOR = "rgba(255,255,255,0.08)"


# ==========================================================
# DATE FORMAT
# ==========================================================

DATE_FORMAT = "%d-%m-%Y"

DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"

MONTH_FORMAT = "%B %Y"


# ==========================================================
# CURRENCY
# ==========================================================

CURRENCY_SYMBOL = "Rp"

DECIMAL_DIGITS = 0

THOUSAND_SEPARATOR = ","