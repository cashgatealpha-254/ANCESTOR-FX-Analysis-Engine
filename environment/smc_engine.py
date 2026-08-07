import pandas as pd


class SMCEngine:

    def __init__(self, swing_length=3):
        self.swing_length = swing_length

    def analyze(self, df: pd.DataFrame):
        """
        Analyze market structure using confirmed swing highs/lows.

        Returns:
            {
                "swing_highs": [...],
                "swing_lows": [...],
                "structure": [...],
                "structure_breaks": [...]
            }
        """

        required_columns = {
            "high",
            "low",
            "close"
        }

        missing = required_columns - set(df.columns)

        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

        if len(df) < (self.swing_length * 2) + 1:
            return {
                "swing_highs": [],
                "swing_lows": [],
                "structure": [],
                "structure_breaks": []
            }

        data = df.copy().reset_index(drop=False)

        swing_highs, swing_lows = self._detect_swings(data)

        structure = self._classify_structure(
            swing_highs,
            swing_lows
        )

        structure_breaks = self._detect_structure_breaks(
            data,
            swing_highs,
            swing_lows
        )

        return {
            "swing_highs": swing_highs,
            "swing_lows": swing_lows,
            "structure": structure,
            "structure_breaks": structure_breaks
        }

    def _detect_swings(self, data):
        swing_highs = []
        swing_lows = []

        length = self.swing_length

        for i in range(
            length,
            len(data) - length
        ):

            current_high = data.iloc[i]["high"]
            current_low = data.iloc[i]["low"]

            left_highs = data.iloc[
                i - length:i
            ]["high"]

            right_highs = data.iloc[
                i + 1:i + length + 1
            ]["high"]

            left_lows = data.iloc[
                i - length:i
            ]["low"]

            right_lows = data.iloc[
                i + 1:i + length + 1
            ]["low"]

            if (
                current_high > left_highs.max()
                and current_high > right_highs.max()
            ):
                swing_highs.append({
                    "type": "SWING_HIGH",
                    "price": float(current_high),
                    "index": data.iloc[i]["index"]
                })

            if (
                current_low < left_lows.min()
                and current_low < right_lows.min()
            ):
                swing_lows.append({
                    "type": "SWING_LOW",
                    "price": float(current_low),
                    "index": data.iloc[i]["index"]
                })

        return swing_highs, swing_lows

    @staticmethod
    def _classify_structure(
        swing_highs,
        swing_lows
    ):
        structure = []

        for i in range(1, len(swing_highs)):

            previous = swing_highs[i - 1]
            current = swing_highs[i]

            if current["price"] > previous["price"]:

                structure.append({
                    "type": "HH",
                    "price": current["price"],
                    "index": current["index"]
                })

            elif current["price"] < previous["price"]:

                structure.append({
                    "type": "LH",
                    "price": current["price"],
                    "index": current["index"]
                })

        for i in range(1, len(swing_lows)):

            previous = swing_lows[i - 1]
            current = swing_lows[i]

            if current["price"] > previous["price"]:

                structure.append({
                    "type": "HL",
                    "price": current["price"],
                    "index": current["index"]
                })

            elif current["price"] < previous["price"]:

                structure.append({
                    "type": "LL",
                    "price": current["price"],
                    "index": current["index"]
                })

        structure.sort(
            key=lambda item: item["index"]
        )

        return structure

    def _detect_structure_breaks(
        self,
        data,
        swing_highs,
        swing_lows
    ):
        """
        Detect structural breaks using candle CLOSE.

        A close above the latest confirmed swing high
        creates a bullish BOS/CHoCH.

        A close below the latest confirmed swing low
        creates a bearish BOS/CHoCH.
        """

        breaks = []

        if not swing_highs or not swing_lows:
            return breaks

        structure_bias = self._get_structure_bias(
            swing_highs,
            swing_lows
        )

        broken_high_indices = set()
        broken_low_indices = set()

        for i in range(len(data)):

            candle = data.iloc[i]

            close = candle["close"]
            candle_index = candle["index"]

            previous_highs = [
                swing
                for swing in swing_highs
                if swing["index"] < candle_index
            ]

            previous_lows = [
                swing
                for swing in swing_lows
                if swing["index"] < candle_index
            ]

            if not previous_highs or not previous_lows:
                continue

            last_high = previous_highs[-1]
            last_low = previous_lows[-1]

            # ---------------------------------
            # Bullish structural break
            # ---------------------------------

            if (
                close > last_high["price"]
                and last_high["index"]
                not in broken_high_indices
            ):

                event_type = (
                    "BOS"
                    if structure_bias == "BULLISH"
                    else "CHoCH"
                )

                breaks.append({
                    "type": event_type,
                    "direction": "BULLISH",
                    "price": float(last_high["price"]),
                    "index": candle_index,
                    "broken_swing_index": last_high["index"]
                })

                broken_high_indices.add(
                    last_high["index"]
                )

                structure_bias = "BULLISH"

            # ---------------------------------
            # Bearish structural break
            # ---------------------------------

            elif (
                close < last_low["price"]
                and last_low["index"]
                not in broken_low_indices
            ):

                event_type = (
                    "BOS"
                    if structure_bias == "BEARISH"
                    else "CHoCH"
                )

                breaks.append({
                    "type": event_type,
                    "direction": "BEARISH",
                    "price": float(last_low["price"]),
                    "index": candle_index,
                    "broken_swing_index": last_low["index"]
                })

                broken_low_indices.add(
                    last_low["index"]
                )

                structure_bias = "BEARISH"

        return breaks

    @staticmethod
    def _get_structure_bias(
        swing_highs,
        swing_lows
    ):
        """
        Determine directional bias from the
        latest swing relationships.
        """

        if (
            len(swing_highs) < 2
            or len(swing_lows) < 2
        ):
            return "NEUTRAL"

        latest_high = swing_highs[-1]
        previous_high = swing_highs[-2]

        latest_low = swing_lows[-1]
        previous_low = swing_lows[-2]

        higher_high = (
            latest_high["price"]
            > previous_high["price"]
        )

        higher_low = (
            latest_low["price"]
            > previous_low["price"]
        )

        lower_high = (
            latest_high["price"]
            < previous_high["price"]
        )

        lower_low = (
            latest_low["price"]
            < previous_low["price"]
        )

        if higher_high and higher_low:
            return "BULLISH"

        if lower_high and lower_low:
            return "BEARISH"

        return "NEUTRAL"