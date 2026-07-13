def build_structure_memory(swings):

    highs = swings["swing_highs"]
    lows = swings["swing_lows"]

    latest_high = highs[-1] if highs else None
    previous_high = highs[-2] if len(highs) >= 2 else None

    latest_low = lows[-1] if lows else None
    previous_low = lows[-2] if len(lows) >= 2 else None

    trend = "Sideways"

    if latest_high and previous_high and latest_low and previous_low:

        if (
            latest_high["price"] > previous_high["price"]
            and latest_low["price"] > previous_low["price"]
        ):
            trend = "Bullish"

        elif (
            latest_high["price"] < previous_high["price"]
            and latest_low["price"] < previous_low["price"]
        ):
            trend = "Bearish"

    return {
        "Latest High": latest_high,
        "Previous High": previous_high,
        "Latest Low": latest_low,
        "Previous Low": previous_low,
        "Trend": trend
    }