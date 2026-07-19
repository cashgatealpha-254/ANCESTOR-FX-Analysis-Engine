# brain/confidence.py

def calculate(results):

    score = 0

    breakdown = {}

    # Trend
    trend = results.get("trend")

    if trend in ["Bullish", "Bearish"]:
        score += 20
        breakdown["Trend"] = 20
    else:
        breakdown["Trend"] = 0

    # Market Structure
    structure = results.get("market_structure")

    if structure == "BOS":
        score += 20
        breakdown["Structure"] = 20
    else:
        breakdown["Structure"] = 0

    # Supply & Demand
    if results.get("zones"):
        score += 20
        breakdown["Zones"] = 20
    else:
        breakdown["Zones"] = 0

    # Liquidity
    if results.get("liquidity_sweep"):
        score += 20
        breakdown["Liquidity"] = 20
    else:
        breakdown["Liquidity"] = 0

    # Momentum
    if results.get("momentum") == "Strong":
        score += 20
        breakdown["Momentum"] = 20
    else:
        breakdown["Momentum"] = 0

    return {
        "score": score,
        "breakdown": breakdown
    }