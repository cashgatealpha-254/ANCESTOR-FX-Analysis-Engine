def analyze_swing_structure(
    swing_highs,
    swing_lows
):
    """
    Classify confirmed swing points into:

        HH = Higher High
        LH = Lower High
        HL = Higher Low
        LL = Lower Low

    Returns:
        {
            "structure": [...],
            "latest": {...}
        }
    """

    structure = []

    # ==================================================
    # HIGH STRUCTURE
    # ==================================================

    for i in range(1, len(swing_highs)):

        previous = swing_highs[i - 1]
        current = swing_highs[i]

        if current["price"] > previous["price"]:

            structure.append({
                "type": "HH",
                "price": float(
                    current["price"]
                ),
                "index": current["index"],
                "source": "SWING_HIGH"
            })

        elif current["price"] < previous["price"]:

            structure.append({
                "type": "LH",
                "price": float(
                    current["price"]
                ),
                "index": current["index"],
                "source": "SWING_HIGH"
            })

    # ==================================================
    # LOW STRUCTURE
    # ==================================================

    for i in range(1, len(swing_lows)):

        previous = swing_lows[i - 1]
        current = swing_lows[i]

        if current["price"] > previous["price"]:

            structure.append({
                "type": "HL",
                "price": float(
                    current["price"]
                ),
                "index": current["index"],
                "source": "SWING_LOW"
            })

        elif current["price"] < previous["price"]:

            structure.append({
                "type": "LL",
                "price": float(
                    current["price"]
                ),
                "index": current["index"],
                "source": "SWING_LOW"
            })

    # ==================================================
    # CHRONOLOGICAL ORDER
    # ==================================================

    structure.sort(
        key=lambda item: item["index"]
    )

    # ==================================================
    # LATEST STRUCTURE
    # ==================================================

    latest = (
        structure[-1]
        if structure
        else None
    )

    return {
        "structure": structure,
        "latest": latest
    }