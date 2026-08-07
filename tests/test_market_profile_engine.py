import MetaTrader5 as mt5

from environment.market_scanner import MarketScanner
from environment.market_profile_engine import MarketProfileEngine


if not mt5.initialize():
    print("MT5 initialization failed")
    print(mt5.last_error())
    raise SystemExit


scanner = MarketScanner()
market_profile = MarketProfileEngine()

markets = scanner.scan()

for symbol, df in markets.items():

    result = market_profile.analyze(df)

    print(f"\n{'=' * 50}")
    print(symbol)

    print(f"POC: {result['poc']}")
    print(f"VAH: {result['vah']}")
    print(f"VAL: {result['val']}")


mt5.shutdown()