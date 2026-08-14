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
                "symbol": setup.get("symbol"),
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

        volume = setup.get(
            "volume"
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

        if volume is None:

            return {
                "status": "REJECTED",
                "symbol": symbol,
                "reason": (
                    "Missing validated position size"
                )
            }

        try:

            entry = float(entry)
            stop_loss = float(stop_loss)
            take_profit = float(take_profit)
            volume = float(volume)

        except (
            TypeError,
            ValueError
        ):

            return {
                "status": "REJECTED",
                "symbol": symbol,
                "reason": (
                    "Invalid execution values"
                )
            }

        if volume <= 0:

            return {
                "status": "REJECTED",
                "symbol": symbol,
                "reason": (
                    "Invalid position size"
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


        # ==============================================
        # EXECUTION ZONE CHECK
        # ==============================================

        zone_low = setup.get(
            "zone_low"
        )

        zone_high = setup.get(
            "zone_high"
        )

        if (
            zone_low is None
            or zone_high is None
        ):

            return {

                "status":
                    "BLOCKED",

                "symbol":
                    symbol,

                "direction":
                    direction,

                "price":
                    price,

                "reason":
                    "Execution zone unavailable"
            }

        try:

            zone_low = float(
                zone_low
            )

            zone_high = float(
                zone_high
            )

        except (
            TypeError,
            ValueError
        ):

            return {

                "status":
                    "BLOCKED",

                "symbol":
                    symbol,

                "direction":
                    direction,

                "price":
                    price,

                "reason":
                    "Invalid execution zone"
            }

        if zone_low > zone_high:

            zone_low, zone_high = (
                zone_high,
                zone_low
            )

        # ==============================================
        # PRICE MUST BE INSIDE VALID ENTRY ZONE
        # ==============================================

        if not (
            zone_low
            <= price
            <= zone_high
        ):

            return {

                "status":
                    "BLOCKED",

                "symbol":
                    symbol,

                "direction":
                    direction,

                "price":
                    price,

                "zone_low":
                    zone_low,

                "zone_high":
                    zone_high,

                "reason":
                    "Live price is outside execution zone"
            }

        # ==============================================
        # BROKER ORDER VALIDATION
        # ==============================================

        symbol_info = mt5.symbol_info(
            symbol
        )

        if symbol_info is None:

            return {

                "status":
                    "ERROR",

                "symbol":
                    symbol,

                "reason":
                    "Symbol information unavailable"
            }

        volume = setup.get(
            "volume"
        )

        if volume is None:

            return {

                "status":
                    "BLOCKED",

                "symbol":
                    symbol,

                "reason":
                    "Position size unavailable"
            }

        try:

            volume = float(
                volume
            )

        except (
            TypeError,
            ValueError
        ):

            return {

                "status":
                    "BLOCKED",

                "symbol":
                    symbol,

                "reason":
                    "Invalid position size"
            }

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

            return {

                "status":
                    "BLOCKED",

                "symbol":
                    symbol,

                "volume":
                    volume,

                "reason":
                    "Volume below broker minimum"
            }

        if volume > volume_max:

            return {

                "status":
                    "BLOCKED",

                "symbol":
                    symbol,

                "volume":
                    volume,

                "reason":
                    "Volume above broker maximum"
            }

        if volume_step <= 0:

            return {

                "status":
                    "ERROR",

                "symbol":
                    symbol,

                "reason":
                    "Invalid broker volume step"
            }

        # ==============================================
        # VOLUME STEP VALIDATION
        # ==============================================

        step_units = round(
            volume
            / volume_step
        )

        normalized_volume = (
            step_units
            * volume_step
        )

        if abs(
            normalized_volume
            - volume
        ) > 1e-8:

            return {

                "status":
                    "BLOCKED",

                "symbol":
                    symbol,

                "volume":
                    volume,

                "volume_step":
                    volume_step,

                "reason":
                    "Volume does not match broker volume step"
            }

        volume = round(
            volume,
            8
        )

        # ==============================================
        # BUILD ORDER
        # ==============================================

        order = {

            "action":
                mt5.TRADE_ACTION_DEAL,

            "symbol":
                symbol,

            "volume":
                volume,

            "type":
                order_type,

            "price":
                price,

            "sl":
                stop_loss,

            "tp":
                take_profit,

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
                    entry,

                "stop_loss":
                    stop_loss,

                "take_profit":
                    take_profit,

                "volume":
                    volume,

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
                entry,

            "stop_loss":
                stop_loss,

            "take_profit":
                take_profit,

            "volume":
                volume,

            "score":
                score,

            "ticket":
                result.order
        }