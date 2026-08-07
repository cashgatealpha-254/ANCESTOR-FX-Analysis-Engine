import MetaTrader5 as mt5

from environment.market_scanner import MarketScanner
from environment.supply_demand_engine import SupplyDemandEngine


if not mt5.initialize():
    print("MT5 initialization failed")
    print(mt5.last_error())
    raise SystemExit


scanner = MarketScanner()
supply_demand = SupplyDemandEngine()

markets = scanner.scan()

for symbol, df in markets.items():

    result = supply_demand.analyze(df)

    print(f"\n{'=' * 50}")
    print(symbol)

    print("\nSUPPLY ZONES:")

    for zone in result["supply"]:
        print(zone)

    print("\nDEMAND ZONES:")

    for zone in result["demand"]:
        print(zone)


mt5.shutdown()