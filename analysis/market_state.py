def analyze_market_state(trend, rsi, atr):
    """
    Combine trend, momentum and volatility into a market state.
    """

    if (
        trend["Trend"] == "Bullish"
        and rsi["Direction"] == "Rising"
        and atr["Volatility"] == "Increasing"
    ):
        state = "Bullish Momentum"

    elif (
        trend["Trend"] == "Bearish"
        and rsi["Direction"] == "Falling"
        and atr["Volatility"] == "Increasing"
    ):
        state = "Bearish Momentum"

    else:
        state = "Transition"

    return {
        "Market State": state
    }