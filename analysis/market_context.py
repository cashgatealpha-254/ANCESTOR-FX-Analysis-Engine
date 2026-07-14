def analyze_market_context(
    multi_timeframe,
    market_bias,
    market_structure,
    supply_demand
):

    context = {}

    # Bullish continuation
    if (
        multi_timeframe["alignment"] == "Aligned"
        and market_bias == "BUY"
        and market_structure != "Sideways"
        and supply_demand == "Demand"
    ):
        context["Context"] = "Bullish Continuation"

    # Bearish continuation
    elif (
        multi_timeframe["alignment"] == "Aligned"
        and market_bias == "SELL"
        and market_structure != "Sideways"
        and supply_demand == "Supply"
    ):
        context["Context"] = "Bearish Continuation"

    # Higher timeframes disagree
    elif (
        multi_timeframe["alignment"] == "Mixed"
    ):
        context["Context"] = "Wait"

    # Everything else
    else:
        context["Context"] = "Reversal Watch"

    context["HTF Alignment"] = multi_timeframe["alignment"]

    return context