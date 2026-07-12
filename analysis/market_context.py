def analyze_market_context(
    multi_timeframe,
    market_bias,
    market_structure,
    supply_demand
):
    context = {}

    if (
        multi_timeframe["alignment"] == "Aligned"
        and market_bias == "Bullish"
        and market_structure == "Trending"
    ):
        context["Context"] = "Continuation"

    elif (
        multi_timeframe["alignment"] == "Mixed"
    ):
        context["Context"] = "Wait"

    else:
        context["Context"] = "Reversal Watch"

    context["Confidence"] = (
        multi_timeframe["alignment"]
    )

    return context