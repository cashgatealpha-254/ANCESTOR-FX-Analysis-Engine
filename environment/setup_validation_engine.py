import MetaTrader5 as mt5


class SetupValidationEngine:

    def __init__(
        self,
        minimum_stop_ticks=2
    ):

        self.minimum_stop_ticks = float(
            minimum_stop_ticks
        )

    # ==================================================
    # VALIDATE SETUP
    # ==================================================

    def validate(
        self,
        setup
    ):

        if not isinstance(
            setup,
            dict
        ):

            return {
                "status": "BLOCKED",
                "reason": "Invalid setup"
            }

        # ==================================================
        # BASIC STATE
        # ==================================================

        setup_status = str(
            setup.get(
                "status",
                ""
            )
        ).upper()

        if setup_status != "READY":

            return {
                "status": "BLOCKED",
                "reason": (
                    "Setup is not READY"
                )
            }

        symbol = setup.get(
            "symbol"
        )

        direction = str(
            setup.get(
                "direction",
                ""
            )
        ).upper()

        entry = setup.get(
            "entry"
        )

        stop_loss = setup.get(
            "stop_loss"
        )

        take_profit = setup.get(
            "take_profit"
        )

        # ==================================================
        # REQUIRED DATA
        # ==================================================

        if not symbol:

            return {
                "status": "BLOCKED",
                "reason": "Missing symbol"
            }

        if direction not in {
            "BULLISH",
            "BEARISH"
        }:

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": "Invalid direction"
            }

        if (
            entry is None
            or stop_loss is None
            or take_profit is None
        ):

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": (
                    "Incomplete trade levels"
                )
            }

        try:

            entry = float(entry)
            stop_loss = float(stop_loss)
            take_profit = float(take_profit)

        except (
            TypeError,
            ValueError
        ):

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": (
                    "Invalid trade levels"
                )
            }

        # ==================================================
        # MARKET STRUCTURE OF TRADE
        # ==================================================

        if direction == "BULLISH":

            if not (
                stop_loss < entry < take_profit
            ):

                return {
                    "status": "BLOCKED",
                    "symbol": symbol,
                    "direction": direction,
                    "reason": (
                        "Invalid bullish "
                        "entry/SL/TP structure"
                    )
                }

        else:

            if not (
                take_profit < entry < stop_loss
            ):

                return {
                    "status": "BLOCKED",
                    "symbol": symbol,
                    "direction": direction,
                    "reason": (
                        "Invalid bearish "
                        "entry/SL/TP structure"
                    )
                }

        # ==================================================
        # MT5 SYMBOL INFORMATION
        # ==================================================

        symbol_info = mt5.symbol_info(
            symbol
        )

        if symbol_info is None:

            return {
                "status": "ERROR",
                "symbol": symbol,
                "reason": (
                    "Symbol information unavailable"
                )
            }

        point = float(
            symbol_info.point
        )

        tick_size = float(
            symbol_info.trade_tick_size
        )

        if point <= 0:

            return {
                "status": "ERROR",
                "symbol": symbol,
                "reason": "Invalid symbol point"
            }

        if tick_size <= 0:

            return {
                "status": "ERROR",
                "symbol": symbol,
                "reason": "Invalid trade tick size"
            }

        # ==================================================
        # STOP DISTANCE
        # ==================================================

        stop_distance = abs(
            entry - stop_loss
        )

        if stop_distance <= 0:

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": (
                    "Zero stop-loss distance"
                )
            }

        # ==================================================
        # POINT / TICK DISTANCE
        # ==================================================

        stop_points = (
            stop_distance
            / point
        )

        stop_ticks = (
            stop_distance
            / tick_size
        )

        # ==================================================
        # MINIMUM STOP DISTANCE
        # ==================================================

        if stop_ticks < self.minimum_stop_ticks:

            return {
                "status": "BLOCKED",

                "symbol": symbol,

                "direction": direction,

                "entry": entry,

                "stop_loss": stop_loss,

                "take_profit": take_profit,

                "stop_distance": stop_distance,

                "stop_points": stop_points,

                "stop_ticks": stop_ticks,

                "minimum_stop_ticks": (
                    self.minimum_stop_ticks
                ),

                "reason": (
                    "Stop distance below "
                    "minimum allowed ticks"
                )
            }

        # ==================================================
        # RESULT
        # ==================================================

        return {

            "status": "VALID",

            "symbol": symbol,

            "direction": direction,

            "entry": entry,

            "stop_loss": stop_loss,

            "take_profit": take_profit,

            "stop_distance": stop_distance,

            "stop_points": stop_points,

            "stop_ticks": stop_ticks,

            "minimum_stop_ticks": (
                self.minimum_stop_ticks
            ),

            "point": point,

            "tick_size": tick_size,

            "reason": (
                "Setup passed structural "
                "and stop-distance validation"
            )
        }