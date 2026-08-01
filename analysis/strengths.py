def analyze_strengths(results):

    strengths = []

    if results["trend"]["Trend"] == "Bullish":
        strengths.append("Trend is bullish.")

    elif results["trend"]["Trend"] == "Bearish":
        strengths.append("Trend is bearish.")

    if results["confluence"]["Strength"] == "High":
        strengths.append("Strong confluence.")

    if results["structure_strength"]["Structure Strength"] == "Strong":
        strengths.append("Strong market structure.")

    if results["market_bias"]["Market Bias"] != "WAIT":
        strengths.append("Clear market bias.")

    if results["bos"]["BOS"] != "No BOS":
        strengths.append("Break of Structure confirmed.")

    if results["choch"]["CHoCH"] != "No CHoCH":
        strengths.append("Change of Character confirmed.")

    if results["liquidity"]["Liquidity"] != "No Sweep":
        strengths.append("Liquidity sweep detected.")

    if len(strengths) == 0:
        strengths.append("No strong confirmations.")

    return {
        "Strengths": strengths
    }