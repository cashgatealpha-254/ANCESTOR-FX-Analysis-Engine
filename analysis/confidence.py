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

    if trend["Trend"] in ["Bullish", "Bearish"]:
        score += 20

    if rsi["Direction"] != "Neutral":
        score += 20

    if atr["Volatility"] == "Increasing":
        score += 20

    if market_state["Market State"] != "Ranging":
        score += 20

    if market_structure["Structure"] != "Sideways":
        score += 20

    if structure_strength["Structure Strength"] == "Strong Bullish Structure":
        score += 20

    if structure_strength["Structure Strength"] == "Strong Bearish Structure":
        score += 20

    if market_bias["Market Bias"] in ["BUY", "SELL"]:
        score += 20

    if bos["BOS"] != "No BOS":
        score += 20

    if choch["CHoCH"] != "No CHoCH":
        score += 20

    if liquidity["Liquidity"] != "No Sweep":
        score += 20

    if supply_demand["Current Zone"] != "Neutral":
        score += 20

    return score