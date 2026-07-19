# brain/decision.py

def decide(results):

    confidence = results.get("confidence", 0)
    trend = results.get("trend")
    structure = results.get("market_structure")
    liquidity = results.get("liquidity_sweep")
    momentum = results.get("momentum")
    execution = results.get("execution_zone")

    # STRONG BUY
    if (
        confidence >= 90
        and trend == "Bullish"
        and structure == "BOS"
        and liquidity
        and momentum == "Strong"
        and execution == "Demand"
    ):
        return "STRONG BUY"

    # BUY
    if (
        confidence >= 80
        and trend == "Bullish"
        and execution == "Demand"
    ):
        return "BUY"

    # STRONG SELL
    if (
        confidence >= 90
        and trend == "Bearish"
        and structure == "BOS"
        and liquidity
        and momentum == "Strong"
        and execution == "Supply"
    ):
        return "STRONG SELL"

    # SELL
    if (
        confidence >= 80
        and trend == "Bearish"
        and execution == "Supply"
    ):
        return "SELL"

    # WATCH
    if confidence >= 70:
        return "WATCH"

    return "IGNORE"