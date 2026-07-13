def analyze_choch(df, protected_levels):

    current_price = df["close"].iloc[-1]

    protected_high = protected_levels["Protected High"]
    protected_low = protected_levels["Protected Low"]

    choch = "No CHoCH"

    if protected_high is not None:

        if current_price > protected_high["price"]:
            choch = "Bullish CHoCH"

    elif protected_low is not None:

        if current_price < protected_low["price"]:
            choch = "Bearish CHoCH"

    return {
        "CHoCH": choch
    }