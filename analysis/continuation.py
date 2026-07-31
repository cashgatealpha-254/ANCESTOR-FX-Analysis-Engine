def analyze_continuation(current, previous):

    if previous is None:

        return {
            "Continuation": "Unknown"
        }

    if current["market_bias"]["Market Bias"] == previous["Previous Bias"]:

        continuation = "Continuation"

    else:

        continuation = "Reversal"

    return {

        "Continuation": continuation

    }