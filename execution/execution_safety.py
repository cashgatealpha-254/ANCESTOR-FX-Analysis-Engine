import MetaTrader5 as mt5


class ExecutionSafety:

    def __init__(
        self,
        max_spread_points=30
    ):

        self.max_spread_points = int(
            max_spread_points
        )

    # ==================================================
    # CHECK
    # ==================================================

    def check(
        self,
        validation
    ):

        if not isinstance(
            validation,
            dict
        ):

            return self._blocked(
                "Invalid validation data"
            )

        if validation.get(
            "status"
        ) != "ALLOW":

            return self._blocked(
                "Order validation did not allow trade"
            )

        symbol = validation.get(
            "symbol"
        )

        direction = str(
            validation.get(
                "direction",
                ""
            )
        ).upper()

        volume = validation.get(
            "volume"
        )

        execution_price = validation.get(
            "execution_price"
        )

        stop_loss = validation.get(
            "stop_loss"
        )

        take_profit = validation.get(
            "take_profit"
        )

        if not symbol:

            return self._blocked(
                "Missing symbol"
            )

        if direction not in {
            "BULLISH",
            "BEARISH"
        }:

            return self._blocked(
                "Invalid direction"
            )

        # ==================================================
        # SYMBOL
        # ==================================================

        symbol_info = mt5.symbol_info(
            symbol
        )

        if symbol_info is None:

            return self._blocked(
                "Symbol information unavailable"
            )

        # ==================================================
        # SYMBOL VISIBILITY
        # ==================================================

        if not symbol_info.visible:

            selected = mt5.symbol_select(
                symbol,
                True
            )

            if not selected:

                return self._blocked(
                    "Unable to select symbol"
                )

            symbol_info = mt5.symbol_info(
                symbol
            )

            if symbol_info is None:

                return self._blocked(
                    "Symbol unavailable after selection"
                )

        # ==================================================
        # TRADING MODE
        # ==================================================

        trade_mode = getattr(
            symbol_info,
            "trade_mode",
            None
        )

        if trade_mode == (
            mt5.SYMBOL_TRADE_MODE_DISABLED
        ):

            return self._blocked(
                "Symbol trading is disabled"
            )

        # ==================================================
        # VOLUME
        # ==================================================

        try:

            volume = float(
                volume
            )

        except (
            TypeError,
            ValueError
        ):

            return self._blocked(
                "Invalid volume"
            )

        if volume <= 0:

            return self._blocked(
                "Volume must be greater than zero"
            )

        volume_min = float(
            symbol_info.volume_min
        )

        volume_max = float(
            symbol_info.volume_max
        )

        volume_step = float(
            symbol_info.volume_step
        )

        if volume < volume_min:

            return self._blocked(
                "Volume below broker minimum"
            )

        if volume > volume_max:

            return self._blocked(
                "Volume above broker maximum"
            )

        # ==================================================
        # VOLUME STEP
        # ==================================================

        steps = round(
            volume / volume_step
        )

        normalized_volume = (
            steps * volume_step
        )

        if abs(
            normalized_volume - volume
        ) > 1e-8:

            return self._blocked(
                "Volume does not match broker volume step"
            )

        # ==================================================
        # LIVE TICK
        # ==================================================

        tick = mt5.symbol_info_tick(
            symbol
        )

        if tick is None:

            return self._blocked(
                "Live tick unavailable"
            )

        bid = float(
            tick.bid
        )

        ask = float(
            tick.ask
        )

        if bid <= 0 or ask <= 0:

            return self._blocked(
                "Invalid bid/ask"
            )

        # ==================================================
        # SPREAD
        # ==================================================

        point = float(
            symbol_info.point
        )

        if point <= 0:

            return self._blocked(
                "Invalid symbol point"
            )

        spread_points = (
            ask - bid
        ) / point

        if (
            spread_points
            > self.max_spread_points
        ):

            return self._blocked(
                "Spread exceeds execution limit"
            )

        # ==================================================
        # EXECUTION PRICE
        # ==================================================

        try:

            execution_price = float(
                execution_price
            )

            stop_loss = float(
                stop_loss
            )

            take_profit = float(
                take_profit
            )

        except (
            TypeError,
            ValueError
        ):

            return self._blocked(
                "Invalid execution levels"
            )

        # ==================================================
        # STOP DISTANCE
        # ==================================================

        stops_level = float(
            getattr(
                symbol_info,
                "trade_stops_level",
                0
            )
        )

        freeze_level = float(
            getattr(
                symbol_info,
                "trade_freeze_level",
                0
            )
        )

        minimum_distance = max(
            stops_level,
            freeze_level
        ) * point

        # ==================================================
        # SL / TP DISTANCE
        # ==================================================

        sl_distance = abs(
            execution_price - stop_loss
        )

        tp_distance = abs(
            take_profit - execution_price
        )

        if (
            minimum_distance > 0
            and sl_distance < minimum_distance
        ):

            return self._blocked(
                "Stop loss violates broker stop/freeze level"
            )

        if (
            minimum_distance > 0
            and tp_distance < minimum_distance
        ):

            return self._blocked(
                "Take profit violates broker stop/freeze level"
            )

        # ==================================================
        # RESULT
        # ==================================================

        return {

            "status": "ALLOW",

            "symbol": symbol,

            "direction": direction,

            "volume": normalized_volume,

            "execution_price": execution_price,

            "stop_loss": stop_loss,

            "take_profit": take_profit,

            "bid": bid,

            "ask": ask,

            "spread_points": round(
                spread_points,
                2
            ),

            "minimum_distance": (
                minimum_distance
            ),

            "stops_level": stops_level,

            "freeze_level": freeze_level
        }

    # ==================================================
    # BLOCK
    # ==================================================

    @staticmethod
    def _blocked(reason):

        return {

            "status": "BLOCKED",

            "reason": reason
        }