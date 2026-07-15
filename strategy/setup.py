class SetupEngine:

    def build(self, analysis):

        RR = 5

        decision = analysis["decision"]
        support = analysis["support"]
        resistance = analysis["resistance"]

        if decision == "BUY":

            entry = support
            stop_loss = support * 0.998

            risk = abs(entry - stop_loss)
            take_profit = entry + (risk * RR)

        elif decision == "SELL":

            entry = resistance
            stop_loss = resistance * 1.002

            risk = abs(entry - stop_loss)
            take_profit = entry - (risk * RR)

        else:

            entry = None
            stop_loss = None
            take_profit = None

        return {
            "entry": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "risk_reward": f"1:{RR}"
        }