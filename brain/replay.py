class ReplayEngine:

    def __init__(self):
        pass

    def search(self, records, filters):

        matches = []

        for trade in records:

            valid = True

            for key, value in filters.items():

                if trade.get(key) != value:
                    valid = False
                    break

            if valid:
                matches.append(trade)

        return matches

    def latest(self, records, limit=10):

        return records[-limit:]

    def wins(self, records):

        return [

            x for x in records

            if x.get("outcome") in [

                "Win",

                "TP1",

                "TP2"

            ]

        ]

    def losses(self, records):

        return [

            x for x in records

            if x.get("outcome") in [

                "Loss",

                "SL"

            ]

        ]

    def statistics(self, records):

        total = len(records)

        wins = len(self.wins(records))

        losses = len(self.losses(records))

        pending = total - wins - losses

        if total == 0:

            win_rate = 0

        else:

            win_rate = round(

                wins / total * 100,

                2

            )

        return {

            "Total": total,

            "Wins": wins,

            "Losses": losses,

            "Pending": pending,

            "Win Rate": win_rate

        }