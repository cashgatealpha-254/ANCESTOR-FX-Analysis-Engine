import MetaTrader5 as mt5
import time


class TradeMonitor:

    def __init__(self, journal, poll_seconds=2):

        self.journal = journal
        self.poll_seconds = poll_seconds

    def monitor(self, ticket, trade_record):

        while True:

            positions = mt5.positions_get(
                ticket=ticket
            )

            # Position closed
            if not positions:

                return self._finalize(
                    ticket,
                    trade_record
                )

            time.sleep(
                self.poll_seconds
            )

    def _finalize(
        self,
        ticket,
        trade_record
    ):

        deals = mt5.history_deals_get(
            ticket=ticket
        )

        profit = 0.0

        if deals:

            profit = sum(
                float(
                    deal.profit
                )
                for deal in deals
            )

        result = (
            "WIN"
            if profit > 0
            else "LOSS"
            if profit < 0
            else "BREAKEVEN"
        )

        trade_record["outcome"] = {

            "result": result,

            "profit": round(
                profit,
                2
            ),

            "ticket": ticket
        }

        self.journal.save(
            trade_record
        )

        return trade_record