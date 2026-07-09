def generate_signal(
    trend,
    market_bias,
    confidence,
):

    score = int(confidence["Confidence"].replace("%", ""))

    if (
        trend["Trend"] == "Bullish"
        and market_bias["Bias"] == "Buy"
        and score >= 80
    ):
        signal = "BUY"

    elif (
        trend["Trend"] == "Bearish"
        and market_bias["Bias"] == "Sell"
        and score >= 80
    ):
        signal = "SELL"

    else:
        signal = "WAIT"

    return {
        "Signal": signal
    }