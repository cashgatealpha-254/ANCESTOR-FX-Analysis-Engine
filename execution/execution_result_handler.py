import MetaTrader5 as mt5


class ExecutionResultHandler:

    # ==================================================
    # HANDLE RESULT
    # ==================================================

    def handle(
        self,
        result,
        request=None
    ):

        if result is None:

            return {
                "status": "ERROR",
                "execution": "FAILED",
                "reason": "MT5 returned no result"
            }

        retcode = getattr(
            result,
            "retcode",
            None
        )

        comment = getattr(
            result,
            "comment",
            ""
        )

        order = getattr(
            result,
            "order",
            0
        )

        deal = getattr(
            result,
            "deal",
            0
        )

        volume = getattr(
            result,
            "volume",
            0.0
        )

        price = getattr(
            result,
            "price",
            0.0
        )

        # ==================================================
        # SUCCESS
        # ==================================================

        if retcode in {
            mt5.TRADE_RETCODE_DONE,
            mt5.TRADE_RETCODE_DONE_PARTIAL
        }:

            if retcode == (
                mt5.TRADE_RETCODE_DONE
            ):

                execution_status = "FILLED"

            else:

                execution_status = "PARTIAL"

            return {

                "status": "SUCCESS",

                "execution": (
                    execution_status
                ),

                "retcode": retcode,

                "comment": comment,

                "order": order,

                "deal": deal,

                "volume": float(
                    volume
                ),

                "price": float(
                    price
                ),

                "request": request
            }

        # ==================================================
        # REQUOTE / PRICE CHANGE
        # ==================================================

        if retcode in {

            mt5.TRADE_RETCODE_REQUOTE,

            mt5.TRADE_RETCODE_PRICE_CHANGED,

            mt5.TRADE_RETCODE_PRICE_OFF
        }:

            return {

                "status": "REJECTED",

                "execution": "PRICE_CHANGED",

                "retcode": retcode,

                "comment": comment,

                "order": order,

                "deal": deal,

                "reason": (
                    "Execution price changed"
                )
            }

        # ==================================================
        # INVALID REQUEST
        # ==================================================

        if retcode in {

            mt5.TRADE_RETCODE_INVALID,

            mt5.TRADE_RETCODE_INVALID_VOLUME,

            mt5.TRADE_RETCODE_INVALID_PRICE,

            mt5.TRADE_RETCODE_INVALID_STOPS
        }:

            return {

                "status": "REJECTED",

                "execution": "INVALID_REQUEST",

                "retcode": retcode,

                "comment": comment,

                "order": order,

                "deal": deal,

                "reason": (
                    "Broker rejected order parameters"
                )
            }

        # ==================================================
        # MARKET / TRADING STATE
        # ==================================================

        if retcode in {

            mt5.TRADE_RETCODE_MARKET_CLOSED,

            mt5.TRADE_RETCODE_TRADE_DISABLED,

            mt5.TRADE_RETCODE_TRADING_DISABLED
        }:

            return {

                "status": "REJECTED",

                "execution": "TRADING_UNAVAILABLE",

                "retcode": retcode,

                "comment": comment,

                "reason": (
                    "Trading is unavailable"
                )
            }

        # ==================================================
        # INSUFFICIENT FUNDS
        # ==================================================

        if retcode in {

            mt5.TRADE_RETCODE_NO_MONEY
        }:

            return {

                "status": "REJECTED",

                "execution": "INSUFFICIENT_FUNDS",

                "retcode": retcode,

                "comment": comment,

                "reason": (
                    "Insufficient margin/funds"
                )
            }

        # ==================================================
        # FALLBACK
        # ==================================================

        return {

            "status": "REJECTED",

            "execution": "BROKER_REJECTED",

            "retcode": retcode,

            "comment": comment,

            "order": order,

            "deal": deal,

            "reason": (
                "Unhandled MT5 trade response"
            )
        }