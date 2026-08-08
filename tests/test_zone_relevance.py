from environment.zone_relevance import ZoneRelevance


engine = ZoneRelevance(
    max_zones=3
)

result = engine.analyze(

    direction="BULLISH",

    fvg={
        "bullish": [
            {"type": "FVG", "distance_pct": 0.50},
            {"type": "FVG", "distance_pct": 0.10},
            {"type": "FVG", "distance_pct": 0.03},
            {"type": "FVG", "distance_pct": 0.80},
        ],
        "bearish": [
            {"type": "FVG", "distance_pct": 0.02},
        ]
    },

    order_blocks={
        "bullish": [
            {"type": "ORDER_BLOCK", "distance_pct": 0.40},
            {"type": "ORDER_BLOCK", "distance_pct": 0.08},
            {"type": "ORDER_BLOCK", "distance_pct": 0.20},
            {"type": "ORDER_BLOCK", "distance_pct": 0.60},
        ],
        "bearish": []
    },

    profile={
        "POC": {"price": 1.1000, "distance_pct": 0.15},
        "VAH": {"price": 1.1020, "distance_pct": 0.30},
        "VAL": {"price": 1.0980, "distance_pct": 0.05},
    }
)


print("\nRelevant zones:")
print(result)