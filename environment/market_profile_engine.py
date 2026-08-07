import pandas as pd


class MarketProfileEngine:

    def __init__(
        self,
        bins=50,
        value_area_percent=0.70
    ):
        self.bins = bins
        self.value_area_percent = value_area_percent

    def analyze(self, df: pd.DataFrame):
        """
        Build a volume-at-price approximation from OHLCV candles.

        Returns:
            {
                "poc": float,
                "vah": float,
                "val": float
            }
        """

        required_columns = {
            "high",
            "low",
            "tick_volume"
        }

        missing = required_columns - set(df.columns)

        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

        if df.empty:
            return {
                "poc": None,
                "vah": None,
                "val": None
            }

        data = df.copy()

        price_low = data["low"].min()
        price_high = data["high"].max()

        if price_high <= price_low:
            return {
                "poc": float(price_low),
                "vah": float(price_high),
                "val": float(price_low)
            }

        price_bins = pd.interval_range(
            start=price_low,
            end=price_high,
            periods=self.bins
        )

        profile = pd.Series(
            0.0,
            index=price_bins
        )

        for _, candle in data.iterrows():

            candle_low = candle["low"]
            candle_high = candle["high"]
            volume = candle["tick_volume"]

            if candle_high <= candle_low:
                continue

            candle_range = candle_high - candle_low

            for price_bin in price_bins:

                overlap_low = max(
                    candle_low,
                    price_bin.left
                )

                overlap_high = min(
                    candle_high,
                    price_bin.right
                )

                overlap = overlap_high - overlap_low

                if overlap <= 0:
                    continue

                volume_share = (
                    overlap / candle_range
                ) * volume

                profile.loc[price_bin] += volume_share

        if profile.sum() <= 0:
            return {
                "poc": None,
                "vah": None,
                "val": None
            }

        # Point of Control.
        poc_bin = profile.idxmax()

        poc = (
            poc_bin.left + poc_bin.right
        ) / 2

        # Target volume inside the value area.
        target_volume = (
            profile.sum()
            * self.value_area_percent
        )

        poc_position = profile.index.get_loc(
            poc_bin
        )

        lower = poc_position
        upper = poc_position
        accumulated_volume = profile.iloc[
            poc_position
        ]

        # Expand the value area from the POC,
        # always taking the side with greater volume.
        while accumulated_volume < target_volume:

            left_volume = (
                profile.iloc[lower - 1]
                if lower > 0
                else -1
            )

            right_volume = (
                profile.iloc[upper + 1]
                if upper < len(profile) - 1
                else -1
            )

            if left_volume < 0 and right_volume < 0:
                break

            if right_volume >= left_volume:

                upper += 1
                accumulated_volume += right_volume

            else:

                lower -= 1
                accumulated_volume += left_volume

        val_bin = profile.index[lower]
        vah_bin = profile.index[upper]

        val = val_bin.left
        vah = vah_bin.right

        return {
            "poc": float(poc),
            "vah": float(vah),
            "val": float(val)
        }