import MetaTrader5 as mt5

from environment.execution_engine import ExecutionEngine


# ==================================================
# MT5 CONNECTION
# ==================================================

if not mt5.initialize():

    print("❌ MT5 initialization failed")

    raise SystemExit


# ==================================================
# TEST SETUP
# ==================================================

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


# ==================================================
# EXECUTION ENGINE
# ==================================================

engine = ExecutionEngine(

    max_positions=1,

    max_score=60,

    dry_run=True
)


# ==================================================
# EXECUTE
# ==================================================

result = engine.execute(
    setup
)


# ==================================================
# OUTPUT
# ==================================================

print()
print("=" * 60)
print("EXECUTION ENGINE TEST")
print("=" * 60)

print()

for key, value in result.items():

    print(
        f"{key}: {value}"
    )

print()
print("=" * 60)


# ==================================================
# CLEANUP
# ==================================================

mt5.shutdown()