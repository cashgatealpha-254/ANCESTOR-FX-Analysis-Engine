import MetaTrader5 as mt5
import pandas as pd

def get_candles(symbol: str, timeframe=mt5.TIMEFRAME_M1, n=100):
        print("Symbol:", symbol, type(symbol))
        print("Timeframe:", timeframe, type(timeframe))
        print("Bars:", n, type(n))

        timeframe = TIMEFRAME_MAPPING.get(timeframe, timeframe)

        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n)

        if rates is None:
         raise Exception(f"Failed to fetch candles for {symbol}")

        df = pd.DataFrame(rates)

        df["time"] = pd.to_datetime(df["time"], unit="s")
        df = df[["time", "open", "high", "low", "close", "tick_volume"]]

        return df

TIMEFRAME_MAPPING = {
    "M1": mt5.TIMEFRAME_M1,
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "M30": mt5.TIMEFRAME_M30,
    "H1": mt5.TIMEFRAME_H1,
    "H4": mt5.TIMEFRAME_H4,
    "D1": mt5.TIMEFRAME_D1,
    "W1": mt5.TIMEFRAME_W1,
    "MN1": mt5.TIMEFRAME_MN1
}