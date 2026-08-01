def coach(results):

    messages = []

    confidence = results["confidence"]
    grade = results["grade"]
    decision = results["decision"]

    if confidence >= 90:
        messages.append(
            "Excellent confidence. Stay disciplined."
        )

    elif confidence >= 75:
        messages.append(
            "Good setup. Wait for precise execution."
        )

    else:
        messages.append(
            "Patience. Better opportunities will come."
        )

    if grade == "A":
        messages.append(
            "Professional-grade setup."
        )

    elif grade == "B":
        messages.append(
            "Tradable, but manage risk carefully."
        )

    else:
        messages.append(
            "Observe only. Do not force trades."
        )

    if decision == "BUY":
        messages.append(
            "Prepare only after confirmation."
        )

    elif decision == "SELL":
        messages.append(
            "Remain patient before entering."
        )

    else:
        messages.append(
            "Stay flat until the market reveals intent."
        )

    return {
        "Coach": messages
    }