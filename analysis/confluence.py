def analyze_confluence(results):

    score = 0
    reasons = []

    # Trend
    if results["trend"]["Trend"] != "Neutral":
        score += 20
        reasons.append("Trend aligned")

    # BOS
    if results["bos"]["BOS"] != "None":
        score += 15
        reasons.append("Break of Structure confirmed")

    # CHoCH
    if results["choch"]["CHoCH"] != "None":
        score += 10
        reasons.append("CHoCH confirmed")

    # Liquidity
    if results["liquidity"]["Liquidity"] != "None":
        score += 10
        reasons.append("Liquidity event detected")

    # Supply / Demand
    zone = results["supply_demand"]["Current Zone"]

    if zone != "None":
        score += 15
        reasons.append(f"{zone} detected")

    # Market Structure
    if results["market_structure"]["Structure"] != "Neutral":
        score += 15
        reasons.append("Market structure aligned")

    # Structure Memory
    if results["structure_memory"]:
        score += 10
        reasons.append("Structure memory available")

    # Protected Levels
    if results["protected_levels"]:
        score += 5
        reasons.append("Protected levels identified")

    return {
        "Score": score,
        "Reasons": reasons
    }