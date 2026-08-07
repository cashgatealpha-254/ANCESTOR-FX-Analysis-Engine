import pandas as pd

from indicators.trend import calculate_ema


class TrendEngine:

    def analyze(self, df: pd.DataFrame):

        df = calculate_ema(df)

        latest = df.iloc[-1]
        previous = df.iloc[-2]

        ema20 = latest["EMA20"]
        ema50 = latest["EMA50"]

        separation = ema20 - ema50
        previous_separation = (
            previous["EMA20"] - previous["EMA50"]
        )

        if ema20 > ema50:
            direction = "BULLISH"

        elif ema20 < ema50:
            direction = "BEARISH"

        else:
            direction = "NEUTRAL"

        if abs(separation) > abs(previous_separation):
            momentum = "STRENGTHENING"

        elif abs(separation) < abs(previous_separation):
            momentum = "WEAKENING"

        else:
            momentum = "STABLE"

        return {
            "direction": direction,
            "momentum": momentum,
            "ema20": ema20,
            "ema50": ema50,
            "separation": separation
        }