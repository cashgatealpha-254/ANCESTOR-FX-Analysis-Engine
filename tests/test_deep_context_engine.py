from mt5.connection import (
    connect_mt5,
    disconnect_mt5
)

from environment.deep_context_engine import (
    DeepContextEngine
)


def main():

    print("=" * 70)
    print("ANCESTOR FX DEEP CONTEXT ENGINE TEST")
    print("=" * 70)

    if not connect_mt5():

        print(
            "MT5 connection failed."
        )

        return

    try:

        engine = DeepContextEngine()

        result = (
            engine.build_symbol_context(
                "GBPUSD"
            )
        )

        print()
        print("=" * 70)
        print("DEEP CONTEXT RESULT")
        print("=" * 70)

        print(
            f"Symbol: "
            f"{result['symbol']}"
        )

        print()

        print("TIMEFRAMES")

        for timeframe, data in (
            result[
                "timeframes"
            ].items()
        ):

            print(
                f"{timeframe}: "
                f"{data['status']} | "
                f"{data.get('candles', 0)} candles"
            )

        print()

        print("HORIZONS")

        for horizon, data in (
            result[
                "horizons"
            ].items()
        ):

            print(
                f"{horizon}: "
                f"{data.get('status')} | "
                f"Direction: "
                f"{data.get('direction')} | "
                f"Bars: "
                f"{data.get('bars', 0)}"
            )

        print()
        print("=" * 70)
        print("TEST COMPLETE")
        print("=" * 70)

    finally:

        disconnect_mt5()


if __name__ == "__main__":
    main()