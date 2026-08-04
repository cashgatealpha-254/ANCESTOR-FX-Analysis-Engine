import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    # ==========================
    # MT5 SETTINGS
    # ==========================

    MT5_LOGIN = int(os.getenv("MT5_LOGIN", 0))
    MT5_PASSWORD = os.getenv("MT5_PASSWORD", "")
    MT5_SERVER = os.getenv("MT5_SERVER", "")

    # ==========================
    # DEFAULT MARKET SETTINGS
    # ==========================

    SYMBOL = "GBPUSD"
    TIMEFRAME = "M15"
    CANDLES = 500

    # ==========================
    # RISK SETTINGS
    # ==========================

    RISK_PERCENT = 2.0
    MAX_OPEN_TRADES = 4

    # ==========================
    # EMA SETTINGS
    # ==========================

    FAST_EMA = 20
    SLOW_EMA = 50

    # ==========================
    # ATR SETTINGS
    # ==========================

    ATR_PERIOD = 14

    # ==========================
    # CONFIDENCE
    # ==========================

    MIN_CONFIDENCE = 70

    # ==========================
    # MEMORY
    # ==========================

    MEMORY_FILE = "memory/trade_memory.json"

    # ==========================
    # LOGGING
    # ==========================

    LOG_FILE = "logs/ancestor.log"

    # ==========================
    # DASHBOARD
    # ==========================

    DASHBOARD_REFRESH = 5

    # seconds

    # ==========================
    # NOTIFICATIONS
    # ==========================

    EMAIL_NOTIFICATIONS = True
    WHATSAPP_NOTIFICATIONS = False

    # ==========================
    # VERSION
    # ==========================

    VERSION = "1.0.0"

    APP_NAME = "Ancestor FX"