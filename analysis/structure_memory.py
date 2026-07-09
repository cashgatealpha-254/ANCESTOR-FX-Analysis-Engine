def build_structure_memory(swings):

    highs = swings["Swing Highs"]
    lows = swings["Swing Lows"]

    latest_high = highs[-1] if highs else None
    previous_high = highs[-2] if len(highs) >= 2 else None

    latest_low = lows[-1] if lows else None
    previous_low = lows[-2] if len(lows) >= 2 else None

    return {
        "Latest High": latest_high,
        "Previous High": previous_high,
        "Latest Low": latest_low,
        "Previous Low": previous_low
    }