import pandas as pd


def calculate_ema(df: pd.DataFrame, period: int = 20, column: str = "close"):
    """
    Calculate the Exponential Moving Average (EMA).
    """

    df[f"EMA{period}"] = df[column].ewm(
        span=period,
        adjust=False
    ).mean()

    return df


def analyze_ema(df: pd.DataFrame):
    """
    Analyze the relationship between EMA20 and EMA50.
    """

    ema20 = df["EMA20"].iloc[-1]
    ema50 = df["EMA50"].iloc[-1]

    if ema20 > ema50:
        trend = "Bullish"
    elif ema20 < ema50:
        trend = "Bearish"
    else:
        trend = "Neutral"

    return {
        "EMA20": round(ema20, 5),
        "EMA50": round(ema50, 5),
        "trend": trend
    }