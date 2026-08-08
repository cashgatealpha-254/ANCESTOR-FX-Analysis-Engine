import MetaTrader5 as mt5
from datetime import datetime, timezone


class PreExecutionEngine:

    def __init__(
        self,
        max_spread_points=30,
        max_price_deviation_points=20,
        max_open_positions=1,
        automation_enabled=False,
        kill_switch=True
    ):

        self.max_spread_points = float(
            max_spread_points
        )

        self.max_price_deviation_points = float(
            max_price_deviation_points
        )

        self.max_open_positions = int(
            max_open_positions
        )

        self.automation_enabled = bool(
            automation_enabled
        )

        self.kill_switch = bool(
            kill_switch
        )

    # ==================================================
    # VALIDATE
    # ==================================================

    def validate(self, sized_trade):

        if not isinstance(
            sized_trade,
            dict
        ):

            return {
                "status": "BLOCKED",
                "reason": "Invalid sized trade"
            }

        if sized_trade.get(
            "status"
        ) != "READY":

            return {
                "status": "BLOCKED",
                "reason": "Position sizing is not READY"
            }

        symbol = sized_trade.get(
            "symbol"
        )

        direction = str(
            sized_trade.get(
                "direction",
                ""
            )
        ).upper()

        planned_entry = sized_trade.get(
            "entry"
        )

        if not symbol:

            return {
                "status": "BLOCKED",
                "reason": "Missing symbol"
            }

        if direction not in {
            "BULLISH",
            "BEARISH"
        }:

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": "Invalid direction"
            }

        try:

            planned_entry = float(
                planned_entry
            )

        except (
            TypeError,
            ValueError
        ):

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": "Invalid planned entry"
            }

        # ==================================================
        # KILL SWITCH
        # ==================================================

        if self.kill_switch:

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": "Kill switch is active"
            }

        # ==================================================
        # MANUAL MODE
        # ==================================================

        if not self.automation_enabled:

            return {
                "status": "MANUAL",
                "symbol": symbol,
                "reason": "Automation disabled",
                "trade": sized_trade
            }

        # ==================================================
        # TERMINAL
        # ==================================================

        terminal = mt5.terminal_info()

        if terminal is None:

            return {
                "status": "ERROR",
                "symbol": symbol,
                "reason": "MT5 terminal unavailable"
            }

        if not terminal.connected:

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": "MT5 terminal not connected"
            }

        # ==================================================
        # ACCOUNT
        # ==================================================

        account = mt5.account_info()

        if account is None:

            return {
                "status": "ERROR",
                "symbol": symbol,
                "reason": "Account information unavailable"
            }

        equity = float(
            account.equity
        )

        if equity <= 0:

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": "Account equity is zero or invalid"
            }

        # ==================================================
        # SYMBOL
        # ==================================================

        symbol_info = mt5.symbol_info(
            symbol
        )

        if symbol_info is None:

            return {
                "status": "ERROR",
                "symbol": symbol,
                "reason": "Symbol information unavailable"
            }

        if not symbol_info.visible:

            selected = mt5.symbol_select(
                symbol,
                True
            )

            if not selected:

                return {
                    "status": "BLOCKED",
                    "symbol": symbol,
                    "reason": "Unable to select symbol"
                }

            symbol_info = mt5.symbol_info(
                symbol
            )

            if symbol_info is None:

                return {
                    "status": "ERROR",
                    "symbol": symbol,
                    "reason": (
                        "Symbol unavailable after selection"
                    )
                }

        # ==================================================
        # CURRENT TICK
        # ==================================================

        tick = mt5.symbol_info_tick(
            symbol
        )

        if tick is None:

            return {
                "status": "ERROR",
                "symbol": symbol,
                "reason": "Current tick unavailable"
            }

        bid = float(
            tick.bid
        )

        ask = float(
            tick.ask
        )

        if bid <= 0 or ask <= 0:

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": "Invalid bid/ask"
            }

        # ==================================================
        # POINT
        # ==================================================

        point = float(
            symbol_info.point
        )

        if point <= 0:

            return {
                "status": "ERROR",
                "symbol": symbol,
                "reason": "Invalid symbol point"
            }

        # ==================================================
        # SPREAD
        # ==================================================

        spread_points = (
            (ask - bid)
            / point
        )

        if (
            spread_points
            > self.max_spread_points
        ):

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "spread_points": round(
                    spread_points,
                    2
                ),
                "reason": (
                    "Spread exceeds configured limit"
                )
            }

        # ==================================================
        # EXECUTION PRICE
        # ==================================================

        if direction == "BULLISH":

            execution_price = ask

        else:

            execution_price = bid

        # ==================================================
        # PRICE DRIFT
        # ==================================================

        deviation_points = (
            abs(
                execution_price
                - planned_entry
            )
            / point
        )

        if (
            deviation_points
            > self.max_price_deviation_points
        ):

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "planned_entry": planned_entry,
                "execution_price": execution_price,
                "deviation_points": round(
                    deviation_points,
                    2
                ),
                "reason": (
                    "Execution price moved "
                    "too far from planned entry"
                )
            }

        # ==================================================
        # OPEN POSITION LIMIT
        # ==================================================

        positions = mt5.positions_get(
            symbol=symbol
        )

        if positions is None:

            positions = []

        open_positions = len(
            positions
        )

        if (
            open_positions
            >= self.max_open_positions
        ):

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "open_positions": open_positions,
                "reason": (
                    "Maximum open positions reached"
                )
            }

        # ==================================================
        # APPROVED
        # ==================================================

        return {

            "status": "EXECUTION_APPROVED",

            "symbol": symbol,

            "direction": direction,

            "planned_entry": planned_entry,

            "execution_price": execution_price,

            "price_deviation_points": round(
                deviation_points,
                2
            ),

            "spread_points": round(
                spread_points,
                2
            ),

            "open_positions": open_positions,

            "equity": equity,

            "volume": sized_trade.get(
                "volume"
            ),

            "validated_at": datetime.now(
                timezone.utc
            ).isoformat(),

            "trade": sized_trade
        }