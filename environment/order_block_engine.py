import pandas as pd


class OrderBlockEngine:

    def __init__(self, lookback=5):
        self.lookback = lookback

    def analyze(self, df: pd.DataFrame):
        """
        Identify order-block candidates from displacement candles.

        Bullish OB:
            Last bearish candle before strong bullish displacement.

        Bearish OB:
            Last bullish candle before strong bearish displacement.
        """

        required_columns = {
            "open",
            "high",
            "low",
            "close"
        }

        missing = required_columns - set(df.columns)

        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

        if len(df) < self.lookback + 2:
            return {
                "bullish": [],
                "bearish": []
            }

        data = df.copy().reset_index(drop=False)

        data["range"] = data["high"] - data["low"]
        data["body"] = (
            data["close"] - data["open"]
        ).abs()

        data["average_range"] = (
            data["range"]
            .rolling(
                window=20,
                min_periods=5
            )
            .mean()
        )

        bullish = []
        bearish = []

        for i in range(1, len(data)):

            candle = data.iloc[i]

            average_range = candle["average_range"]

            if pd.isna(average_range):
                continue

            if average_range <= 0:
                continue

            displacement_strength = (
                candle["range"] / average_range
            )

            # Require meaningful displacement.
            if displacement_strength < 1.5:
                continue

            bullish_displacement = (
                candle["close"] > candle["open"]
            )

            bearish_displacement = (
                candle["close"] < candle["open"]
            )

            # --------------------------------
            # Bullish Order Block Candidate
            # --------------------------------

            if bullish_displacement:

                origin = self._find_previous_opposite_candle(
                    data,
                    i,
                    direction="BULLISH"
                )

                if origin is not None:

                    bullish.append({
                        "type": "BULLISH_OB_CANDIDATE",
                        "low": float(origin["low"]),
                        "high": float(origin["high"]),
                        "origin_index": origin["index"],
                        "displacement_index": candle["index"],
                        "displacement_strength": round(
                            float(displacement_strength),
                            2
                        )
                    })

            # --------------------------------
            # Bearish Order Block Candidate
            # --------------------------------

            elif bearish_displacement:

                origin = self._find_previous_opposite_candle(
                    data,
                    i,
                    direction="BEARISH"
                )

                if origin is not None:

                    bearish.append({
                        "type": "BEARISH_OB_CANDIDATE",
                        "low": float(origin["low"]),
                        "high": float(origin["high"]),
                        "origin_index": origin["index"],
                        "displacement_index": candle["index"],
                        "displacement_strength": round(
                            float(displacement_strength),
                            2
                        )
                    })

        return {
            "bullish": bullish,
            "bearish": bearish
        }

    def _find_previous_opposite_candle(
        self,
        data,
        displacement_index,
        direction
    ):
        """
        Find the most recent candle of the opposite
        direction before the displacement candle.
        """

        start = max(
            0,
            displacement_index - self.lookback
        )

        for i in range(
            displacement_index - 1,
            start - 1,
            -1
        ):

            candle = data.iloc[i]

            bullish = (
                candle["close"] > candle["open"]
            )

            bearish = (
                candle["close"] < candle["open"]
            )

            if direction == "BULLISH" and bearish:
                return candle

            if direction == "BEARISH" and bullish:
                return candle

        return None