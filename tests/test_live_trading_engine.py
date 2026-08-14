import time
import MetaTrader5 as mt5

from environment.trading_engine import TradingEngine


# ============================================================
# CONFIGURATION
# ============================================================

SYMBOLS = [
    "GBPUSD",
    "XAUUSD",
]

CYCLES = 10
DELAY_SECONDS = 5


# ============================================================
# INITIALIZE MT5
# ============================================================

if not mt5.initialize():

    print("❌ MT5 initialization failed")

    raise SystemExit


# ============================================================
# ENGINE
# ============================================================

engine = TradingEngine(

    minimum_score=70,

    max_opportunities=3,

    minimum_rr=2.0,

    risk_percent=1.0,

    max_risk_percent=2.0,

    max_positions=1,

    dry_run=True
)


# ============================================================
# STATS
# ============================================================

stats = {

    "OK": 0,

    "ERROR": 0,

    "EXECUTED": 0,

    "DRY_RUN": 0,

    "BLOCKED": 0,

    "WAITING": 0,

    "REJECTED": 0,

    "NOT_EXECUTED": 0,

}


# ============================================================
# HELPER
# ============================================================

def record_status(
    result
):

    if not isinstance(
        result,
        dict
    ):

        return

    status = str(
        result.get(
            "status",
            ""
        )
    ).upper()

    if status in stats:

        stats[status] += 1


# ============================================================
# STRESS TEST
# ============================================================

try:

    for cycle in range(
        1,
        CYCLES + 1
    ):

        print()
        print("=" * 80)
        print(
            f"STRESS TEST CYCLE "
            f"{cycle}/{CYCLES}"
        )
        print("=" * 80)

        for symbol in SYMBOLS:

            print()
            print(
                f"▶ ANALYZING {symbol}"
            )

            try:

                result = engine.run(
                    symbol
                )

                record_status(
                    result
                )

                print(
                    f"ENGINE STATUS: "
                    f"{result.get('status')}"
                )

                print(
                    f"SYMBOL: "
                    f"{result.get('symbol')}"
                )

                # ------------------------------------------------
                # HORIZONS
                # ------------------------------------------------

                horizon_results = result.get(
                    "horizon_results",
                    {}
                )

                if isinstance(
                    horizon_results,
                    dict
                ):

                    for horizon, data in (
                        horizon_results.items()
                    ):

                        if not isinstance(
                            data,
                            dict
                        ):

                            continue

                        print(
                            f"  {horizon}: "
                            f"{data.get('direction', 'N/A')}"
                        )

                # ------------------------------------------------
                # OPPORTUNITIES
                # ------------------------------------------------

                opportunities = result.get(
                    "opportunities",
                    []
                )

                print(
                    f"OPPORTUNITIES: "
                    f"{len(opportunities)}"
                )

                # ------------------------------------------------
                # SELECTED
                # ------------------------------------------------

                selected = result.get(
                    "selected",
                    []
                )

                print(
                    f"SELECTED: "
                    f"{len(selected)}"
                )

                # ------------------------------------------------
                # DECISIONS
                # ------------------------------------------------

                decisions = result.get(
                    "decisions",
                    []
                )

                print(
                    f"DECISIONS: "
                    f"{len(decisions)}"
                )

                for index, decision in enumerate(
                    decisions,
                    start=1
                ):

                    print()
                    print(
                        f"  DECISION #{index}"
                    )

                    print(
                        f"    status: "
                        f"{decision.get('status')}"
                    )

                    print(
                        f"    direction: "
                        f"{decision.get('direction')}"
                    )

                    print(
                        f"    horizon: "
                        f"{decision.get('horizon')}"
                    )

                    print(
                        f"    score: "
                        f"{decision.get('score')}"
                    )

                    print(
                        f"    entry: "
                        f"{decision.get('entry')}"
                    )

                    print(
                        f"    stop_loss: "
                        f"{decision.get('stop_loss')}"
                    )

                    print(
                        f"    take_profit: "
                        f"{decision.get('take_profit')}"
                    )

                    print(
                        f"    rr: "
                        f"{decision.get('rr')}"
                    )

                # ------------------------------------------------
                # EXECUTIONS
                # ------------------------------------------------

                executions = result.get(
                    "executions",
                    []
                )

                print()
                print(
                    f"EXECUTIONS: "
                    f"{len(executions)}"
                )

                for index, execution in enumerate(
                    executions,
                    start=1
                ):

                    record_status(
                        execution
                    )

                    print()
                    print(
                        f"  EXECUTION #{index}"
                    )

                    print(
                        f"    status: "
                        f"{execution.get('status')}"
                    )

                    print(
                        f"    stage: "
                        f"{execution.get('stage')}"
                    )

                    print(
                        f"    reason: "
                        f"{execution.get('reason')}"
                    )

                    print(
                        f"    direction: "
                        f"{execution.get('direction')}"
                    )

                    print(
                        f"    entry: "
                        f"{execution.get('entry')}"
                    )

                    print(
                        f"    stop_loss: "
                        f"{execution.get('stop_loss')}"
                    )

                    print(
                        f"    take_profit: "
                        f"{execution.get('take_profit')}"
                    )

                    print(
                        f"    rr: "
                        f"{execution.get('rr')}"
                    )

            except Exception as error:

                stats["ERROR"] += 1

                print()
                print(
                    f"❌ {symbol} ENGINE ERROR"
                )

                print(
                    f"   {error}"
                )

        if cycle < CYCLES:

            print()
            print(
                f"Waiting "
                f"{DELAY_SECONDS} seconds..."
            )

            time.sleep(
                DELAY_SECONDS
            )


finally:

    mt5.shutdown()


# ============================================================
# FINAL REPORT
# ============================================================

print()
print("=" * 80)
print("LIVE TRADING ENGINE STRESS TEST COMPLETE")
print("=" * 80)

print()

for key, value in stats.items():

    print(
        f"{key:<20}: {value}"
    )

print()
print("=" * 80)