import MetaTrader5 as mt5

from environment.market_scanner import MarketScanner
from environment.trend_engine import TrendEngine


if not mt5.initialize():
    print("MT5 initialization failed")
    print(mt5.last_error())
    raise SystemExit
scanner = MarketScanner()
trend_engine = TrendEngine()

markets = scanner.scan()

for symbol, df in markets.items():

    result = trend_engine.analyze(df)

    print(f"\n{symbol}")
    print(f"Direction: {result['direction']}")
    print(f"Momentum: {result['momentum']}")
    print(f"EMA20: {result['ema20']}")
    print(f"EMA50: {result['ema50']}")
    print(f"Separation: {result['separation']}")

    mt5.shutdown()