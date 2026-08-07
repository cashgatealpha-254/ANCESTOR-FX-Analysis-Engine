import pandas as pd


class SupplyDemandEngine:

    def __init__(
        self,
        base_candles=3,
        displacement_multiplier=1.5,
        max_zones=10
    ):
        self.base_candles = base_candles
        self.displacement_multiplier = displacement_multiplier
        self.max_zones = max_zones

    def analyze(self, df: pd.DataFrame):
        """
        Detect basic supply and demand zones from OHLC data.

        A zone is identified when a short consolidation/base is
        followed by a strong displacement candle.

        Returns:
            {
                "supply": [...],
                "demand": [...]
            }
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

        if len(df) < self.base_candles + 2:
            return {
                "supply": [],
                "demand": []
            }

        data = df.copy().reset_index(drop=False)

        data["range"] = data["high"] - data["low"]
        data["body"] = (data["close"] - data["open"]).abs()

        # Average recent candle range.
        data["average_range"] = (
            data["range"]
            .rolling(window=20, min_periods=5)
            .mean()
        )

        supply_zones = []
        demand_zones = []

        for i in range(self.base_candles, len(data)):

            displacement = data.iloc[i]

            if pd.isna(displacement["average_range"]):
                continue

            average_range = displacement["average_range"]

            if average_range <= 0:
                continue

            # Strong displacement condition.
            strong_displacement = (
                displacement["range"]
                >= average_range * self.displacement_multiplier
            )

            if not strong_displacement:
                continue

            # Candles immediately preceding displacement.
            base = data.iloc[
                i - self.base_candles:i
            ]

            if base["range"].mean() <= 0:
                continue

            base_high = base["high"].max()
            base_low = base["low"].min()

            base_body_ratio = (
                base["body"] / base["range"]
            ).mean()

            # Base should show relatively small bodies.
            is_base = base_body_ratio <= 0.55

            if not is_base:
                continue

            displacement_bullish = (
                displacement["close"] > displacement["open"]
            )

            displacement_bearish = (
                displacement["close"] < displacement["open"]
            )

            displacement_strength = (
                displacement["range"] / average_range
            )

            strength = self._classify_strength(
                displacement_strength
            )

            origin_index = data.iloc[
                i - self.base_candles
            ]["index"]

            zone = {
                "type": None,
                "low": float(base_low),
                "high": float(base_high),
                "strength": strength,
                "displacement_strength": round(
                    float(displacement_strength),
                    2
                ),
                "origin_index": origin_index
            }

            # Bullish displacement from a base → demand.
            if displacement_bullish:

                zone["type"] = "DEMAND"

                demand_zones.append(zone)

            # Bearish displacement from a base → supply.
            elif displacement_bearish:

                zone["type"] = "SUPPLY"

                supply_zones.append(zone)

        # Keep the most recent zones.
        demand_zones = demand_zones[-self.max_zones:]
        supply_zones = supply_zones[-self.max_zones:]

        return {
            "supply": supply_zones,
            "demand": demand_zones
        }

    @staticmethod
    def _classify_strength(displacement_strength):

        if displacement_strength >= 2.5:
            return "STRONG"

        if displacement_strength >= 2.0:
            return "MODERATE"

        return "WEAK"