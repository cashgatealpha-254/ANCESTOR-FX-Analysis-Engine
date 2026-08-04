class BehaviorEngine:

    def __init__(self):
        pass

    def analyze(self, trades):

        report = {

            "Early Entries": 0,

            "Late Entries": 0,

            "Rule Violations": 0,

            "Wins": 0,

            "Losses": 0

        }

        for trade in trades:

            if trade.get("entry_quality") == "Early":
                report["Early Entries"] += 1

            if trade.get("entry_quality") == "Late":
                report["Late Entries"] += 1

            if trade.get("rule_break", False):
                report["Rule Violations"] += 1

            if trade.get("outcome") in [
                "Win",
                "TP1",
                "TP2"
            ]:
                report["Wins"] += 1

            if trade.get("outcome") in [
                "Loss",
                "SL"
            ]:
                report["Losses"] += 1

        total = report["Wins"] + report["Losses"]

        if total == 0:

            score = 100

        else:

            penalties = (

                report["Early Entries"] * 2 +

                report["Late Entries"] * 2 +

                report["Rule Violations"] * 5

            )

            score = max(

                0,

                100 - penalties

            )

        report["Behaviour Score"] = score

        return report

    def recommendation(self, report):

        score = report["Behaviour Score"]

        if score >= 90:

            return "Excellent discipline."

        elif score >= 75:

            return "Good discipline. Minor improvements needed."

        elif score >= 60:

            return "Reduce execution mistakes."

        return "Focus on discipline before increasing risk."