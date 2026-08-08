import MetaTrader5 as mt5
from datetime import datetime


class TradePolicy:

    def __init__(
        self,
        max_positions=1,
        max_daily_trades=3,
        one_position_per_symbol=True,
        block_opposite_position=True
    ):

        self.max_positions = int(max_positions)
        self.max_daily_trades = int(max_daily_trades)

        self.one_position_per_symbol = (
            bool(one_position_per_symbol)
        )

        self.block_opposite_position = (
            bool(block_opposite_position)
        )

    # ==================================================
    # CHECK
    # ==================================================

    def check(self, symbol, direction):

        direction = str(
            direction
        ).upper()

        if direction not in {
            "BULLISH",
            "BEARISH"
        }:

            return self._blocked(
                "Invalid direction"
            )

        # ==============================================
        # OPEN POSITIONS
        # ==============================================

        positions = mt5.positions_get()

        if positions is None:
            positions = []

        if len(positions) >= self.max_positions:

            return self._blocked(
                "Maximum open positions reached"
            )

        # ==============================================
        # SYMBOL POSITIONS
        # ==============================================

        symbol_positions = [

            position
            for position in positions

            if position.symbol == symbol
        ]

        if (
            self.one_position_per_symbol
            and symbol_positions
        ):

            return self._blocked(
                "Position already exists for symbol"
            )

        # ==============================================
        # OPPOSITE POSITION
        # ==============================================

        if self.block_opposite_position:

            for position in symbol_positions:

                if (
                    direction == "BULLISH"
                    and position.type
                    == mt5.POSITION_TYPE_SELL
                ):

                    return self._blocked(
                        "Opposite position exists"
                    )

                if (
                    direction == "BEARISH"
                    and position.type
                    == mt5.POSITION_TYPE_BUY
                ):

                    return self._blocked(
                        "Opposite position exists"
                    )

        # ==============================================
        # DAILY TRADES
        # ==============================================

        start = datetime.now().replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        deals = mt5.history_deals_get(
            start,
            datetime.now()
        )

        if deals is None:
            deals = []

        entry_deals = [

            deal
            for deal in deals

            if deal.entry
            == mt5.DEAL_ENTRY_IN
        ]

        if len(entry_deals) >= self.max_daily_trades:

            return self._blocked(
                "Maximum daily trades reached"
            )

        # ==============================================
        # ALLOWED
        # ==============================================

        return {

            "status": "ALLOW",

            "symbol": symbol,

            "direction": direction,

            "open_positions": len(
                positions
            ),

            "symbol_positions": len(
                symbol_positions
            ),

            "daily_trades": len(
                entry_deals
            ),

            "max_positions": (
                self.max_positions
            ),

            "max_daily_trades": (
                self.max_daily_trades
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