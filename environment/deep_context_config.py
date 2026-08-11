# environment/deep_context_config.py

import MetaTrader5 as mt5


# ============================================================
# DEEP CONTEXT CANDLE ALLOCATION
# ============================================================
#
# HTF  -> approximately 90 days of historical context
# LTF  -> deliberately shorter, more recent context
#
# Do NOT scatter candle counts throughout the engine.
# Change them here when stress testing.
# ============================================================

DEEP_CONTEXT_CANDLES = {

    # -------------------------
    # HIGHER TIMEFRAME
    # -------------------------

    "D1": {
        "timeframe": mt5.TIMEFRAME_D1,
        "candles": 90,
        "purpose": "Macro trend and major structure",
    },

    "H4": {
        "timeframe": mt5.TIMEFRAME_H4,
        "candles": 540,
        "purpose": "Swing structure and major zones",
    },

    # -------------------------
    # INTRADAY
    # -------------------------

    "H1": {
        "timeframe": mt5.TIMEFRAME_H1,
        "candles": 2160,
        "purpose": "Intraday structure and session behavior",
    },

    # -------------------------
    # LOWER TIMEFRAME
    # -------------------------

    "M15": {
        "timeframe": mt5.TIMEFRAME_M15,
        "candles": 3840,
        "purpose": "Recent execution and liquidity context",
    },

    "M5": {
        "timeframe": mt5.TIMEFRAME_M5,
        "candles": 4320,
        "purpose": "Recent LTF structure and execution context",
    },
}


# ============================================================
# SYMBOLS FOR DEEP CONTEXT
# ============================================================

DEEP_CONTEXT_SYMBOLS = [

    "GBPUSD",
    "XAUUSD",
    "EURUSD",
    "USDJPY",
    "DE30",

]


# ============================================================
# CONTEXT HORIZONS
# ============================================================

DEEP_CONTEXT_HORIZONS = {

    "SWING": [
        "D1",
        "H4",
    ],

    "INTRADAY": [
        "H4",
        "H1",
        "M15",
    ],

    "SCALPING": [
        "H1",
        "M15",
        "M5",
    ],

}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_candle_config(timeframe_name):

    config = DEEP_CONTEXT_CANDLES.get(
        timeframe_name
    )

    if config is None:
        raise ValueError(
            f"Unsupported timeframe: {timeframe_name}"
        )

    return config


def get_candle_count(timeframe_name):

    return get_candle_config(
        timeframe_name
    )["candles"]


def get_timeframe(timeframe_name):

    return get_candle_config(
        timeframe_name
    )["timeframe"]


def get_horizon_timeframes(horizon):

    timeframes = DEEP_CONTEXT_HORIZONS.get(
        horizon.upper()
    )

    if timeframes is None:
        raise ValueError(
            f"Unsupported horizon: {horizon}"
        )

    return timeframes


def get_symbols():

    return DEEP_CONTEXT_SYMBOLS.copy()