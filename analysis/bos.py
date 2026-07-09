def analyze_bos(df):

    recent_high = df["high"].iloc[-2]
    previous_high = df["high"].iloc[-3]

    recent_low = df["low"].iloc[-2]
    previous_low = df["low"].iloc[-3]

    if recent_high > previous_high:
        bos = "Bullish BOS"

    elif recent_low < previous_low:
        bos = "Bearish BOS"

    else:
        bos = "No BOS"

    return {
        "BOS": bos
    }