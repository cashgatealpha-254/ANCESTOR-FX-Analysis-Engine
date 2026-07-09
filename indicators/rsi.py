import pandas as pd


def calculate_rsi(df: pd.DataFrame, period: int = 14, column: str = "close"):
    """
    Calculate the Relative Strength Index (RSI).
    """

    delta = df[column].diff()

    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    df[f"RSI{period}"] = rsi

    return df


def analyze_rsi(df: pd.DataFrame, period: int = 14):
    """
    Analyze the latest RSI observation.
    """

    column = f"RSI{period}"

    latest = df[column].iloc[-1]
    previous = df[column].iloc[-2]

    # Direction
    if latest > previous:
        direction = "Rising"
    elif latest < previous:
        direction = "Falling"
    else:
        direction = "Flat"

    # Territory
    if latest >= 50:
        territory = "Above 50"
    else:
        territory = "Below 50"

    return {
        "RSI": round(latest, 2),
        "Direction": direction,
        "Territory": territory
    }