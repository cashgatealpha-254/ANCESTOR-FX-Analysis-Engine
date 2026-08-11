import MetaTrader5 as mt5
import pandas as pd


class FastForwardEngine:

    def __init__(self):

        # Recent-context windows.
        # These are deliberately configurable.
        self.horizons = {

            "SWING": {
                "timeframe": mt5.TIMEFRAME_H4,
                "bars": 90
            },

            "INTRADAY": {
                "timeframe": mt5.TIMEFRAME_M15,
                "bars": 240
            },

            "SCALPING": {
                "timeframe": mt5.TIMEFRAME_M5,
                "bars": 300
            }
        }

    # ==================================================
    # ANALYZE
    # ==================================================

    def analyze(
        self,
        symbol,
        horizon
    ):

        settings = self.horizons.get(
            horizon
        )

        if settings is None:

            return {
                "status": "ERROR",
                "error": (
                    f"Unknown horizon: {horizon}"
                )
            }

        timeframe = settings["timeframe"]
        bars = settings["bars"]

        rates = mt5.copy_rates_from_pos(
            symbol,
            timeframe,
            0,
            bars
        )

        if rates is None:

            return {
                "status": "NO_DATA",
                "symbol": symbol,
                "horizon": horizon
            }

        df = pd.DataFrame(rates)

        if df.empty:

            return {
                "status": "NO_DATA",
                "symbol": symbol,
                "horizon": horizon
            }

        df["time"] = pd.to_datetime(
            df["time"],
            unit="s"
        )

        return {

            "status": "OK",

            "symbol": symbol,

            "horizon": horizon,

            "timeframe": timeframe,

            "bars": len(df),

            "start_time": (
                df["time"].iloc[0].isoformat()
            ),

            "end_time": (
                df["time"].iloc[-1].isoformat()
            ),

            "latest_close": float(
                df["close"].iloc[-1]
            ),

            "data": df
        }