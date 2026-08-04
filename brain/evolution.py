from collections import defaultdict


class StrategyEvolution:

    def __init__(self):
        pass

    def analyze(self, trades):

        strategies = defaultdict(

            lambda: {

                "Wins": 0,

                "Losses": 0,

                "Total": 0

            }

        )

        for trade in trades:

            strategy = (

                f"{trade.get('bias')} | "

                f"{trade.get('zone')} | "

                f"{trade.get('liquidity')}"

            )

            strategies[strategy]["Total"] += 1

            if trade.get("outcome") in [

                "Win",

                "TP1",

                "TP2"

            ]:

                strategies[strategy]["Wins"] += 1

            elif trade.get("outcome") in [

                "Loss",

                "SL"

            ]:

                strategies[strategy]["Losses"] += 1

        report = {}

        for name, stats in strategies.items():

            if stats["Total"] == 0:

                win_rate = 0

            else:

                win_rate = round(

                    stats["Wins"]

                    / stats["Total"]

                    * 100,

                    2

                )

            report[name] = {

                "Wins": stats["Wins"],

                "Losses": stats["Losses"],

                "Total": stats["Total"],

                "Win Rate": win_rate

            }

        return report

    def strongest(self, report):

        if not report:

            return None

        return max(

            report,

            key=lambda x:

            report[x]["Win Rate"]

        )

    def weakest(self, report):

        if not report:

            return None

        return min(

            report,

            key=lambda x:

            report[x]["Win Rate"]

        )