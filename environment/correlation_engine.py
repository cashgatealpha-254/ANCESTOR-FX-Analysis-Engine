import pandas as pd


class CorrelationEngine:

    def __init__(self):

        self.groups = {

            "USD": [
                "GBPUSD",
                "EURUSD",
                "AUDUSD",
                "NZDUSD"
            ],

            "SAFE_HAVEN": [
                "XAUUSD",
                "USDJPY"
            ]

        }

    def analyse(self, market_data):

        report = {}

        for group, symbols in self.groups.items():

            direction = {}

            for symbol in symbols:

                if symbol not in market_data:
                    continue

                df = market_data[symbol]

                last = df["close"].iloc[-1]
                previous = df["close"].iloc[-2]

                if last > previous:

                    direction[symbol] = "Bullish"

                else:

                    direction[symbol] = "Bearish"

            report[group] = direction

        return report