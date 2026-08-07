import MetaTrader5 as mt5

from environment.horizon_engine import HorizonEngine
from environment.opportunity_ranker import OpportunityRanker


if not mt5.initialize():
    print("MT5 initialization failed")
    print(mt5.last_error())
    raise SystemExit


horizon_engine = HorizonEngine()
ranker = OpportunityRanker()

symbols = [
    "GBPUSD",
    "EURUSD",
    "USDJPY",
    "XAUUSD",
    "US30"
]

all_opportunities = []

for symbol in symbols:

    print(f"\nScanning {symbol}...")

    horizon_results = (
        horizon_engine.analyze(symbol)
    )

    ranked = ranker.rank(
        horizon_results
    )

    for opportunity in ranked:

        opportunity["symbol"] = symbol

        all_opportunities.append(
            opportunity
        )


all_opportunities.sort(
    key=lambda item: item["score"],
    reverse=True
)


print("\n")
print("=" * 70)
print("ANCESTOR OPPORTUNITY RANKING")
print("=" * 70)


for position, opportunity in enumerate(
    all_opportunities,
    start=1
):

    print(
        f"\n#{position} "
        f"{opportunity['symbol']} "
        f"| {opportunity['horizon']} "
        f"| {opportunity['direction']} "
        f"| SCORE: {opportunity['score']}/100"
    )

    for reason in opportunity["reasons"]:
        print(f"  + {reason}")

mt5.shutdown()