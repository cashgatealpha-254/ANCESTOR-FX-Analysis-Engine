def analyze_liquidity(df):

    last_high = df["high"].iloc[-1]
    previous_high = df["high"].iloc[-2]

    last_low = df["low"].iloc[-1]
    previous_low = df["low"].iloc[-2]

    if last_high > previous_high:
        liquidity = "Buy-side Liquidity Swept"

    elif last_low < previous_low:
        liquidity = "Sell-side Liquidity Swept"

    else:
        liquidity = "No Sweep"

    return {
        "Liquidity": liquidity
    }