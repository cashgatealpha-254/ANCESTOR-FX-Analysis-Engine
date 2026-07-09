def analyze_confluence(results):

    score = 0

    if results["trend"]["Trend"] in ["Bullish", "Bearish"]:
        score += 1

    if results["bos"]["BOS"] != "No BOS":
        score += 1

    if results["choch"]["CHoCH"] != "No CHoCH":
        score += 1

    if results["liquidity"]["Liquidity"] != "No Sweep":
        score += 1

    if results["supply_demand"]["Current Zone"] != "Neutral":
        score += 1

    if score >= 5:
        confluence = "Excellent"

    elif score >= 4:
        confluence = "Strong"

    elif score >= 3:
        confluence = "Moderate"

    else:
        confluence = "Weak"

    return {
        "Confluence": confluence,
        "Score": score
    }