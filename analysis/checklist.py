def build_checklist(results):

    return {
        "Trend": results["trend"],
        "Market Bias": results["market_bias"]["Market Bias"],
        "BOS": results["bos"]["BOS"],
        "CHoCH": results["choch"]["CHoCH"],
        "Liquidity": results["liquidity"]["Liquidity"],
        "Risk Allowed": results.get("trade_allowed", False),
        "Confidence": results["confidence"],
        "Decision": results["decision"]
    }