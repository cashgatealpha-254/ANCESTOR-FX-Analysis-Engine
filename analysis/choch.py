def analyze_choch(df):

    last_close = df["close"].iloc[-1]
    previous_close = df["close"].iloc[-2]

    last_open = df["open"].iloc[-1]
    previous_open = df["open"].iloc[-2]

    if previous_close < previous_open and last_close > last_open:
        choch = "Bullish CHoCH"

    elif previous_close > previous_open and last_close < last_open:
        choch = "Bearish CHoCH"

    else:
        choch = "No CHoCH"

    return {
        "CHoCH": choch
    }