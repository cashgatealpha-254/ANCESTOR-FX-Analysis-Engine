import MetaTrader5 as mt5
import pandas as pd


def get_candles(symbol: str, timeframe=mt5.TIMEFRAME_M1, n=100):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n)

    if rates is None:
        raise Exception(f"Failed to fetch candles for {symbol}")

    df = pd.DataFrame(rates)

    df["time"] = pd.to_datetime(df["time"], unit="s")

    return df