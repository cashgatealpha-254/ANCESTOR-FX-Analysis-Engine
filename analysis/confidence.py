def calculate_confidence(
    trend,
    rsi,
    atr,
    market_state,
    market_bias,
    market_structure,
    bos,
    choch,
    liquidity,
    supply_demand,
    structure_memory,
    protected_levels,
    structure_strength
):

    score = 0
    max_score = 12

    if trend["Trend"] in ["Bullish", "Bearish"]:
        score += 1

    if rsi["Direction"] != "Neutral":
        score += 1

    if atr["Volatility"] == "Increasing":
        score += 1

    if market_state["Market State"] != "Ranging":
        score += 1

    if market_structure["Structure"] != "Sideways":
        score += 1

    if structure_strength["Structure Strength"] == "Strong Bullish Structure":
        score += 1

    if structure_strength["Structure Strength"] == "Strong Bearish Structure":
        score += 1

    if market_bias["Market Bias"] in ["BUY", "SELL"]:
        score += 1

    if bos["BOS"] != "No BOS":
        score += 1

    if choch["CHoCH"] != "No CHoCH":
        score += 1

    if liquidity["Liquidity"] != "No Sweep":
        score += 1

    if supply_demand["Current Zone"] != "Neutral":
        score += 1

    calculate_confidence = round((score/max_score) * 100)

    return calculate_confidence