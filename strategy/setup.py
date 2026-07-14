class SetupEngine:

    def __init__(self):
        pass

    def build(self, analysis):

        RR = 5

        decision = analysis["Decision"]
        support = analysis["support"]
        resistance = analysis["resistance"]
        protected_levels = analysis["protected_levels"]

        if decision == "BUY":

            entry = support
            stop_loss = protected_levels["Protected Low"]["price"]

            risk = abs(entry - stop_loss)

            take_profit = entry + (risk * RR)

        elif decision == "SELL":

            entry = resistance
            stop_loss = protected_levels["Protected High"]["price"]

            risk = abs(stop_loss - entry)

            take_profit = entry - (risk * RR)

        else:

            entry = None
            stop_loss = None
            take_profit = None

        return {
            "Entry": entry,
            "Stop Loss": stop_loss,
            "Take Profit": take_profit,
            "Risk Reward": f"1:{RR}"
        }