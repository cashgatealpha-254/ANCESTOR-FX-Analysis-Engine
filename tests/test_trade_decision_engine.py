from environment.trade_decision_engine import (
    TradeDecisionEngine
)


# ==================================================
# MOCK OPPORTUNITIES
# ==================================================

opportunities = [

    {
        "symbol": "EURUSD",
        "horizon": "SWING",
        "direction": "BULLISH",
        "score": 78
    },

    {
        "symbol": "GBPUSD",
        "horizon": "INTRADAY",
        "direction": "BULLISH",
        "score": 74
    },

    {
        "symbol": "USDJPY",
        "horizon": "SCALPING",
        "direction": "BEARISH",
        "score": 72
    }
]


# ==================================================
# MOCK HORIZON DATA
# ==================================================

horizon_results = {

    "SWING": {

        "status": "OK",

        "symbol": "EURUSD",

        "horizon": "SWING",

        "direction": "BULLISH",

        "liquidity": {

            "buy_side": [
                {
                    "price": 1.1100
                }
            ],

            "sell_side": [
                {
                    "price": 1.0850
                }
            ]
        },

        "location": {

            "fvg": [
                {
                    "type": "FVG",
                    "direction": "BULLISH",
                    "distance_pct": 0.10,
                    "low": 1.0950,
                    "high": 1.0960
                }
            ],

            "order_blocks": []
        }
    },

    "INTRADAY": {

        "status": "OK",

        "symbol": "GBPUSD",

        "horizon": "INTRADAY",

        "direction": "BULLISH",

        "liquidity": {

            "buy_side": [
                {
                    "price": 1.3100
                }
            ],

            "sell_side": [
                {
                    "price": 1.2900
                }
            ]
        },

        "location": {

            "fvg": [
                {
                    "type": "FVG",
                    "direction": "BULLISH",
                    "distance_pct": 0.08,
                    "low": 1.2980,
                    "high": 1.2990
                }
            ],

            "order_blocks": []
        }
    },

    "SCALPING": {

        "status": "OK",

        "symbol": "USDJPY",

        "horizon": "SCALPING",

        "direction": "BEARISH",

        "liquidity": {

            "buy_side": [
                {
                    "price": 155.00
                }
            ],

            "sell_side": [
                {
                    "price": 154.00
                }
            ]
        },

        "location": {

            "fvg": [
                {
                    "type": "FVG",
                    "direction": "BEARISH",
                    "distance_pct": 0.05,
                    "low": 154.40,
                    "high": 154.50
                }
            ],

            "order_blocks": []
        }
    }
}


# ==================================================
# TEST
# ==================================================

engine = TradeDecisionEngine(
    minimum_rr=2.0,
    max_setups=3
)


# We deliberately don't provide live market data
# here. TradeSetupEngine will use MarketContext itself.

results = engine.decide(
    opportunities,
    horizon_results=horizon_results
)


# ==================================================
# OUTPUT
# ==================================================

print()
print("=" * 70)
print("TRADE DECISION ENGINE TEST")
print("=" * 70)

print()

for index, result in enumerate(
    results,
    start=1
):

    print(
        f"#{index}"
    )

    print(
        f"symbol: "
        f"{result.get('symbol')}"
    )

    print(
        f"horizon: "
        f"{result.get('horizon')}"
    )

    print(
        f"direction: "
        f"{result.get('direction')}"
    )

    print(
        f"score: "
        f"{result.get('score')}"
    )

    print(
        f"status: "
        f"{result.get('status')}"
    )

    print(
        f"entry: "
        f"{result.get('entry')}"
    )

    print(
        f"stop_loss: "
        f"{result.get('stop_loss')}"
    )

    print(
        f"take_profit: "
        f"{result.get('take_profit')}"
    )

    print(
        f"rr: "
        f"{result.get('rr')}"
    )

    print(
        f"trigger: "
        f"{result.get('trigger')}"
    )

    print(
        f"reason: "
        f"{result.get('reason')}"
    )

    print("-" * 70)