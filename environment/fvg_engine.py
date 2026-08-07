import pandas as pd


class FVGEngine:

    def __init__(self, min_gap_size=0.0):
        self.min_gap_size = min_gap_size

    def analyze(self, df: pd.DataFrame):
        """
        Detect three-candle Fair Value Gaps.

        Bullish FVG:
            candle 3 low > candle 1 high

        Bearish FVG:
            candle 3 high < candle 1 low

        Returns:
            {
                "bullish": [...],
                "bearish": [...]
            }
        """

        required_columns = {
            "high",
            "low"
        }

        missing = required_columns - set(df.columns)

        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

        if len(df) < 3:
            return {
                "bullish": [],
                "bearish": []
            }

        data = df.copy().reset_index(drop=False)

        bullish = []
        bearish = []

        for i in range(2, len(data)):

            candle_1 = data.iloc[i - 2]
            candle_2 = data.iloc[i - 1]
            candle_3 = data.iloc[i]

            # -----------------------------
            # Bullish FVG
            # -----------------------------

            bullish_gap = (
                candle_3["low"]
                - candle_1["high"]
            )

            if bullish_gap > self.min_gap_size:

                bullish.append({
                    "type": "BULLISH_FVG",
                    "low": float(candle_1["high"]),
                    "high": float(candle_3["low"]),
                    "size": float(bullish_gap),
                    "index": candle_3["index"],
                    "origin_index": candle_2["index"]
                })

            # -----------------------------
            # Bearish FVG
            # -----------------------------

            bearish_gap = (
                candle_1["low"]
                - candle_3["high"]
            )

            if bearish_gap > self.min_gap_size:

                bearish.append({
                    "type": "BEARISH_FVG",
                    "low": float(candle_3["high"]),
                    "high": float(candle_1["low"]),
                    "size": float(bearish_gap),
                    "index": candle_3["index"],
                    "origin_index": candle_2["index"]
                })

        return {
            "bullish": bullish,
            "bearish": bearish
        }