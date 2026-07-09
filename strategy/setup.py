class SetupEngine:

    def __init__(self):
        pass

    def build(self, analysis):

        RR = 5

        trend = analysis["trend"]
        decision = analysis["Decision"]
        support = analysis["support"]
        resistance = analysis["resistance"]
        supply_demand = analysis["supply_demand"]
        atr = analysis["atr"]

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
            "Entry": entry,
            "Stop Loss": stop_loss,
            "Take Profit": take_profit,
            "Risk Reward": f"1:{RR}"
        }