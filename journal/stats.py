from journal.reader import JournalReader


class JournalStats:

    def __init__(self):
        self.reader = JournalReader()

    def summary(self):

        trades = self.reader.read()

        executed = [
            t for t in trades
            if t.get("execution", {}).get("status")
            == "EXECUTED"
        ]

        wins = [
            t for t in executed
            if t.get("outcome", {}).get("result")
            == "WIN"
        ]

        losses = [
            t for t in executed
            if t.get("outcome", {}).get("result")
            == "LOSS"
        ]

        total = len(executed)

        return {
            "total_trades": total,
            "wins": len(wins),
            "losses": len(losses),
            "win_rate": (
                round(len(wins) / total * 100, 2)
                if total
                else 0
            ),
            "net_profit": round(
                sum(
                    float(
                        t.get("outcome", {})
                         .get("profit", 0)
                    )
                    for t in executed
                ),
                2
            )
        }