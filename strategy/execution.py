class ExecutionEngine:

    def __init__(self):
        pass

    def prepare(self, decision, confidence):

        if decision == "BUY":
            return {
                "action": "BUY",
                "risk": "NORMAL" if confidence >= 90 else "LOW"
            }

        elif decision == "SELL":
            return {
                "action": "SELL",
                "risk": "NORMAL" if confidence >= 90 else "LOW"
            }

        return {
            "action": "WAIT",
            "risk": "NONE"
        }

    def execute(self, decision, setup, current_price):

        if decision["decision"] == "WAIT":
            return {
                "Status": "WAIT",
                "Reason": "No valid setup."
            }

        entry = setup["Entry"]

        if entry is None:
            return {
                "Status": "WAIT",
                "Reason": "No valid entry."
            }

        stop_loss = setup["Stop Loss"]
        take_profit = setup["Take Profit"]

        distance = abs(current_price - entry)

        tolerance = 0.00050

        if distance <= tolerance:

            status = "ENTER NOW"

        elif decision["decision"] == "BUY" and current_price < entry:

            status = "WAIT FOR RETEST"

        elif decision["decision"] == "SELL" and current_price > entry:

            status = "WAIT FOR RETEST"

        else:

            status = "MISSED TRADE"

        return {
            "Status": status,
            "Direction": decision["decision"],
            "Current Price": round(current_price, 5),
            "Entry": round(entry, 5),
            "Distance": round(distance, 5),
            "Stop Loss": round(stop_loss, 5),
            "Take Profit": round(take_profit, 5),
            "Risk Reward": setup["Risk Reward"]
        }