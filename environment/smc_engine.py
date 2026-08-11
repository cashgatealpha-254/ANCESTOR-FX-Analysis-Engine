import pandas as pd

from analysis.swings import detect_swings
from analysis.swing_structure import analyze_swing_structure
from analysis.mss import detect_mss


class SMCEngine:

    def __init__(
        self,
        swing_length=3
    ):

        self.swing_length = int(
            swing_length
        )

    # ==================================================
    # MAIN ANALYSIS
    # ==================================================

    def analyze(
        self,
        df: pd.DataFrame
    ):
        """
        Analyze market structure.

        Pipeline:

            OHLC
              ↓
            Swings
              ↓
            HH / HL / LH / LL
              ↓
            BOS / CHoCH
              ↓
            MSS

        Returns:
            {
                "swing_highs": [],
                "swing_lows": [],
                "structure": [],
                "structure_breaks": [],
                "mss": {...}
            }
        """

        required_columns = {
            "high",
            "low",
            "close"
        }

        missing = (
            required_columns
            - set(df.columns)
        )

        if missing:

            raise ValueError(
                f"Missing required columns: "
                f"{sorted(missing)}"
            )

        if len(df) < (
            self.swing_length * 2
        ) + 1:

            return {
                "swing_highs": [],
                "swing_lows": [],
                "structure": [],
                "structure_breaks": [],
                "mss": {
                    "status": "WAITING",
                    "mss": False,
                    "direction": "NEUTRAL",
                    "type": None,
                    "reason": "Insufficient data"
                }
            }

        # ==================================================
        # SWINGS
        # ==================================================

        swing_data = self._detect_swings(
            df
        )

        swing_highs = swing_data.get(
            "swing_highs",
            []
        )

        swing_lows = swing_data.get(
            "swing_lows",
            []
        )

        # ==================================================
        # STRUCTURE
        # ==================================================

        structure_data = (
            analyze_swing_structure(
                swing_highs,
                swing_lows
            )
        )

        structure = structure_data.get(
            "structure",
            []
        )

        # ==================================================
        # STRUCTURAL BIAS
        # ==================================================

        structure_bias = (
            self._get_structure_bias(
                swing_highs,
                swing_lows
            )
        )

        # ==================================================
        # STRUCTURE BREAKS
        # ==================================================

        structure_breaks = (
            self._detect_structure_breaks(
                df,
                swing_highs,
                swing_lows
            )
        )

        # ==================================================
        # CURRENT PRICE
        # ==================================================

        current_price = float(
            df["close"].iloc[-1]
        )

        # ==================================================
        # MSS
        # ==================================================

        mss = detect_mss(
         structure,
         current_price,
         previous_bias=structure_bias,
         structure_breaks=structure_breaks
        )

        # ==================================================
        # RETURN
        # ==================================================

        return {

            "swing_highs": swing_highs,

            "swing_lows": swing_lows,

            "structure": structure,

            "structure_bias": structure_bias,

            "structure_breaks":
                structure_breaks,

            "mss": mss
        }

    # ==================================================
    # SWING DETECTION
    # ==================================================

    def _detect_swings(
        self,
        df
    ):

        """
        Use the existing modular swing detector.

        The detector currently uses a fixed
        two-candle confirmation window.
        """

        return detect_swings(
            df
        )

    # ==================================================
    # STRUCTURE BREAKS
    # ==================================================

    def _detect_structure_breaks(
        self,
        data,
        swing_highs,
        swing_lows
    ):

        """
        Detect BOS and CHoCH using candle CLOSE.

        Existing behavior is preserved.
        """

        breaks = []

        if (
            not swing_highs
            or not swing_lows
        ):

            return breaks

        structure_bias = (
            self._get_structure_bias(
                swing_highs,
                swing_lows
            )
        )

        broken_high_indices = set()

        broken_low_indices = set()

        working_data = (
            data.copy()
            .reset_index(drop=False)
        )

        for i in range(
            len(working_data)
        ):

            candle = (
                working_data.iloc[i]
            )

            close = candle["close"]

            candle_index = (
                candle["index"]
            )

            previous_highs = [
                swing
                for swing in swing_highs
                if swing["index"]
                < candle_index
            ]

            previous_lows = [
                swing
                for swing in swing_lows
                if swing["index"]
                < candle_index
            ]

            if (
                not previous_highs
                or not previous_lows
            ):

                continue

            last_high = (
                previous_highs[-1]
            )

            last_low = (
                previous_lows[-1]
            )

            # ==========================================
            # BULLISH BREAK
            # ==========================================

            if (
                close
                > last_high["price"]
                and last_high["index"]
                not in broken_high_indices
            ):

                event_type = (
                    "BOS"
                    if structure_bias
                    == "BULLISH"
                    else "CHoCH"
                )

                breaks.append({

                    "type": event_type,

                    "direction":
                        "BULLISH",

                    "price":
                        float(
                            last_high["price"]
                        ),

                    "index":
                        candle_index,

                    "broken_swing_index":
                        last_high["index"]
                })

                broken_high_indices.add(
                    last_high["index"]
                )

                structure_bias = (
                    "BULLISH"
                )

            # ==========================================
            # BEARISH BREAK
            # ==========================================

            elif (
                close
                < last_low["price"]
                and last_low["index"]
                not in broken_low_indices
            ):

                event_type = (
                    "BOS"
                    if structure_bias
                    == "BEARISH"
                    else "CHoCH"
                )

                breaks.append({

                    "type": event_type,

                    "direction":
                        "BEARISH",

                    "price":
                        float(
                            last_low["price"]
                        ),

                    "index":
                        candle_index,

                    "broken_swing_index":
                        last_low["index"]
                })

                broken_low_indices.add(
                    last_low["index"]
                )

                structure_bias = (
                    "BEARISH"
                )

        return breaks

    # ==================================================
    # STRUCTURE BIAS
    # ==================================================

    @staticmethod
    def _get_structure_bias(
        swing_highs,
        swing_lows
    ):

        if (
            len(swing_highs) < 2
            or len(swing_lows) < 2
        ):

            return "NEUTRAL"

        latest_high = (
            swing_highs[-1]
        )

        previous_high = (
            swing_highs[-2]
        )

        latest_low = (
            swing_lows[-1]
        )

        previous_low = (
            swing_lows[-2]
        )

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

        if (
            higher_high
            and higher_low
        ):

            return "BULLISH"

        if (
            lower_high
            and lower_low
        ):

            return "BEARISH"

        return "NEUTRAL"