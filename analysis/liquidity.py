def analyze_liquidity(df, swings):

    swing_highs = swings["swing_highs"]
    swing_lows = swings["swing_lows"]

    if len(swing_highs) < 1 or len(swing_lows) < 1:
        return {
            "Liquidity": "No Sweep"
        }

    current_price = df["close"].iloc[-1]

    last_high = swing_highs[-1]["price"]
    last_low = swing_lows[-1]["price"]

    if current_price > last_high:
        liquidity = "Buy-side Liquidity Swept"

    elif current_price < last_low:
        liquidity = "Sell-side Liquidity Swept"

    else:
        liquidity = "No Sweep"

    return {
        "Liquidity": liquidity,
        "Buy-side": last_high,
        "Sell-side": last_low
    }