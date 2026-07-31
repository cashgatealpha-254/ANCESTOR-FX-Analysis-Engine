def reflect(results):

    reflection = []

    reflection.append(
        f"Bias: {results['market_bias']['Market Bias']}"
    )

    reflection.append(
        f"Trend: {results['trend']['Trend']}"
    )

    reflection.append(
        f"Confidence: {results['confidence']}"
    )

    reflection.append(
        f"Trade Score: {results['trade_score']['Trade Score']}"
    )

    reflection.append(
        f"Decision: {results['decision']}"
    )

    return {

        "Reflection": reflection

    }