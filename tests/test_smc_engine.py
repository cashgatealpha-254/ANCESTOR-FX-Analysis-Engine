import MetaTrader5 as mt5

from environment.market_scanner import MarketScanner
from environment.smc_engine import SMCEngine


if not mt5.initialize():
    print("MT5 initialization failed")
    print(mt5.last_error())
    raise SystemExit


scanner = MarketScanner()
smc = SMCEngine()

markets = scanner.scan()

for symbol, df in markets.items():

    result = smc.analyze(df)

    print(f"\n{'=' * 60}")
    print(symbol)

    print("\nSTRUCTURE SUMMARY")
    print("-" * 60)

    print(
        f"Structure Bias: "
        f"{result.get('structure_bias', 'NEUTRAL')}"
    )

    structure = result.get("structure", [])

    if structure:
        latest = structure[-1]

        print(
            f"Latest Structure: "
            f"{latest['type']} "
            f"@ {latest['price']}"
        )
    else:
        print("Latest Structure: NONE")

    breaks = result.get(
        "structure_breaks",
        []
    )

    if breaks:

        latest_break = breaks[-1]

        print(
            f"Latest Break: "
            f"{latest_break['type']} "
            f"{latest_break['direction']} "
            f"@ {latest_break['price']}"
        )

    else:

        print("Latest Break: NONE")

    print("\nMSS")
    print("-" * 60)

    mss = result.get("mss", {})

    print(
        f"MSS: "
        f"{mss.get('mss', False)}"
    )

    print(
        f"Direction: "
        f"{mss.get('direction', 'NEUTRAL')}"
    )

    print(
        f"Type: "
        f"{mss.get('type')}"
    )

    print(
        f"Reason: "
        f"{mss.get('reason')}"
    )


mt5.shutdown()