import MetaTrader5 as mt5
from datetime import datetime


class ExecutionEngine:

    def __init__(
        self,
        deviation=20,
        magic_number=260806,
        comment="AncestorFX",
        max_positions=1
    ):

        self.deviation = int(deviation)
        self.magic_number = int(magic_number)
        self.comment = str(comment)
        self.max_positions = int(max_positions)

    # ==================================================
    # EXECUTE
    # ==================================================

    def execute(self, setup):

        # ------------------------------------------------
        # BASIC VALIDATION
        # ------------------------------------------------

        if not isinstance(setup, dict):

            return self._blocked(
                "Invalid execution payload"
            )

        if setup.get("status") != "READY":

            return self._blocked(
                "Position sizing did not produce READY setup"
            )

        symbol = setup.get("symbol")

        direction = str(
            setup.get(
                "direction",
                ""
            )
        ).upper()

        entry = setup.get("entry")
        stop_loss = setup.get("stop_loss")
        take_profit = setup.get("take_profit")
        volume = setup.get("volume")

        if not symbol:

            return self._blocked(
                "Missing symbol"
            )

        if direction not in {
            "BULLISH",
            "BEARISH"
        }:

            return self._blocked(
                "Invalid direction",
                symbol=symbol
            )

        # ------------------------------------------------
        # LEVEL VALIDATION
        # ------------------------------------------------

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
                "Invalid execution levels",
                symbol=symbol
            )

        if volume <= 0:

            return self._blocked(
                "Invalid trade volume",
                symbol=symbol
            )

        # ------------------------------------------------
        # CONNECTIVITY
        # ------------------------------------------------

        terminal = mt5.terminal_info()

        if terminal is None:

            return self._error(
                "MT5 terminal information unavailable",
                symbol=symbol
            )

        if not terminal.connected:

            return self._error(
                "MT5 terminal is not connected",
                symbol=symbol
            )

        # ------------------------------------------------
        # ACCOUNT SAFETY
        # ------------------------------------------------

        account = mt5.account_info()

        if account is None:

            return self._error(
                "Unable to retrieve account information",
                symbol=symbol
            )

        balance = float(
            account.balance
        )

        equity = float(
            account.equity
        )

        if balance <= 0:

            return self._blocked(
                "Account balance is zero or invalid",
                symbol=symbol,
                balance=balance,
                equity=equity
            )

        if equity <= 0:

            return self._blocked(
                "Account equity is zero or invalid",
                symbol=symbol,
                balance=balance,
                equity=equity
            )

        # ------------------------------------------------
        # SYMBOL
        # ------------------------------------------------

        symbol_info = mt5.symbol_info(
            symbol
        )

        if symbol_info is None:

            return self._error(
                "Symbol information unavailable",
                symbol=symbol
            )

        # ------------------------------------------------
        # ENSURE SYMBOL IS VISIBLE
        # ------------------------------------------------

        if not symbol_info.visible:

            selected = mt5.symbol_select(
                symbol,
                True
            )

            if not selected:

                return self._error(
                    "Unable to select symbol",
                    symbol=symbol
                )

            symbol_info = mt5.symbol_info(
                symbol
            )

            if symbol_info is None:

                return self._error(
                    "Symbol unavailable after selection",
                    symbol=symbol
                )

        # ------------------------------------------------
        # CURRENT TICK
        # ------------------------------------------------

        tick = mt5.symbol_info_tick(
            symbol
        )

        if tick is None:

            return self._error(
                "Unable to retrieve current tick",
                symbol=symbol
            )

        bid = float(tick.bid)
        ask = float(tick.ask)

        if bid <= 0 or ask <= 0:

            return self._blocked(
                "Invalid market prices",
                symbol=symbol,
                bid=bid,
                ask=ask
            )

        # ------------------------------------------------
        # EXECUTION PRICE
        # ------------------------------------------------

        if direction == "BULLISH":

            order_type = mt5.ORDER_TYPE_BUY
            market_price = ask

            if not (
                stop_loss < market_price
                and take_profit > market_price
            ):

                return self._blocked(
                    "Invalid bullish SL/TP relative to market",
                    symbol=symbol,
                    market_price=market_price
                )

        else:

            order_type = mt5.ORDER_TYPE_SELL
            market_price = bid

            if not (
                stop_loss > market_price
                and take_profit < market_price
            ):

                return self._blocked(
                    "Invalid bearish SL/TP relative to market",
                    symbol=symbol,
                    market_price=market_price
                )

        # ------------------------------------------------
        # POSITION LIMIT
        # ------------------------------------------------

        positions = mt5.positions_get(
            symbol=symbol
        )

        if positions is None:

            positions = []

        if len(positions) >= self.max_positions:

            return self._blocked(
                "Maximum open-position limit reached",
                symbol=symbol,
                open_positions=len(positions)
            )

        # ------------------------------------------------
        # VOLUME VALIDATION
        # ------------------------------------------------

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
                "Volume below broker minimum",
                symbol=symbol,
                volume=volume,
                broker_minimum=volume_min
            )

        if volume > volume_max:

            return self._blocked(
                "Volume above broker maximum",
                symbol=symbol,
                volume=volume,
                broker_maximum=volume_max
            )

        # ------------------------------------------------
        # VOLUME STEP VALIDATION
        # ------------------------------------------------

        step_count = round(
            volume / volume_step
        )

        normalized_volume = round(
            step_count * volume_step,
            8
        )

        if abs(
            normalized_volume - volume
        ) > 1e-8:

            return self._blocked(
                "Volume does not match broker volume step",
                symbol=symbol,
                volume=volume,
                volume_step=volume_step
            )

        # ------------------------------------------------
        # PRICE NORMALIZATION
        # ------------------------------------------------

        digits = int(
            symbol_info.digits
        )

        stop_loss = round(
            stop_loss,
            digits
        )

        take_profit = round(
            take_profit,
            digits
        )

        market_price = round(
            market_price,
            digits
        )

        # ------------------------------------------------
        # FINAL RISK CHECK
        # ------------------------------------------------

        risk_percent = setup.get(
            "actual_risk_percent"
        )

        if risk_percent is not None:

            try:

                risk_percent = float(
                    risk_percent
                )

            except (
                TypeError,
                ValueError
            ):

                return self._blocked(
                    "Invalid calculated risk percentage",
                    symbol=symbol
                )

            if risk_percent <= 0:

                return self._blocked(
                    "Calculated risk is invalid",
                    symbol=symbol
                )

            if risk_percent > 2.0:

                return self._blocked(
                    "Execution risk exceeds hard safety limit",
                    symbol=symbol,
                    actual_risk_percent=risk_percent
                )

        # ------------------------------------------------
        # ORDER REQUEST
        # ------------------------------------------------

        request = {

            "action": mt5.TRADE_ACTION_DEAL,

            "symbol": symbol,

            "volume": normalized_volume,

            "type": order_type,

            "price": market_price,

            "sl": stop_loss,

            "tp": take_profit,

            "deviation": self.deviation,

            "magic": self.magic_number,

            "comment": self.comment,

            "type_time": mt5.ORDER_TIME_GTC,

            "type_filling": (
                mt5.ORDER_FILLING_IOC
            )
        }

        # ------------------------------------------------
        # PRE-TRADE CHECK
        # ------------------------------------------------

        check = mt5.order_check(
            request
        )

        if check is None:

            return self._error(
                "MT5 order_check returned no result",
                symbol=symbol
            )

        check_retcode = getattr(
            check,
            "retcode",
            None
        )

        if check_retcode != mt5.TRADE_RETCODE_DONE:

            return self._blocked(
                "Broker rejected pre-trade check",
                symbol=symbol,
                retcode=check_retcode,
                comment=getattr(
                    check,
                    "comment",
                    ""
                )
            )

        # ------------------------------------------------
        # EXECUTE
        # ------------------------------------------------

        result = mt5.order_send(
            request
        )

        if result is None:

            return self._error(
                "MT5 order_send returned no result",
                symbol=symbol
            )

        retcode = getattr(
            result,
            "retcode",
            None
        )

        # ------------------------------------------------
        # SUCCESS
        # ------------------------------------------------

        if retcode == mt5.TRADE_RETCODE_DONE:

            return {

                "status": "EXECUTED",

                "symbol": symbol,

                "direction": direction,

                "volume": normalized_volume,

                "entry": market_price,

                "stop_loss": stop_loss,

                "take_profit": take_profit,

                "ticket": getattr(
                    result,
                    "order",
                    None
                ),

                "deal": getattr(
                    result,
                    "deal",
                    None
                ),

                "retcode": retcode,

                "comment": getattr(
                    result,
                    "comment",
                    ""
                ),

                "timestamp": (
                    datetime.utcnow().isoformat()
                )
            }

        # ------------------------------------------------
        # REJECTION
        # ------------------------------------------------

        return {

            "status": "REJECTED",

            "symbol": symbol,

            "direction": direction,

            "volume": normalized_volume,

            "entry": market_price,

            "stop_loss": stop_loss,

            "take_profit": take_profit,

            "retcode": retcode,

            "comment": getattr(
                result,
                "comment",
                ""
            ),

            "timestamp": (
                datetime.utcnow().isoformat()
            )
        }

    # ==================================================
    # HELPERS
    # ==================================================

    @staticmethod
    def _blocked(
        reason,
        **kwargs
    ):

        result = {

            "status": "BLOCKED",

            "reason": reason
        }

        result.update(
            kwargs
        )

        return result

    @staticmethod
    def _error(
        reason,
        **kwargs
    ):

        result = {

            "status": "ERROR",

            "reason": reason
        }

        result.update(
            kwargs
        )

        return result