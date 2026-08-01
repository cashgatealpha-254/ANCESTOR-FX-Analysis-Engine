def analyze_improvements(results):

    improvements = []

    # Confidence
    if results["confidence"] < 70:
        improvements.append(
            "Increase confidence before execution."
        )

    # Confluence
    if results["confluence"]["Strength"] != "High":
        improvements.append(
            "Wait for stronger confluence."
        )

    # Risk
    if not results.get("trade_allowed", True):
        improvements.append(
            "Risk conditions are not satisfied."
        )

    # Market Bias
    if results["market_bias"]["Market Bias"] == "WAIT":
        improvements.append(
            "Market bias is neutral. Wait."
        )

    # BOS
    if results["bos"]["BOS"] == "No BOS":
        improvements.append(
            "Wait for a Break Of Structure."
        )

    # CHoCH
    if results["choch"]["CHoCH"] == "No CHoCH":
        improvements.append(
            "No Change Of Character detected."
        )

    # Liquidity
    if results["liquidity"]["Liquidity"] == "No Sweep":
        improvements.append(
            "Wait for liquidity sweep."
        )

    # Execution
    if results["decision"] == "IGNORE":
        improvements.append(
            "No executable setup."
        )

    if len(improvements) == 0:
        improvements.append(
            "Everything aligns. Monitor execution."
        )

    return {
        "Improvements": improvements
    }