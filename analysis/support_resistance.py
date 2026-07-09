import pandas as pd


def analyze_support_resistance(df: pd.DataFrame, lookback: int = 20):

    support = df["low"].tail(lookback).min()
    resistance = df["high"].tail(lookback).max()

    current_price = df["close"].iloc[-1]

    if current_price <= support:
        location = "At Support"

    elif current_price >= resistance:
        location = "At Resistance"

    else:
        location = "Between Levels"

    return {
        "Support": round(support, 5),
        "Resistance": round(resistance, 5),
        "Current Price": round(current_price, 5),
        "Location": location
    }