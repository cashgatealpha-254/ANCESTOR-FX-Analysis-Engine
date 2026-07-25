def build(report):
    """
    Final verdict before the trader acts.
    """

    confidence = report.get("confidence", 0)
    trade_allowed = report.get("trade_allowed", False)
    grade = report.get("grade", "D")

    if not trade_allowed:
        return {
            "status": "NO TRADE",
            "color": "red",
            "message": "Risk rules blocked this setup."
        }

    if confidence >= 90 and grade == "A":
        return {
            "status": "EXECUTE",
            "color": "green",
            "message": "High-probability setup."
        }

    if confidence >= 70:
        return {
            "status": "WAIT",
            "color": "yellow",
            "message": "Setup exists but needs confirmation."
        }

    return {
        "status": "IGNORE",
        "color": "gray",
        "message": "Low-quality setup."
    }