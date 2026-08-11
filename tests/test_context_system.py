from environment.context_orchestrator import ContextOrchestrator


def main():

    print("=" * 70)
    print("CONTEXT SYSTEM TEST")
    print("=" * 70)

    orchestrator = ContextOrchestrator()

    symbols = [
        "GBPUSD",
        "EURUSD",
        "USDJPY",
        "XAUUSD",
        "DE30"
    ]

    horizons = [
        "SWING",
        "INTRADAY",
        "SCALPING"
    ]

    for symbol in symbols:

        print()
        print("-" * 70)
        print(symbol)
        print("-" * 70)

        for horizon in horizons:

            print()
            print(f"[{horizon}]")

            try:

                context = orchestrator.build_context(
                    symbol,
                    horizon
                )

                status = context.get(
                    "status",
                    "UNKNOWN"
                )

                print(
                    f"STATUS: {status}"
                )

                if status != "OK":

                    print(
                        "Context could not be built."
                    )

                    continue

                recent = context.get(
                    "recent_context",
                    {}
                )

                changes = context.get(
                    "changes",
                    {}
                )

                print(
                    f"TIMEFRAME: "
                    f"{recent.get('timeframe')}"
                )

                print(
                    f"BARS: "
                    f"{recent.get('bars')}"
                )

                print(
                    f"LATEST CLOSE: "
                    f"{recent.get('latest_close')}"
                )

                print(
                    f"CHANGES: "
                    f"{changes.get('change_count', 0)}"
                )

            except Exception as error:

                print(
                    f"ERROR: {error}"
                )


if __name__ == "__main__":

    main()