class ExecutionEngine:

    def execute(self, decision, setup, current_price):

        if decision["decision"] == "WAIT":
            return {
                "status": "WAIT",
                "entry": None,
                "stop_loss": None,
                "take_profit": None
            }

        entry = setup["entry"]
        stop_loss = setup["stop_loss"]
        take_profit = setup["take_profit"]

        tolerance = 0.00050

        if abs(current_price - entry) <= tolerance:
            status = "ENTER NOW"

        elif decision["decision"] == "BUY" and current_price < entry:
            status = "WAIT FOR RETEST"

        elif decision["decision"] == "SELL" and current_price > entry:
            status = "WAIT FOR RETEST"

        else:
            status = "MISSED TRADE"

        return {
            "status": status,
            "entry": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "current_price": current_price,
            "risk_reward": setup["risk_reward"]
        }