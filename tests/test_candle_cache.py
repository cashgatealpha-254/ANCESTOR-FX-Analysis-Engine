from mt5.connection import (
    connect_mt5,
    disconnect_mt5
)

from environment.candle_cache import CandleCache


def main():

    print("=" * 70)
    print("ANCESTOR FX CANDLE CACHE TEST")
    print("=" * 70)

    if not connect_mt5():

        print("MT5 connection failed.")

        return

    try:

        cache = CandleCache()

        symbol = "GBPUSD"

        print(
            f"\nBuilding cache for {symbol}..."
        )

        context = (
            cache.build_symbol_context(
                symbol
            )
        )

        print("\n" + "=" * 70)
        print("CACHE STATUS")
        print("=" * 70)

        status = cache.status(
            symbol
        )

        for timeframe, info in status.items():

            print(
                f"{timeframe:<5} | "
                f"{info['status']:<8} | "
                f"Candles: {info['bars']} / "
                f"{info['expected']}"
            )

            print(
                f"      "
                f"{info['oldest']} → "
                f"{info['latest']}"
            )

        print("\n" + "=" * 70)
        print("CACHE TEST COMPLETE")
        print("=" * 70)

    finally:

        disconnect_mt5()


if __name__ == "__main__":
    main()