# test_deep_context.py

from mt5.connection import (
    connect_mt5,
    disconnect_mt5,
)

from environment.deep_context_engine import (
    DeepContextEngine,
)


def main():

    print()
    print("=" * 70)
    print("ANCESTOR FX DEEP CONTEXT TEST")
    print("=" * 70)

    if not connect_mt5():

        print("MT5 connection failed.")
        return

    try:

        engine = DeepContextEngine()

        print()
        print("Building GBPUSD deep context...")
        print()

        context = (
            engine.build_symbol_context(
                "GBPUSD"
            )
        )

        print(
            f"Symbol: {context['symbol']}"
        )

        print()

        print("TIMEFRAME DATA")
        print("-" * 70)

        for timeframe, data in (
            context[
                "timeframes"
            ].items()
        ):

            print(
                f"{timeframe:5} | "
                f"Status: {data['status']:7} | "
                f"Candles: {data['count']}"
            )

            if data["status"] == "READY":

                print(
                    f"       "
                    f"{data['start']} "
                    f"→ "
                    f"{data['end']}"
                )

        print()

        print("HORIZONS")
        print("-" * 70)

        for horizon, data in (
            context[
                "horizons"
            ].items()
        ):

            print(
                f"{horizon}: "
                f"{', '.join(data.keys())}"
            )

        print()

        print("=" * 70)
        print("DEEP CONTEXT TEST COMPLETE")
        print("=" * 70)

    finally:

        disconnect_mt5()


if __name__ == "__main__":
    main()