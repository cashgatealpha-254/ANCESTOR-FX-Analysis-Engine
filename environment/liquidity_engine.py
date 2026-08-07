import pandas as pd


class LiquidityEngine:

    def __init__(self, tolerance=0.0003):
        """
        tolerance:
            Relative price tolerance used to identify
            approximately equal highs/lows.

            Example:
            0.0003 = 0.03%
        """
        self.tolerance = tolerance

    def analyze(self, df: pd.DataFrame):

        required_columns = {
            "high",
            "low"
        }

        missing = required_columns - set(df.columns)

        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

        if df.empty:
            return {
                "buy_side": [],
                "sell_side": []
            }

        data = df.copy().reset_index(drop=False)

        buy_side = []
        sell_side = []

        # -----------------------------
        # Previous highs/lows
        # -----------------------------

        for i in range(len(data)):

            buy_side.append({
                "type": "SWING_HIGH_LIQUIDITY",
                "price": float(data.iloc[i]["high"]),
                "index": data.iloc[i]["index"]
            })

            sell_side.append({
                "type": "SWING_LOW_LIQUIDITY",
                "price": float(data.iloc[i]["low"]),
                "index": data.iloc[i]["index"]
            })

        # -----------------------------
        # Equal highs
        # -----------------------------

        for i in range(len(data)):

            current_high = data.iloc[i]["high"]

            for j in range(i + 1, len(data)):

                next_high = data.iloc[j]["high"]

                if self._approximately_equal(
                    current_high,
                    next_high
                ):

                    price = (
                        current_high + next_high
                    ) / 2

                    buy_side.append({
                        "type": "EQUAL_HIGH",
                        "price": float(price),
                        "index": data.iloc[j]["index"],
                        "reference_index": data.iloc[i]["index"]
                    })

        # -----------------------------
        # Equal lows
        # -----------------------------

        for i in range(len(data)):

            current_low = data.iloc[i]["low"]

            for j in range(i + 1, len(data)):

                next_low = data.iloc[j]["low"]

                if self._approximately_equal(
                    current_low,
                    next_low
                ):

                    price = (
                        current_low + next_low
                    ) / 2

                    sell_side.append({
                        "type": "EQUAL_LOW",
                        "price": float(price),
                        "index": data.iloc[j]["index"],
                        "reference_index": data.iloc[i]["index"]
                    })

        return {
            "buy_side": buy_side,
            "sell_side": sell_side
        }

    def _approximately_equal(
        self,
        price_a,
        price_b
    ):

        if price_a == 0:
            return False

        difference = abs(
            price_a - price_b
        )

        relative_difference = (
            difference / abs(price_a)
        )

        return (
            relative_difference
            <= self.tolerance
        )