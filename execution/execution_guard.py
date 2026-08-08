import MetaTrader5 as mt5


class ExecutionGuard:

    def __init__(
        self,
        max_positions=1,
        max_daily_trades=3
    ):

        self.max_positions = int(
            max_positions
        )

        self.max_daily_trades = int(
            max_daily_trades
        )

    def check(
        self,
        setup
    ):

        if not isinstance(setup, dict):

            return {
                "status": "BLOCKED",
                "reason": "Invalid setup"
            }

        if setup.get("status") != "READY":

            return {
                "status": "BLOCKED",
                "reason": "Setup is not READY"
            }

        # ==========================================
        # MT5 CONNECTION
        # ==========================================

        terminal = mt5.terminal_info()

        if terminal is None:

            return {
                "status": "BLOCKED",
                "reason": "MT5 terminal unavailable"
            }

        if not terminal.connected:

            return {
                "status": "BLOCKED",
                "reason": "MT5 terminal not connected"
            }

        # ==========================================
        # SYMBOL
        # ==========================================

        symbol = setup.get("symbol")

        if not symbol:

            return {
                "status": "BLOCKED",
                "reason": "Missing symbol"
            }

        symbol_info = mt5.symbol_info(
            symbol
        )

        if symbol_info is None:

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": "Symbol unavailable"
            }

        # ==========================================
        # SYMBOL TRADEABILITY
        # ==========================================

        if not symbol_info.visible:

            if not mt5.symbol_select(
                symbol,
                True
            ):

                return {
                    "status": "BLOCKED",
                    "symbol": symbol,
                    "reason": "Unable to select symbol"
                }

        # ==========================================
        # EXISTING POSITIONS
        # ==========================================

        positions = mt5.positions_get()

        if positions is None:

            positions = []

        if len(positions) >= self.max_positions:

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": "Maximum open positions reached",
                "open_positions": len(positions)
            }

        # ==========================================
        # RESULT
        # ==========================================

        return {

            "status": "ALLOW",

            "symbol": symbol,

            "open_positions": len(
                positions
            ),

            "max_positions": (
                self.max_positions
            ),

            "max_daily_trades": (
                self.max_daily_trades
            )
        }