from collections import Counter


class TraderDNA:

    def __init__(self):
        pass

    def analyze(self, trades):

        if len(trades) == 0:

            return {

                "Preferred Bias": None,

                "Preferred Pair": None,

                "Preferred Session": None,

                "Preferred Zone": None,

                "Preferred Grade": None,

                "Trading Style": "Unknown"

            }

        bias = Counter(
            t.get("bias")
            for t in trades
        )

        pair = Counter(
            t.get("symbol")
            for t in trades
        )

        session = Counter(
            t.get("session")
            for t in trades
        )

        zone = Counter(
            t.get("zone")
            for t in trades
        )

        grade = Counter(
            t.get("grade")
            for t in trades
        )

        average_duration = sum(

            t.get("duration", 0)

            for t in trades

        ) / len(trades)

        if average_duration < 60:

            style = "Scalper"

        elif average_duration < 240:

            style = "Intraday"

        elif average_duration < 1440:

            style = "Swing Trader"

        else:

            style = "Position Trader"

        return {

            "Preferred Bias":

                bias.most_common(1)[0][0],

            "Preferred Pair":

                pair.most_common(1)[0][0],

            "Preferred Session":

                session.most_common(1)[0][0],

            "Preferred Zone":

                zone.most_common(1)[0][0],

            "Preferred Grade":

                grade.most_common(1)[0][0],

            "Average Duration":

                round(average_duration, 2),

            "Trading Style":

                style

        }

    def summary(self, dna):

        return (

            f"{dna['Trading Style']} | "

            f"{dna['Preferred Pair']} | "

            f"{dna['Preferred Session']}"

        )