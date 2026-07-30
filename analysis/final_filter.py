def final_filter(results):

    passed = True
    reasons = []

    # Confidence
    if results["confidence"] < 75:
        passed = False
        reasons.append("Confidence too low.")

    # Execution Quality
    if results["execution_quality"]["Quality"] not in ["Excellent", "Good"]:
        passed = False
        reasons.append("Execution quality insufficient.")

    # Wait Signal
    if results["wait_signal"]["Signal"] == "WAIT":
        passed = False
        reasons.append("Wait signal active.")

    # Risk
    if not results.get("trade_allowed", False):
        passed = False
        reasons.append("Risk manager blocked trade.")

    return {

        "Passed": passed,
        "Reasons": reasons

    }