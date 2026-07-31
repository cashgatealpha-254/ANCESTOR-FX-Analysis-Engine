def analyze_improvement(results):

    improvements = []

    if results["confidence"] < 80:
        improvements.append(
            "Increase confidence before execution."
        )

    if results["confluence"]["Strength"] != "High":
        improvements.append(
            "Wait for stronger confluence."
        )

    if results["execution_quality"]["Quality"] != "Excellent":
        improvements.append(
            "Improve execution timing."
        )

    if not improvements:
        improvements.append(
            "No major improvements needed."
        )

    return {

        "Improvements": improvements

    }