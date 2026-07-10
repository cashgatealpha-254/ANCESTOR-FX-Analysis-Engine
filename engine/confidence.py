def calculate_confidence(data):
    score = 0

    # Trend
    if data["trend"] == "Bullish":
        score += 25
    elif data["trend"] == "Bearish":
        score += 25

    # BOS
    if data["bos"] != "No BOS":
        score += 20

    # CHOCH
    if data["choch"] != "No CHOCH":
        score += 15

    # Liquidity
    if data["liquidity"] != "No Sweep":
        score += 15

    # Supply / Demand
    if data["supply_demand"] != "Neutral":
        score += 15

    # ATR
    if data["atr"] == "Healthy":
        score += 10

    return min(score, 100)