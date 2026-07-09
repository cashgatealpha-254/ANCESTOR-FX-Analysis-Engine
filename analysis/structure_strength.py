def analyze_structure_strength(memory):

    latest_high = memory["Latest High"]
    previous_high = memory["Previous High"]

    latest_low = memory["Latest Low"]
    previous_low = memory["Previous Low"]

    if (
        latest_high
        and previous_high
        and latest_low
        and previous_low
    ):

        if (
            latest_high["price"] > previous_high["price"]
            and latest_low["price"] > previous_low["price"]
        ):
            strength = "Strong Bullish Structure"

        elif (
            latest_high["price"] < previous_high["price"]
            and latest_low["price"] < previous_low["price"]
        ):
            strength = "Strong Bearish Structure"

        else:
            strength = "Weak / Transition"

    else:
        strength = "Insufficient Data"

    return {
        "Structure Strength": strength
    }