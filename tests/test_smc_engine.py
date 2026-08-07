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

    print("\nSWING HIGHS:")
    for swing in result["swing_highs"][-5:]:
        print(swing)

    print("\nSWING LOWS:")
    for swing in result["swing_lows"][-5:]:
        print(swing)

    print("\nSTRUCTURE:")
    for item in result["structure"][-10:]:
        print(item)

    print("\nSTRUCTURE BREAKS:")
    for event in result["structure_breaks"][-10:]:
        print(event)


mt5.shutdown()