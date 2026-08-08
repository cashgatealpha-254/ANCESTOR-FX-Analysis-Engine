from environment.opportunity_selector import (
    OpportunitySelector
)


selector = OpportunitySelector(
    minimum_score=70,
    max_opportunities=3
)


opportunities = [

    {
        "symbol": "EURUSD",
        "horizon": "SWING",
        "direction": "BULLISH",
        "score": 82
    },

    {
        "symbol": "GBPUSD",
        "horizon": "INTRADAY",
        "direction": "BULLISH",
        "score": 76
    },

    {
        "symbol": "USDJPY",
        "horizon": "SCALPING",
        "direction": "BEARISH",
        "score": 68
    },

    {
        "symbol": "XAUUSD",
        "horizon": "INTRADAY",
        "direction": "BULLISH",
        "score": 91
    },

    {
        "symbol": "EURUSD",
        "horizon": "INTRADAY",
        "direction": "BULLISH",
        "score": 74
    }
]


selected = selector.select(
    opportunities
)


print()
print("Selected opportunities:")
print()


for index, opportunity in enumerate(
    selected,
    start=1
):

    print(
        f"#{index} "
        f"{opportunity['symbol']} | "
        f"{opportunity['horizon']} | "
        f"{opportunity['direction']} | "
        f"{opportunity['score']}/100"
    )