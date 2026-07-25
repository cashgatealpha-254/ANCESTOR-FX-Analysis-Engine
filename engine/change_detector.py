# engine/change_detector.py

def compare(current, previous):

    if previous is None:
        return {
            "changes": ["First analysis available."]
        }

    changes = []

    # Confidence
    current_conf = current.get("confidence", 0)
    previous_conf = previous.get("confidence", 0)

    if current_conf > previous_conf:
        changes.append(
            f"Confidence increased (+{current_conf - previous_conf})"
        )

    elif current_conf < previous_conf:
        changes.append(
            f"Confidence decreased (-{previous_conf - current_conf})"
        )

    # Grade

    if current.get("grade") != previous.get("grade"):
        changes.append(
            f"Grade changed: {previous.get('grade')} → {current.get('grade')}"
        )

    # Decision

    if current.get("decision") != previous.get("decision"):
        changes.append(
            f"Decision changed: {previous.get('decision')} → {current.get('decision')}"
        )

    # Verdict

    current_status = current.get("verdict", {}).get("status")
    previous_status = previous.get("verdict", {}).get("status")

    if current_status != previous_status:
        changes.append(
            f"Verdict changed: {previous_status} → {current_status}"
        )

    return {
        "changes": changes
    }