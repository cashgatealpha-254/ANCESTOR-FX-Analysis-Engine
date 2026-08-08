import MetaTrader5 as mt5

from environment.execution_pipeline import (
    ExecutionPipeline
)


if not mt5.initialize():

    print("❌ MT5 initialization failed")

    raise SystemExit


setup = {

    "status": "READY",

    "symbol": "GBPUSD",

    "horizon": "INTRADAY",

    "direction": "BULLISH",

    "score": 75,

    "entry": 1.30000,

    "stop_loss": 1.29800,

    "take_profit": 1.30600
}


pipeline = ExecutionPipeline(

    risk_percent=1.0,

    max_risk_percent=2.0,

    minimum_rr=2.0,

    max_positions=1,

    dry_run=True
)


result = pipeline.execute(
    setup
)


print()
print("=" * 70)
print("EXECUTION PIPELINE TEST")
print("=" * 70)

print()

for key, value in result.items():

    print(
        f"{key}: {value}"
    )

print()
print("=" * 70)


mt5.shutdown()