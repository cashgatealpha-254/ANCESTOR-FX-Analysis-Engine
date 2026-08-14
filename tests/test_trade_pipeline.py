from environment.opportunity_selector import (
    OpportunitySelector
)

from environment.trade_setup_engine import (
    TradeSetupEngine
)


# ==================================================
# MOCK OPPORTUNITIES
# ==================================================

opportunities = [

    {
        "symbol": "EURUSD",
        "horizon": "SWING",
        "direction": "BULLISH",
        "score": 82,

        "trend": {
            "trend": "BULLISH"
        },

        "liquidity": {
            "buy_side": [
                {
                    "price": 1.1050
                }
            ],
            "sell_side": []
        },

        "relevant_zones": {

            "fvg": [
                {
                    "type": "FVG",
                    "direction": "BULLISH",
                    "distance_pct": 0.03,
                    "low": 1.1000,
                    "high": 1.1010
                }
            ],

            "order_blocks": [
                {
                    "type": "ORDER_BLOCK",
                    "direction": "BULLISH",
                    "distance_pct": 0.08,
                    "low": 1.0990,
                    "high": 1.1005
                }
            ]
        }
    },

    {
        "symbol": "USDJPY",
        "horizon": "INTRADAY",
        "direction": "BEARISH",
        "score": 76,

        "trend": {
            "trend": "BEARISH"
        },

        "liquidity": {
            "buy_side": [],
            "sell_side": [
                {
                    "price": 146.20
                }
            ]
        },

        "relevant_zones": {

            "fvg": [
                {
                    "type": "FVG",
                    "direction": "BEARISH",
                    "distance_pct": 0.04,
                    "low": 147.00,
                    "high": 147.20
                }
            ],

            "order_blocks": [
                {
                    "type": "ORDER_BLOCK",
                    "direction": "BEARISH",
                    "distance_pct": 0.09,
                    "low": 147.10,
                    "high": 147.30
                }
            ]
        }
    }
]


# ==================================================
# SELECT
# ==================================================

selector = OpportunitySelector(
    minimum_score=70,
    max_opportunities=3
)

selected = selector.select(
    opportunities
)


# ==================================================
# BUILD SETUPS
# ==================================================

setup_engine = TradeSetupEngine(
    minimum_rr=2.0
)


setups = []


for opportunity in selected:

    setup = setup_engine.build(
        opportunity
    )

    setups.append(
        setup
    )


# ==================================================
# OUTPUT
# ==================================================

print()
print("=" * 60)
print("TRADE PIPELINE")
print("=" * 60)

for index, setup in enumerate(
    setups,
    start=1
):

    print()

    print(
        f"#{index} "
        f"{setup.get('symbol')} | "
        f"{setup.get('horizon')} | "
        f"{setup.get('direction')}"
    )

    print(
        f"STATUS: "
        f"{setup.get('status')}"
    )

    if setup.get("status") == "READY":

        print(
            f"ENTRY: "
            f"{setup.get('entry')}"
        )

        print(
            f"SL: "
            f"{setup.get('stop_loss')}"
        )

        print(
            f"TP: "
            f"{setup.get('take_profit')}"
        )

        print(
            f"RR: "
            f"{setup.get('rr')}"
        )

        print(
            f"TRIGGER: "
            f"{setup.get('trigger')}"
        )

        print(
            f"EXECUTION: "
            f"{setup.get('execution')}"
        )

    else:

        print(
            f"REASON: "
            f"{setup.get('reason')}"
        )

        print(
            f"TRIGGER: "
            f"{setup.get('trigger')}"
        )

        print(
            f"CURRENT PRICE: "
            f"{setup.get('current_price')}"
        )

        print(
            f"ZONE: "
            f"{setup.get('zone')}"
        )

print()
print("=" * 60)