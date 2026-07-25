def build(results):
    """
    Creates the final trading report used by:
    - Dashboard
    - Journal
    - Alerts
    - API
    """

    execution = results.get("execution", {})
    risk = results.get("risk", {})

    report = {
        "symbol": results.get("symbol"),

        "grade": results.get("grade"),

        "confidence": results.get("confidence"),

        "decision": results.get("decision"),

        "setup": results.get("setup"),

        "entry": execution.get("entry"),

        "stop_loss": execution.get("stop_loss"),

        "take_profit": execution.get("take_profit"),

        "risk_reward": risk.get("risk_reward"),

        "trade_allowed": results.get("trade_allowed"),

        "reason": results.get("reasoning"),

        "narrative": results.get("narrative")
    }

    return report