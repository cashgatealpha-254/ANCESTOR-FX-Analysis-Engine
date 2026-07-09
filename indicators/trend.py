import pandas as pd

def calculate_ema(df: pd.DataFrame):
    """
    Calculate EMA20 and EMA50.
    """

    df["EMA20"] = df["close"].ewm(span=20, adjust=False).mean()
    df["EMA50"] = df["close"].ewm(span=50, adjust=False).mean()

    return df