# brain/risk_manager.py

def check(results):

    confidence = results.get("confidence", 0)

    if confidence < 70:
        return {
            "trade": False,
            "reason": "Confidence below trading threshold."
        }

    return {
        "trade": True,
        "reason": "Risk conditions satisfied."
    }