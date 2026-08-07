import MetaTrader5 as mt5

from environment.market_scanner import MarketScanner
from environment.location_engine import LocationEngine
from environment.supply_demand_engine import SupplyDemandEngine
from environment.market_profile_engine import MarketProfileEngine
from environment.fvg_engine import FVGEngine
from environment.order_block_engine import OrderBlockEngine


if not mt5.initialize():
    print("MT5 initialization failed")
    print(mt5.last_error())
    raise SystemExit


scanner = MarketScanner()

location = LocationEngine()

supply_demand = SupplyDemandEngine()
market_profile = MarketProfileEngine()
fvg_engine = FVGEngine()
order_blocks = OrderBlockEngine()


markets = scanner.scan()


for symbol, df in markets.items():

    sd = supply_demand.analyze(df)

    profile = market_profile.analyze(df)

    fvg = fvg_engine.analyze(df)

    blocks = order_blocks.analyze(df)

    result = location.analyze(
        df,
        supply_demand=sd,
        market_profile=profile,
        fvg=fvg,
        order_blocks=blocks
    )

    print(f"\n{'=' * 60}")
    print(symbol)

    print(
        f"Current price: "
        f"{result['current_price']}"
    )

    print(
        f"Location score: "
        f"{result['score']}/20"
    )

    print("\nNEARBY ZONES:")

    for zone in result["nearby_zones"]:
        print(zone)


mt5.shutdown()