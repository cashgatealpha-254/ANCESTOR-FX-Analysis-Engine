def analyze_wait_signal(results):

    reasons = []

    wait = False

    # Low confidence
    if results["confidence"] < 70:
        wait = True
        reasons.append("Confidence below 70.")

    # Weak confluence
    if results["confluence"]["Strength"] == "Low":
        wait = True
        reasons.append("Weak confluence.")

    # Poor execution quality
    if results["execution_quality"]["Quality"] == "Poor":
        wait = True
        reasons.append("Poor execution quality.")

    # Risk manager
    if not results.get("trade_allowed", False):
        wait = True
        reasons.append("Risk manager blocked trade.")

    if wait:
        verdict = "WAIT"
    else:
        verdict = "READY"

    return {

        "Signal": verdict,
        "Reasons": reasons

    }