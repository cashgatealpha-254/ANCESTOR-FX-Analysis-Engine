import MetaTrader5 as mt5

from environment.horizon_engine import HorizonEngine


if not mt5.initialize():
    print("MT5 initialization failed")
    print(mt5.last_error())
    raise SystemExit


engine = HorizonEngine()

symbols = [
    "GBPUSD",
    "EURUSD",
    "USDJPY",
    "XAUUSD",
    "DE30"
]

for symbol in symbols:

    print(f"\n{'=' * 70}")
    print(symbol)

    result = engine.analyze(symbol)

    for horizon, data in result.items():

        print(f"\n--- {horizon} ---")

        print(f"Status: {data['status']}")

        if data["status"] == "OK":

            print(
                f"Bars: {data['bars']}"
            )

            print(
                f"Trend: {data['trend']}"
            )

            print(
                f"Market Profile: "
                f"{data['market_profile']}"
            )

            print(
                f"SMC structure: "
                f"{data['smc'].get('structure', [])[-3:]}"
            )


mt5.shutdown()