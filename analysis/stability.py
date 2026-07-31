def analyze_stability(history):

    if len(history) < 3:

        return {

            "Stability": "Insufficient Data"

        }

    last_three = [h["market_bias"] for h in history[-3:]]

    if len(set(last_three)) == 1:

        return {

            "Stability": "Stable"

        }

    return {

        "Stability": "Changing"

    }