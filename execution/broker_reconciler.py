import MetaTrader5 as mt5


class BrokerReconciler:

    # ==================================================
    # FIND MATCHING POSITION
    # ==================================================

    def find_position(
        self,
        symbol,
        trade_id=None,
        magic=None
    ):

        positions = mt5.positions_get(
            symbol=symbol
        )

        if positions is None:

            return {
                "status": "UNKNOWN",
                "symbol": symbol,
                "reason": (
                    "Unable to retrieve "
                    "MT5 positions"
                )
            }

        for position in positions:

            # ------------------------------------------
            # Magic-number matching
            # ------------------------------------------

            if magic is not None:

                try:

                    if int(
                        position.magic
                    ) != int(magic):

                        continue

                except (
                    TypeError,
                    ValueError
                ):

                    continue

            # ------------------------------------------
            # Comment / trade-id matching
            # ------------------------------------------

            if trade_id:

                comment = str(
                    getattr(
                        position,
                        "comment",
                        ""
                    )
                )

                if trade_id not in comment:

                    continue

            return {

                "status": "FOUND",

                "symbol": symbol,

                "ticket": position.ticket,

                "volume": position.volume,

                "price_open": position.price_open,

                "price_current": position.price_current,

                "stop_loss": position.sl,

                "take_profit": position.tp,

                "type": position.type,

                "magic": position.magic,

                "comment": position.comment
            }

        return {

            "status": "NOT_FOUND",

            "symbol": symbol,

            "reason": (
                "No matching broker position found"
            )
        }

    # ==================================================
    # FIND MATCHING ORDER
    # ==================================================

    def find_order(
        self,
        symbol,
        trade_id=None,
        magic=None
    ):

        orders = mt5.orders_get(
            symbol=symbol
        )

        if orders is None:

            return {

                "status": "UNKNOWN",

                "symbol": symbol,

                "reason": (
                    "Unable to retrieve "
                    "MT5 orders"
                )
            }

        for order in orders:

            # ------------------------------------------
            # Magic-number matching
            # ------------------------------------------

            if magic is not None:

                try:

                    if int(
                        order.magic
                    ) != int(magic):

                        continue

                except (
                    TypeError,
                    ValueError
                ):

                    continue

            # ------------------------------------------
            # Comment / trade-id matching
            # ------------------------------------------

            if trade_id:

                comment = str(
                    getattr(
                        order,
                        "comment",
                        ""
                    )
                )

                if trade_id not in comment:

                    continue

            return {

                "status": "FOUND",

                "symbol": symbol,

                "ticket": order.ticket,

                "volume": order.volume_initial,

                "price_open": order.price_open,

                "stop_loss": order.sl,

                "take_profit": order.tp,

                "type": order.type,

                "magic": order.magic,

                "comment": order.comment
            }

        return {

            "status": "NOT_FOUND",

            "symbol": symbol,

            "reason": (
                "No matching broker order found"
            )
        }

    # ==================================================
    # RECONCILE
    # ==================================================

    def reconcile(
        self,
        symbol,
        trade_id=None,
        magic=None
    ):

        if not symbol:

            return {

                "status": "ERROR",

                "reason": "Missing symbol"
            }

        # ------------------------------------------
        # Check open position first
        # ------------------------------------------

        position = self.find_position(
            symbol=symbol,
            trade_id=trade_id,
            magic=magic
        )

        if position.get(
            "status"
        ) == "FOUND":

            return {

                "status": "FILLED",

                "symbol": symbol,

                "source": "POSITION",

                "trade": position
            }

        if position.get(
            "status"
        ) == "UNKNOWN":

            return position

        # ------------------------------------------
        # Check pending orders
        # ------------------------------------------

        order = self.find_order(
            symbol=symbol,
            trade_id=trade_id,
            magic=magic
        )

        if order.get(
            "status"
        ) == "FOUND":

            return {

                "status": "PENDING",

                "symbol": symbol,

                "source": "ORDER",

                "trade": order
            }

        if order.get(
            "status"
        ) == "UNKNOWN":

            return order

        # ------------------------------------------
        # Nothing found
        # ------------------------------------------

        return {

            "status": "NOT_FOUND",

            "symbol": symbol,

            "reason": (
                "No matching position or "
                "pending order found"
            )
        }