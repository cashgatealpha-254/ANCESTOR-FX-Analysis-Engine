import MetaTrader5 as mt5


def connect_mt5():
    """Connect to the MetaTrader 5 terminal."""
    if not mt5.initialize():
        raise Exception(f"MT5 initialization failed: {mt5.last_error()}")

    print("✅ Connected to MetaTrader 5")


def disconnect_mt5():
    """Disconnect from the MetaTrader 5 terminal."""
    mt5.shutdown()
    print("🔌 Disconnected from MT5")

def get_price(symbol: str):
    """Get current bid/ask price from MT5."""
    tick = mt5.symbol_info_tick(symbol)

    if tick is None:
        raise Exception(f"Failed to get price for {symbol}")

    return {
        "symbol": symbol,
        "bid": tick.bid,
        "ask": tick.ask,
        "spread": tick.ask - tick.bid,
        "time": tick.time
    } 

import pandas as pd

def get_candles(symbol, timeframe, bars):
    rates = mt5.copy_rates_from_pos(
        symbol,
        timeframe,
        0,
        bars
    )

    if rates is None:
        raise Exception(f"Failed to get candles for {symbol}")

    df = pd.DataFrame(rates)

    df["time"] = pd.to_datetime(df["time"], unit="s")

    df.set_index("time", inplace=True)

    return df
def connect_mt5():
    if not mt5.initialize():
        raise Exception(f"MT5 initialization failed: {mt5.last_error()}")

    print("✅ Connected to MetaTrader 5")


def disconnect_mt5():
    mt5.shutdown()
    print("🔌 Disconnected from MT5")