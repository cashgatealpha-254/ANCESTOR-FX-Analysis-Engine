# brain/advisor.py

def explain(results):

    reasons = []

    if results.get("trend") == "Bullish":
        reasons.append("HTF trend is Bullish.")

    if results.get("market_structure") == "BOS":
        reasons.append("Bullish BOS confirmed.")

    if results.get("liquidity_sweep"):
        reasons.append("Liquidity sweep detected.")

    if results.get("execution_zone") == "Demand":
        reasons.append("Price is inside Demand Zone.")

    if results.get("momentum") == "Strong":
        reasons.append("Momentum supports continuation.")

    if not reasons:
        return "No strong confluence detected."

    return " ".join(reasons)