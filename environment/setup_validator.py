class SetupValidator:

    def __init__(
        self,
        minimum_rr=2.0,
        minimum_zone_ticks=2.0,
        minimum_stop_ticks=2.0
    ):

        self.minimum_rr = float(
            minimum_rr
        )

        self.minimum_zone_ticks = float(
            minimum_zone_ticks
        )

        self.minimum_stop_ticks = float(
            minimum_stop_ticks
        )

    # ==================================================
    # VALIDATE SETUP
    # ==================================================

    def validate(
        self,
        setup,
        symbol_info=None,
        current_price=None
    ):

        if not isinstance(
            setup,
            dict
        ):

            return {
                "status": "REJECTED",
                "reason": "Invalid setup"
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

        entry = self._to_float(
            setup.get("entry")
        )

        stop_loss = self._to_float(
            setup.get("stop_loss")
        )

        take_profit = self._to_float(
            setup.get("take_profit")
        )

        zone = setup.get(
            "zone"
        )

        trigger = str(
            setup.get(
                "trigger",
                ""
            )
        ).upper()

        # ==================================================
        # BASIC DATA
        # ==================================================

        if not symbol:

            return self._rejected(
                "Missing symbol"
            )

        if direction not in {
            "BULLISH",
            "BEARISH"
        }:

            return self._rejected(
                "Invalid direction"
            )

        if entry is None:

            return self._rejected(
                "Missing entry"
            )

        if stop_loss is None:

            return self._rejected(
                "Missing stop loss"
            )

        if take_profit is None:

            return self._rejected(
                "Missing take profit"
            )

        # ==================================================
        # DIRECTION / PRICE STRUCTURE
        # ==================================================

        if direction == "BULLISH":

            if not (
                stop_loss < entry < take_profit
            ):

                return self._rejected(
                    "Invalid bullish price structure"
                )

        else:

            if not (
                take_profit < entry < stop_loss
            ):

                return self._rejected(
                    "Invalid bearish price structure"
                )

        # ==================================================
        # RISK / REWARD
        # ==================================================

        risk_distance = abs(
            entry - stop_loss
        )

        reward_distance = abs(
            take_profit - entry
        )

        if risk_distance <= 0:

            return self._rejected(
                "Zero risk distance"
            )

        rr = (
            reward_distance
            / risk_distance
        )

        if rr < self.minimum_rr:

            return self._rejected(
                f"RR {rr:.2f} below "
                f"minimum {self.minimum_rr:.2f}"
            )

        # ==================================================
        # SYMBOL PRECISION
        # ==================================================

        tick_size = None

        if symbol_info is not None:

            tick_size = self._to_float(
                getattr(
                    symbol_info,
                    "trade_tick_size",
                    None
                )
            )

            if tick_size is None:

                tick_size = self._to_float(
                    getattr(
                        symbol_info,
                        "point",
                        None
                    )
                )

        # ==================================================
        # STOP DISTANCE
        # ==================================================

        stop_ticks = None

        if tick_size is not None:

            if tick_size <= 0:

                return self._rejected(
                    "Invalid tick size"
                )

            stop_ticks = (
                risk_distance
                / tick_size
            )

            if (
                stop_ticks
                < self.minimum_stop_ticks
            ):

                return self._rejected(
                    "Stop distance is too small"
                )

        # ==================================================
        # ZONE VALIDATION
        # ==================================================

        zone_width = None
        zone_ticks = None

        if not isinstance(
            zone,
            dict
        ):

            return self._rejected(
                "Missing entry zone"
            )

        zone_low = self._to_float(
            zone.get("low")
        )

        zone_high = self._to_float(
            zone.get("high")
        )

        if (
            zone_low is None
            or zone_high is None
        ):

            return self._rejected(
                "Entry zone has no valid boundaries"
            )

        if zone_low > zone_high:

            zone_low, zone_high = (
                zone_high,
                zone_low
            )

        zone_width = (
            zone_high
            - zone_low
        )

        if zone_width <= 0:

            return self._rejected(
                "Entry zone has zero width"
            )

        if tick_size is not None:

            zone_ticks = (
                zone_width
                / tick_size
            )

            if (
                zone_ticks
                < self.minimum_zone_ticks
            ):

                return self._rejected(
                    "Entry zone is too narrow"
                )

        # ==================================================
        # CURRENT PRICE
        # ==================================================

        if current_price is None:

            current_price = setup.get(
                "current_price"
            )

        current_price = self._to_float(
            current_price
        )

        # ==================================================
        # TRIGGER STATE
        # ==================================================

        if current_price is not None:

            if (
                zone_low
                <= current_price
                <= zone_high
            ):

                trigger_state = (
                    "ENTRY_NOW"
                )

            elif current_price > zone_high:

                if direction == "BULLISH":

                    trigger_state = (
                        "WAITING_FOR_RETRACE"
                    )

                else:

                    trigger_state = (
                        "ZONE_INVALIDATED"
                    )

            else:

                if direction == "BEARISH":

                    trigger_state = (
                        "WAITING_FOR_RETRACE"
                    )

                else:

                    trigger_state = (
                        "ZONE_INVALIDATED"
                    )

        else:

            trigger_state = trigger or (
                "WAITING_FOR_PRICE"
            )

        # ==================================================
        # INVALIDATED
        # ==================================================

        if trigger_state == "ZONE_INVALIDATED":

            return {

                "status": "REJECTED",

                "symbol": symbol,

                "direction": direction,

                "entry": entry,

                "stop_loss": stop_loss,

                "take_profit": take_profit,

                "rr": round(
                    rr,
                    2
                ),

                "trigger": trigger_state,

                "zone_low": zone_low,

                "zone_high": zone_high,

                "reason": (
                    "Price has moved through "
                    "the entry zone"
                )
            }

        # ==================================================
        # WAITING
        # ==================================================

        if trigger_state != "ENTRY_NOW":

            return {

                "status": "WAITING",

                "symbol": symbol,

                "direction": direction,

                "entry": entry,

                "stop_loss": stop_loss,

                "take_profit": take_profit,

                "rr": round(
                    rr,
                    2
                ),

                "trigger": trigger_state,

                "current_price": current_price,

                "zone_low": zone_low,

                "zone_high": zone_high,

                "zone_width": zone_width,

                "zone_width_ticks": (
                    round(
                        zone_ticks,
                        4
                    )
                    if zone_ticks is not None
                    else None
                ),

                "stop_distance": risk_distance,

                "stop_distance_ticks": (
                    round(
                        stop_ticks,
                        4
                    )
                    if stop_ticks is not None
                    else None
                ),

                "reason": (
                    trigger_state
                )
            }

        # ==================================================
        # READY
        # ==================================================

        return {

            "status": "READY",

            "symbol": symbol,

            "direction": direction,

            "entry": entry,

            "stop_loss": stop_loss,

            "take_profit": take_profit,

            "rr": round(
                rr,
                2
            ),

            "trigger": "ENTRY_NOW",

            "current_price": current_price,

            "zone_low": zone_low,

            "zone_high": zone_high,

            "zone_width": zone_width,

            "zone_width_ticks": (
                round(
                    zone_ticks,
                    4
                )
                if zone_ticks is not None
                else None
            ),

            "stop_distance": risk_distance,

            "stop_distance_ticks": (
                round(
                    stop_ticks,
                    4
                )
                if stop_ticks is not None
                else None
            ),

            "reason": (
                "Setup passed structural validation"
            )
        }

    # ==================================================
    # HELPERS
    # ==================================================

    @staticmethod
    def _to_float(
        value
    ):

        if value is None:

            return None

        try:

            return float(
                value
            )

        except (
            TypeError,
            ValueError
        ):

            return None

    # ==================================================
    # REJECTION
    # ==================================================

    @staticmethod
    def _rejected(
        reason
    ):

        return {

            "status": "REJECTED",

            "reason": reason
        }