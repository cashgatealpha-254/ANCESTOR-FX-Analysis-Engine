import MetaTrader5 as mt5


class OrderValidator:

    def __init__(
        self,
        max_deviation_points=20
    ):

        self.max_deviation_points = int(
            max_deviation_points
        )

    # ==================================================
    # VALIDATE ORDER
    # ==================================================

    def validate(
        self,
        setup,
        position
    ):

        if not isinstance(setup, dict):

            return self._blocked(
                "Invalid setup"
            )

        if not isinstance(position, dict):

            return self._blocked(
                "Invalid position sizing"
            )

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

        volume = position.get(
            "volume"
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

        try:

            entry = float(entry)
            stop_loss = float(stop_loss)
            take_profit = float(take_profit)
            volume = float(volume)

        except (
            TypeError,
            ValueError
        ):

            return self._blocked(
                "Invalid order values"
            )

        if volume <= 0:

            return self._blocked(
                "Invalid volume"
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
                "Invalid live bid/ask"
            )

        # ==================================================
        # EXECUTION PRICE
        # ==================================================

        if direction == "BULLISH":

            execution_price = ask

        else:

            execution_price = bid

        # ==================================================
        # PRICE DISTANCE
        # ==================================================

        point = float(
            symbol_info.point
        )

        if point <= 0:

            return self._blocked(
                "Invalid symbol point"
            )

        deviation = abs(
            execution_price - entry
        ) / point

        if (
            deviation
            > self.max_deviation_points
        ):

            return self._blocked(
                "Market moved beyond allowed deviation"
            )

        # ==================================================
        # LEVEL STRUCTURE
        # ==================================================

        if direction == "BULLISH":

            if not (
                stop_loss
                < execution_price
                < take_profit
            ):

                return self._blocked(
                    "Invalid bullish live order structure"
                )

        else:

            if not (
                take_profit
                < execution_price
                < stop_loss
            ):

                return self._blocked(
                    "Invalid bearish live order structure"
                )

        # ==================================================
        # RESULT
        # ==================================================

        return {

            "status": "ALLOW",

            "symbol": symbol,

            "direction": direction,

            "requested_entry": entry,

            "execution_price": (
                execution_price
            ),

            "stop_loss": stop_loss,

            "take_profit": take_profit,

            "volume": volume,

            "bid": bid,

            "ask": ask,

            "deviation_points": round(
                deviation,
                2
            ),

            "max_deviation_points": (
                self.max_deviation_points
            )
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