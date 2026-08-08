import MetaTrader5 as mt5


class ExecutionEngine:

    def __init__(
        self,
        max_positions=1,
        max_score=0,
        dry_run=True
    ):

        self.max_positions = int(
            max_positions
        )

        self.max_score = float(
            max_score
        )

        self.dry_run = bool(
            dry_run
        )

    # ==================================================
    # EXECUTE
    # ==================================================

    def execute(
        self,
        setup
    ):

        if not isinstance(
            setup,
            dict
        ):

            return {
                "status": "ERROR",
                "reason": "Invalid trade setup"
            }

        # ==============================================
        # SETUP STATUS
        # ==============================================

        if setup.get(
            "status"
        ) != "READY":

            return {

                "status": "NOT_EXECUTED",

                "symbol": setup.get(
                    "symbol"
                ),

                "reason": (
                    "Trade setup is not READY"
                )
            }

        # ==============================================
        # REQUIRED DATA
        # ==============================================

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

        score = float(
            setup.get(
                "score",
                0
            )
        )

        if not symbol:

            return {
                "status": "REJECTED",
                "reason": "Missing symbol"
            }

        if direction not in {
            "BULLISH",
            "BEARISH"
        }:

            return {
                "status": "REJECTED",
                "reason": "Invalid direction"
            }

        if (
            entry is None
            or stop_loss is None
            or take_profit is None
        ):

            return {
                "status": "REJECTED",
                "symbol": symbol,
                "reason": (
                    "Incomplete trade levels"
                )
            }

        # ==============================================
        # SCORE VALIDATION
        # ==============================================

        if (
            self.max_score > 0
            and score < self.max_score
        ):

            return {

                "status": "REJECTED",

                "symbol": symbol,

                "score": score,

                "reason": (
                    f"Score {score:.2f} "
                    f"below execution threshold "
                    f"{self.max_score:.2f}"
                )
            }

        # ==============================================
        # SYMBOL
        # ==============================================

        if not mt5.symbol_select(
            symbol,
            True
        ):

            return {

                "status": "ERROR",

                "symbol": symbol,

                "reason": (
                    "Unable to select symbol"
                )
            }

        # ==============================================
        # POSITION LIMIT
        # ==============================================

        positions = mt5.positions_get(
            symbol=symbol
        )

        if positions is None:

            positions = []

        if len(positions) >= self.max_positions:

            return {

                "status": "BLOCKED",

                "symbol": symbol,

                "reason": (
                    "Maximum position limit reached"
                ),

                "open_positions": len(
                    positions
                )
            }

        # ==============================================
        # BUILD ORDER
        # ==============================================

        tick = mt5.symbol_info_tick(
            symbol
        )

        if tick is None:

            return {

                "status": "ERROR",

                "symbol": symbol,

                "reason": (
                    "Live tick unavailable"
                )
            }

        if direction == "BULLISH":

            order_type = (
                mt5.ORDER_TYPE_BUY
            )

            price = float(
                tick.ask
            )

        else:

            order_type = (
                mt5.ORDER_TYPE_SELL
            )

            price = float(
                tick.bid
            )

        order = {

            "action":
                mt5.TRADE_ACTION_DEAL,

            "symbol":
                symbol,

            "volume":
                0.01,

            "type":
                order_type,

            "price":
                price,

            "sl":
                float(stop_loss),

            "tp":
                float(take_profit),

            "deviation":
                20,

            "magic":
                20260806,

            "comment":
                "AncestorFX",

            "type_time":
                mt5.ORDER_TIME_GTC,

            "type_filling":
                mt5.ORDER_FILLING_IOC
        }

        # ==============================================
        # DRY RUN
        # ==============================================

        if self.dry_run:

            return {

                "status":
                    "DRY_RUN",

                "symbol":
                    symbol,

                "direction":
                    direction,

                "price":
                    price,

                "entry":
                    float(entry),

                "stop_loss":
                    float(stop_loss),

                "take_profit":
                    float(take_profit),

                "score":
                    score,

                "order":
                    order
            }

        # ==============================================
        # LIVE EXECUTION
        # ==============================================

        result = mt5.order_send(
            order
        )

        if result is None:

            return {

                "status":
                    "ERROR",

                "symbol":
                    symbol,

                "reason":
                    "MT5 order_send returned None"
            }

        if result.retcode != mt5.TRADE_RETCODE_DONE:

            return {

                "status":
                    "FAILED",

                "symbol":
                    symbol,

                "direction":
                    direction,

                "retcode":
                    result.retcode,

                "comment":
                    result.comment
            }

        return {

            "status":
                "EXECUTED",

            "symbol":
                symbol,

            "direction":
                direction,

            "price":
                price,

            "entry":
                float(entry),

            "stop_loss":
                float(stop_loss),

            "take_profit":
                float(take_profit),

            "score":
                score,

            "ticket":
                result.order
        }