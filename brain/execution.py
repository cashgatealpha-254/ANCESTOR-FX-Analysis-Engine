def execution_plan(results):
    plan = {
        "entry": None,
        "stop_loss": None,
        "take_profit": None,
        "risk": "No Trade"
    }

    if results["decision"] == "BUY":

        zone = results["zones"]["demand"]

        plan["entry"] = zone["entry"]
        plan["stop_loss"] = zone["stop_loss"]
        plan["take_profit"] = zone["take_profit"]
        plan["risk"] = "2%"

    elif results["decision"] == "SELL":

        zone = results["zones"]["supply"]

        plan["entry"] = zone["entry"]
        plan["stop_loss"] = zone["stop_loss"]
        plan["take_profit"] = zone["take_profit"]
        plan["risk"] = "2%"

    return plan