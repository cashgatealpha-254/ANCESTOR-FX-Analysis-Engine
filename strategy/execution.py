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
                "action": "WAIT",
                "entry": None,
                "stop_loss": None,
                "take_profit": None
            }
        if decision["decision"] == "BUY":
            entry = setup["Entry"]
            stop_loss = setup["Stop Loss"]
            take_profit = setup["Take Profit"]

            if current_price < entry:
                return {
                    "action": "BUY",
                    "entry": entry,
                    "stop_loss": stop_loss,
                    "take_profit": take_profit
                }
            else:
                return {
                    "action": "WAIT",
                    "entry": None,
                    "stop_loss": None,
                    "take_profit": None
                }
            
        elif decision["decision"] == "SELL":
            entry = setup["Entry"]
            stop_loss = setup["Stop Loss"]
            take_profit = setup["Take Profit"]

            if current_price > entry:
                return {
                    "action": "SELL",
                    "entry": entry,
                    "stop_loss": stop_loss,
                    "take_profit": take_profit
                }
            else:
                return {
                    "action": "WAIT",
                    "entry": None,
                    "stop_loss": None,
                    "take_profit": None
                }
    
    def execute(self, decision, setup, current_price):

        if decision == "WAIT":
            return {
                "Status": "WAIT",
                "Reason": "No valid setup."
            }

        entry = setup["Entry"]
        if entry is None:
            return {
                "Status": "WAIT",
                "Reason": "No valid entry point."
            }
        stop_loss = setup["Stop Loss"]
        take_profit = setup["Take Profit"]

        distance = abs(current_price - entry)

        # Adjustable tolerance
        tolerance = 0.00050

        if distance <= tolerance:
            status = "ENTER NOW"

        elif current_price < entry and decision == "BUY":
            status = "WAIT FOR RETEST"

        elif current_price > entry and decision == "SELL":
            status = "WAIT FOR RETEST"

        else:
            status = "MISSED TRADE"

        return {
            "Status": status,
            "Current Price": round(current_price, 5),
            "Entry": round(entry, 5),
            "Distance": round(distance, 5),
            "Stop Loss": round(stop_loss, 5),
            "Take Profit": round(take_profit, 5),
            "Risk Reward": setup["Risk Reward"]
        }