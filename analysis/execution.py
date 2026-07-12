def analyze_execution(
    symbol,
    trend,
    supply_demand,
    protected_levels,
    atr,
    current_price
):

    execution = {}

    atr_value = atr["ATR"]

    if trend["Trend"] == "Bullish":

        execution["direction"] = "BUY"
        execution["entry"] = round(current_price, 5)
        execution["sl"] = round(current_price - (2 * atr_value), 5)
        execution["tp"] = round(current_price + (4 * atr_value), 5)

    elif trend["Trend"] == "Bearish":

        execution["direction"] = "SELL"
        execution["entry"] = round(current_price, 5)
        execution["sl"] = round(current_price + (2 * atr_value), 5)
        execution["tp"] = round(current_price - (4 * atr_value), 5)

    else:

        execution["direction"] = "WAIT"
        execution["entry"] = None
        execution["sl"] = None
        execution["tp"] = None

    return execution