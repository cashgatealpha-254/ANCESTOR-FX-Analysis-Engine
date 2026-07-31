def calculate_trade_score(results):

    score = 0

    score += min(results["confidence"], 40)

    if results["confluence"]["Strength"] == "High":
        score += 20

    if results["execution_quality"]["Quality"] == "Excellent":
        score += 20

    if results["trade_allowed"]:
        score += 20

    return {
        "Trade Score": score
    }