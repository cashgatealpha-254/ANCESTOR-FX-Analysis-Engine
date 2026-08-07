import MetaTrader5 as mt5

from environment.market_scanner import MarketScanner
from environment.liquidity_engine import LiquidityEngine


if not mt5.initialize():
    print("MT5 initialization failed")
    print(mt5.last_error())
    raise SystemExit


scanner = MarketScanner()
liquidity = LiquidityEngine()

markets = scanner.scan()

for symbol, df in markets.items():

    result = liquidity.analyze(df)

    print(f"\n{'=' * 60}")
    print(symbol)

    print("\nBUY-SIDE LIQUIDITY:")
    for level in result["buy_side"][-10:]:
        print(level)

    print("\nSELL-SIDE LIQUIDITY:")
    for level in result["sell_side"][-10:]:
        print(level)


mt5.shutdown()