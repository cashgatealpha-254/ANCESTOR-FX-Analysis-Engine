def track_setup(results):

    return {

        "Bias": results["market_bias"]["Market Bias"],
        "Confidence": results["confidence"],
        "Grade": results["grade"],
        "Decision": results["decision"],
        "Trade Score": results["trade_score"]["Trade Score"]

    }