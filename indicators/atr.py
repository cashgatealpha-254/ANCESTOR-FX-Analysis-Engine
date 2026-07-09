import pandas as pd


def calculate_atr(df: pd.DataFrame, period: int = 14):

    high_low = df["high"] - df["low"]

    high_close = (df["high"] - df["close"].shift()).abs()

    low_close = (df["low"] - df["close"].shift()).abs()

    true_range = pd.concat(
        [high_low, high_close, low_close],
        axis=1
    ).max(axis=1)

    df[f"ATR{period}"] = true_range.rolling(period).mean()

    return df


def analyze_atr(df: pd.DataFrame, period: int = 14):

    column = f"ATR{period}"

    latest = df[column].iloc[-1]
    previous = df[column].iloc[-2]

    if latest > previous:
        volatility = "Increasing"
    elif latest < previous:
        volatility = "Decreasing"
    else:
        volatility = "Stable"

    return {
        "ATR": round(latest, 5),
        "Volatility": volatility
    }