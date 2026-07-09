import pandas as pd


def analyze_market_structure(df: pd.DataFrame):

    high1 = df["high"].iloc[-1]
    high2 = df["high"].iloc[-2]

    low1 = df["low"].iloc[-1]
    low2 = df["low"].iloc[-2]

    if high1 > high2 and low1 > low2:
        structure = "Higher High / Higher Low"

    elif high1 < high2 and low1 < low2:
        structure = "Lower High / Lower Low"

    elif high1 > high2:
        structure = "Higher High"

    elif low1 < low2:
        structure = "Lower Low"

    else:
        structure = "Sideways"

    return {
        "Structure": structure
    }