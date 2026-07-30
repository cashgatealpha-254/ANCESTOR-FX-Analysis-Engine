def analyze_execution_quality(results):

    score = 0
    reasons = []

    # -------------------------
    # Trend Alignment
    # -------------------------
    if results["trend"]["Trend"] == results["market_bias"]["Market Bias"]:
        score += 1
        reasons.append("Trend aligned.")

    # -------------------------
    # Confluence
    # -------------------------
    if results["confluence"]["Strength"] == "High":
        score += 1
        reasons.append("High confluence.")

    # -------------------------
    # Structure
    # -------------------------
    if results["structure_strength"]["Structure Strength"] == "Strong":
        score += 1
        reasons.append("Strong market structure.")

    # -------------------------
    # Validation
    # -------------------------
    if results["validation"]["Valid"]:
        score += 1
        reasons.append("Analysis validated.")

    # -------------------------
    # Risk
    # -------------------------
    if results.get("trade_allowed", False):
        score += 1
        reasons.append("Risk acceptable.")

    # -------------------------
    # Rating
    # -------------------------
    if score == 5:
        quality = "Excellent"

    elif score >= 4:
        quality = "Good"

    elif score >= 3:
        quality = "Average"

    else:
        quality = "Poor"

    return {

        "Score": score,
        "Max Score": 5,
        "Quality": quality,
        "Reasons": reasons

    }