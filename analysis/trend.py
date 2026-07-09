import pandas as pd


def analyze_trend(df: pd.DataFrame):
    """
    Analyze overall market trend using EMA20 and EMA50.
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
        "Trend": trend,
        "EMA20": round(ema20, 5),
        "EMA50": round(ema50, 5)
    }