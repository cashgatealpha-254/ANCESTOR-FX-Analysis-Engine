def analyze_confluence(results):

    bullish = 0
    bearish = 0

    # Trend
    if results["trend"]["Trend"] == "Bullish":
        bullish += 1
    elif results["trend"]["Trend"] == "Bearish":
        bearish += 1

    # BOS
    if results["bos"]["BOS"] == "Bullish BOS":
        bullish += 1
    elif results["bos"]["BOS"] == "Bearish BOS":
        bearish += 1

    # CHoCH
    if results["choch"]["CHoCH"] == "Bullish CHoCH":
        bullish += 1
    elif results["choch"]["CHoCH"] == "Bearish CHoCH":
        bearish += 1

    # Supply / Demand
    if results["supply_demand"]["Current Zone"] == "Demand":
        bullish += 1
    elif results["supply_demand"]["Current Zone"] == "Supply":
        bearish += 1

    # Liquidity
    if results["liquidity"]["Liquidity"] == "Sell-side Liquidity Swept":
        bullish += 1
    elif results["liquidity"]["Liquidity"] == "Buy-side Liquidity Swept":
        bearish += 1

    # Decide dominant side
    if bullish > bearish:
        direction = "Bullish"
        confirmations = bullish
    elif bearish > bullish:
        direction = "Bearish"
        confirmations = bearish
    else:
        direction = "Neutral"
        confirmations = bullish

    # Grade confluence
    if confirmations >= 4:
        confluence = "High"
    elif confirmations >= 2:
        confluence = "Medium"
    else:
        confluence = "Low"