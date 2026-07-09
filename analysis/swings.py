def detect_swings(df):

    swing_highs = []
    swing_lows = []

    for i in range(2, len(df) - 2):

        high = df["high"].iloc[i]

        if (
            high > df["high"].iloc[i - 1]
            and high > df["high"].iloc[i - 2]
            and high > df["high"].iloc[i + 1]
            and high > df["high"].iloc[i + 2]
        ):
            swing_highs.append(
                {
                    "index": i,
                    "price": high
                }
            )

        low = df["low"].iloc[i]

        if (
            low < df["low"].iloc[i - 1]
            and low < df["low"].iloc[i - 2]
            and low < df["low"].iloc[i + 1]
            and low < df["low"].iloc[i + 2]
        ):
            swing_lows.append(
                {
                    "index": i,
                    "price": low
                }
            )

    return {
        "Swing Highs": swing_highs,
        "Swing Lows": swing_lows
    }