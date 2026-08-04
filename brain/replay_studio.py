class ReplayStudio:

    def __init__(self):
        pass

    def timeline(self, trades):

        timeline = []

        for trade in trades:

            timeline.append({

                "Date": trade.get("date"),

                "Pair": trade.get("symbol"),

                "Bias": trade.get("bias"),

                "Zone": trade.get("zone"),

                "Liquidity": trade.get("liquidity"),

                "Decision": trade.get("decision"),

                "Outcome": trade.get("outcome"),

                "Confidence": trade.get("confidence")

            })

        return timeline

    def latest(self, trades, limit=20):

        return self.timeline(trades[-limit:])

    def search(self, trades, keyword):

        keyword = keyword.lower()

        results = []

        for trade in trades:

            text = str(trade).lower()

            if keyword in text:

                results.append(trade)

        return results

    def replay(self, trades, index):

        if len(trades) == 0:

            return None

        if index < 0:

            index = 0

        if index >= len(trades):

            index = len(trades) - 1

        return trades[index]