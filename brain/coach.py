class CoachEngine:

    def __init__(self):
        pass

    def advise(self, results):

        advice = []

        confidence = results["adaptive_confidence"]["Adaptive Confidence"]

        trade_allowed = results.get("trade_allowed", False)

        if not trade_allowed:

            advice.append(
                "Trade blocked by Risk Manager."
            )

        if confidence >= 90:

            advice.append(
                "Exceptional setup. Follow the execution plan."
            )

        elif confidence >= 80:

            advice.append(
                "High conviction. Stay patient and wait for confirmation."
            )

        elif confidence >= 65:

            advice.append(
                "Good setup. Execute only if all confirmations remain valid."
            )

        elif confidence >= 50:

            advice.append(
                "Average setup. Reduce risk or wait."
            )

        else:

            advice.append(
                "Weak setup. Preserve capital."
            )

        if results["bos"]["BOS"]:

            advice.append(
                "Break of Structure confirmed."
            )

        if results["choch"]["CHoCH"]:

            advice.append(
                "Change of Character detected."
            )

        if results["liquidity"]["Liquidity"] != "None":

            advice.append(
                f"Liquidity Event: {results['liquidity']['Liquidity']}"
            )

        if results["market_structure"]["Structure"] == "Ranging":

            advice.append(
                "Market is ranging. Lower expectations."
            )

        if results["market_bias"]["Market Bias"] == "Bullish":

            advice.append(
                "Prefer long opportunities."
            )

        elif results["market_bias"]["Market Bias"] == "Bearish":

            advice.append(
                "Prefer short opportunities."
            )

        return advice

    def summary(self, results):

        confidence = results["adaptive_confidence"]["Adaptive Confidence"]

        decision = results["decision"]

        return (

            f"{decision} | "

            f"Confidence: {confidence}%"

        )