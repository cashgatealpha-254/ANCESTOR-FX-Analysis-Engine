import MetaTrader5 as mt5


class PositionSizer:

    def __init__(
        self,
        risk_percent=1.0,
        minimum_lot=None,
        maximum_lot=None
    ):

        self.risk_percent = float(
            risk_percent
        )

        self.minimum_lot = minimum_lot
        self.maximum_lot = maximum_lot

    # ==================================================
    # CALCULATE POSITION SIZE
    # ==================================================

    def calculate(
        self,
        setup
    ):

        if not isinstance(
            setup,
            dict
        ):

            return {
                "status": "ERROR",
                "reason": "Invalid setup"
            }

        if setup.get(
            "status"
        ) != "ALLOW":

            return {
                "status": "BLOCKED",
                "reason": "Risk engine did not allow trade"
            }

        symbol = setup.get(
            "symbol"
        )

        entry = setup.get(
            "entry"
        )

        stop_loss = setup.get(
            "stop_loss"
        )

        money_at_risk = setup.get(
            "money_at_risk"
        )

        if not symbol:

            return {
                "status": "ERROR",
                "reason": "Missing symbol"
            }

        if (
            entry is None
            or stop_loss is None
            or money_at_risk is None
        ):

            return {
                "status": "ERROR",
                "symbol": symbol,
                "reason": (
                    "Incomplete position-sizing data"
                )
            }

        try:

            entry = float(entry)
            stop_loss = float(stop_loss)
            money_at_risk = float(
                money_at_risk
            )

        except (
            TypeError,
            ValueError
        ):

            return {
                "status": "ERROR",
                "symbol": symbol,
                "reason": (
                    "Invalid position-sizing values"
                )
            }

        if money_at_risk <= 0:

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": "Invalid money at risk"
            }

        # ==================================================
        # SYMBOL INFORMATION
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

        # ==================================================
        # TICK INFORMATION
        # ==================================================

        tick_size = float(
            symbol_info.trade_tick_size
        )

        tick_value = float(
            symbol_info.trade_tick_value
        )

        if tick_size <= 0:

            return {
                "status": "ERROR",
                "symbol": symbol,
                "reason": (
                    "Invalid trade tick size"
                )
            }

        if tick_value <= 0:

            return {
                "status": "ERROR",
                "symbol": symbol,
                "reason": (
                    "Invalid trade tick value"
                )
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
                    "Invalid stop-loss distance"
                )
            }

        # ==================================================
        # TICKS TO STOP
        # ==================================================

        stop_ticks = (
            stop_distance
            / tick_size
        )

        if stop_ticks <= 0:

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": (
                    "Invalid stop distance in ticks"
                )
            }

        # ==================================================
        # RISK PER ONE LOT
        # ==================================================

        risk_per_lot = (
            stop_ticks
            * tick_value
        )

        if risk_per_lot <= 0:

            return {
                "status": "ERROR",
                "symbol": symbol,
                "reason": (
                    "Invalid calculated risk per lot"
                )
            }

        # ==================================================
        # RAW LOT SIZE
        # ==================================================

        raw_volume = (
            money_at_risk
            / risk_per_lot
        )

        # ==================================================
        # BROKER VOLUME RULES
        # ==================================================

        volume_min = float(
            symbol_info.volume_min
        )

        volume_max = float(
            symbol_info.volume_max
        )

        volume_step = float(
            symbol_info.volume_step
        )

        if volume_min <= 0:

            return {
                "status": "ERROR",
                "symbol": symbol,
                "reason": (
                    "Invalid broker minimum volume"
                )
            }

        if volume_max <= 0:

            return {
                "status": "ERROR",
                "symbol": symbol,
                "reason": (
                    "Invalid broker maximum volume"
                )
            }

        if volume_step <= 0:

            return {
                "status": "ERROR",
                "symbol": symbol,
                "reason": (
                    "Invalid broker volume step"
                )
            }

        # ==================================================
        # APPLY ENGINE LIMITS
        # ==================================================

        minimum_lot = volume_min

        maximum_lot = volume_max

        if self.minimum_lot is not None:

            minimum_lot = max(
                minimum_lot,
                float(self.minimum_lot)
            )

        if self.maximum_lot is not None:

            maximum_lot = min(
                maximum_lot,
                float(self.maximum_lot)
            )

        if minimum_lot > maximum_lot:

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": (
                    "Configured lot limits "
                    "are incompatible with broker limits"
                )
            }

        # ==================================================
        # ROUND DOWN
        # ==================================================

        volume = (
            int(
                raw_volume
                / volume_step
            )
            * volume_step
        )

        # Avoid accidentally exceeding risk
        # through upward rounding.

        if volume < minimum_lot:

            return {

                "status": "BLOCKED",

                "symbol": symbol,

                "reason": (
                    "Calculated volume is below "
                    "broker minimum"
                ),

                "raw_volume": raw_volume,

                "broker_minimum": volume_min
            }

        volume = min(
            volume,
            maximum_lot
        )

        # ==================================================
        # NORMALIZE DECIMAL PLACES
        # ==================================================

        volume = round(
            volume,
            8
        )

        # ==================================================
        # ACTUAL ESTIMATED RISK
        # ==================================================

        actual_risk = (
            risk_per_lot
            * volume
        )

        actual_risk_percent = (
            actual_risk
            / float(
                setup.get(
                    "equity",
                    0
                )
            )
            * 100
            if float(
                setup.get(
                    "equity",
                    0
                )
            ) > 0
            else None
        )

        # ==================================================
        # RESULT
        # ==================================================

        return {

            "status": "READY",

            "symbol": symbol,

            "volume": volume,

            "risk_percent": (
                self.risk_percent
            ),

            "money_at_risk": (
                money_at_risk
            ),

            "actual_risk": round(
                actual_risk,
                2
            ),

            "actual_risk_percent": (
                round(
                    actual_risk_percent,
                    4
                )
                if actual_risk_percent
                is not None
                else None
            ),

            "entry": entry,

            "stop_loss": stop_loss,

            "stop_distance": (
                stop_distance
            ),

            "stop_ticks": (
                stop_ticks
            ),

            "risk_per_lot": (
                risk_per_lot
            ),

            "tick_size": tick_size,

            "tick_value": tick_value,

            "volume_min": volume_min,

            "volume_max": volume_max,

            "volume_step": volume_step
        }