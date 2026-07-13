def analyze_bos(df, swings):

    swing_highs = swings["swing_highs"]
    swing_lows = swings["swing_lows"]

    if len(swing_highs) == 0 or len(swing_lows) == 0:
        return {"BOS": "No BOS"}

    current_price = df["close"].iloc[-1]

    last_swing_high = swing_highs[-1]["price"]
    last_swing_low = swing_lows[-1]["price"]

    if current_price > last_swing_high:
        bos = "Bullish BOS"

    elif current_price < last_swing_low:
        bos = "Bearish BOS"

    else:
        bos = "No BOS"

    return {
        "BOS": bos,
        "Last Swing High": last_swing_high,
        "Last Swing Low": last_swing_low
    }