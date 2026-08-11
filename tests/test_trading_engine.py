import MetaTrader5 as mt5

from environment.trading_engine import TradingEngine


# ==================================================
# MT5 INITIALIZATION
# ==================================================

if not mt5.initialize():

    print(
        "MT5 initialization failed"
    )

    print(
        mt5.last_error()
    )

    raise SystemExit


# ==================================================
# ENGINE
# ==================================================

engine = TradingEngine(
    minimum_score=70,
    max_opportunities=3,
    minimum_rr=2.0,
    risk_percent=1.0,
    max_risk_percent=2.0,
    max_positions=1,
    dry_run=True
)


# ==================================================
# SYMBOLS
# ==================================================

symbols = [

    "GBPUSD",
    "EURUSD",
    "USDJPY",
    "XAUUSD",
    "DE30"

]


# ==================================================
# RUN
# ==================================================

results = engine.run_many(
    symbols
)


# ==================================================
# OUTPUT
# ==================================================

for symbol, result in results.items():

    print()
    print("=" * 70)
    print(symbol)
    print("=" * 70)

    print(
        f"STATUS: "
        f"{result.get('status')}"
    )

    if result.get(
        "status"
    ) != "OK":

        print(
            f"REASON: "
            f"{result.get('reason')}"
        )

        continue

    opportunities = result.get(
        "opportunities",
        []
    )

    selected = result.get(
        "selected",
        []
    )

    decisions = result.get(
        "decisions",
        []
    )

    executions = result.get(
        "executions",
        []
    )

    print()
    print(
        f"OPPORTUNITIES: "
        f"{len(opportunities)}"
    )

    for opportunity in opportunities[:3]:

        print(
            f"  {opportunity.get('symbol')} | "
            f"{opportunity.get('horizon')} | "
            f"{opportunity.get('direction')} | "
            f"SCORE {opportunity.get('score')}"
        )

    print()
    print(
        f"SELECTED: "
        f"{len(selected)}"
    )

    for opportunity in selected:

        print(
            f"  {opportunity.get('symbol')} | "
            f"{opportunity.get('horizon')} | "
            f"{opportunity.get('direction')} | "
            f"SCORE {opportunity.get('score')}"
        )

    print()
    print(
        f"DECISIONS: "
        f"{len(decisions)}"
    )

    for decision in decisions:

        print(
            f"  {decision.get('symbol')} | "
            f"{decision.get('direction')} | "
            f"{decision.get('status')}"
        )

        if decision.get(
            "entry"
        ) is not None:

            print(
                f"    ENTRY: "
                f"{decision.get('entry')}"
            )

        if decision.get(
            "stop_loss"
        ) is not None:

            print(
                f"    SL: "
                f"{decision.get('stop_loss')}"
            )

        if decision.get(
            "take_profit"
        ) is not None:

            print(
                f"    TP: "
                f"{decision.get('take_profit')}"
            )

        if decision.get(
            "rr"
        ) is not None:

            print(
                f"    RR: "
                f"{decision.get('rr')}"
            )

    print()
    print(
        f"EXECUTIONS: "
        f"{len(executions)}"
    )

    for execution in executions:

        print(
            f"  {execution.get('status')} | "
            f"STAGE: {execution.get('stage')}"
        )

        if execution.get(
            "reason"
        ):

            print(
                f"    {execution.get('reason')}"
            )


# ==================================================
# SHUTDOWN
# ==================================================

mt5.shutdown()