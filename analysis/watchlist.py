def analyze_watchlist(results):

    watch = []

    # Trend continuation
    if results["trend"]["Trend"] == "Bullish":
        watch.append("Watch for bullish continuation.")

    elif results["trend"]["Trend"] == "Bearish":
        watch.append("Watch for bearish continuation.")

    # Liquidity
    if results["liquidity"]["Liquidity"] == "No Sweep":
        watch.append("Watch for liquidity sweep.")

    # BOS
    if results["bos"]["BOS"] == "No BOS":
        watch.append("Watch for Break of Structure.")

    # CHoCH
    if results["choch"]["CHoCH"] == "No CHoCH":
        watch.append("Watch for Change of Character.")

    # Supply & Demand
    zone = results["supply_demand"]["Current Zone"]

    if zone == "Demand":
        watch.append("Watch for bullish reaction in demand.")

    elif zone == "Supply":
        watch.append("Watch for bearish reaction in supply.")

    # Risk
    if not results.get("trade_allowed", True):
        watch.append("No trade until risk conditions improve.")

    return {
        "Watchlist": watch
    }