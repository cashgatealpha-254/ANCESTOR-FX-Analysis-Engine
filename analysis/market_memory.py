def update_market_memory(results):

    return {

        "Previous Bias": results["market_bias"]["Market Bias"],
        "Previous Trend": results["trend"]["Trend"],
        "Previous Structure": results["market_structure"]["Structure"],
        "Previous Decision": results["decision"]

    }