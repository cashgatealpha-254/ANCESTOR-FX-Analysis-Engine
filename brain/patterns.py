from collections import Counter


class PatternEngine:

    def __init__(self):
        pass

    def analyze(self, trades):

        if len(trades) == 0:

            return {

                "Most Common Bias": None,

                "Most Common Zone": None,

                "Most Common Liquidity": None,

                "Best Grade": None,

                "Total Trades": 0

            }

        bias = Counter(

            x["bias"]

            for x in trades

        )

        zone = Counter(

            x["zone"]

            for x in trades

        )

        liquidity = Counter(

            x["liquidity"]

            for x in trades

        )

        grade = Counter(

            x["grade"]

            for x in trades

        )

        return {

            "Most Common Bias":

                bias.most_common(1)[0][0],

            "Most Common Zone":

                zone.most_common(1)[0][0],

            "Most Common Liquidity":

                liquidity.most_common(1)[0][0],

            "Best Grade":

                grade.most_common(1)[0][0],

            "Total Trades":

                len(trades)

        }

    def strongest_pattern(self, trades):

        wins = [

            x

            for x in trades

            if x["outcome"] in [

                "Win",

                "TP1",

                "TP2"

            ]

        ]

        return self.analyze(wins)

    def weakest_pattern(self, trades):

        losses = [

            x

            for x in trades

            if x["outcome"] in [

                "Loss",

                "SL"

            ]

        ]

        return self.analyze(losses)