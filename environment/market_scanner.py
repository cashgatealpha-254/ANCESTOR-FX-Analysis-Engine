import MetaTrader5 as mt5
import pandas as pd

from core.logger import Logger
from core.exceptions import CandleDataError 


class MarketScanner:

    def __init__(self):

        self.logger = Logger()
        self.symbols = [

            "GBPUSD",
            "EURUSD",
            "USDJPY",
            "AUDUSD",
            "USDCHF",
            "USDCAD",
            "NZDUSD",

            "XAUUSD",
            "XAGUSD",

            "US500",
            "NASDAQ-100",
            "DE30",

        ]

    def scan(self, timeframe=mt5.TIMEFRAME_M15, bars=200):

        results = {}

        for symbol in self.symbols:

            rates = mt5.copy_rates_from_pos(
                symbol,
                timeframe,
                0,
                bars
            )

            if rates is None:

                self.logger.warning(f"Failed to retrieve data for {symbol}")
                continue

            df = pd.DataFrame(rates)

            df["time"] = pd.to_datetime(
                df["time"],
                unit="s"
            )

            results[symbol] = df

        return results