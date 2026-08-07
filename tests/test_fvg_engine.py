import MetaTrader5 as mt5

from environment.market_scanner import MarketScanner
from environment.fvg_engine import FVGEngine


if not mt5.initialize():
    print("MT5 initialization failed")
    print(mt5.last_error())
    raise SystemExit


scanner = MarketScanner()
fvg = FVGEngine()

markets = scanner.scan()

for symbol, df in markets.items():

    result = fvg.analyze(df)

    print(f"\n{'=' * 60}")
    print(symbol)

    print("\nBULLISH FVG:")
    for gap in result["bullish"][-10:]:
        print(gap)

    print("\nBEARISH FVG:")
    for gap in result["bearish"][-10:]:
        print(gap)


mt5.shutdown()