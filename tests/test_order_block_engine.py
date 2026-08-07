import MetaTrader5 as mt5

from environment.market_scanner import MarketScanner
from environment.order_block_engine import OrderBlockEngine


if not mt5.initialize():
    print("MT5 initialization failed")
    print(mt5.last_error())
    raise SystemExit


scanner = MarketScanner()
order_blocks = OrderBlockEngine()

markets = scanner.scan()

for symbol, df in markets.items():

    result = order_blocks.analyze(df)

    print(f"\n{'=' * 60}")
    print(symbol)

    print("\nBULLISH ORDER-BLOCK CANDIDATES:")

    for block in result["bullish"][-10:]:
        print(block)

    print("\nBEARISH ORDER-BLOCK CANDIDATES:")

    for block in result["bearish"][-10:]:
        print(block)


mt5.shutdown()