def analyze_market_bias(trend, rsi, atr, market_state):
    """
    Determine the overall market bias.
    """

    if market_state["Market State"] == "Bullish Momentum":
        bias = "BUY"

    elif market_state["Market State"] == "Bearish Momentum":
        bias = "SELL"

    else:
        bias = "WAIT"

    return {
        "Market Bias": bias,
        "Reason": market_state["Market State"]
    }