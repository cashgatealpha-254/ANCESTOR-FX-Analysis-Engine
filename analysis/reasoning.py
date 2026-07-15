class ReasoningEngine:

    def explain(self, analysis):

        narrative = []

        if analysis["market_bias"] == "Bullish":
            narrative.append("Higher timeframe bias is bullish.")

        elif analysis["market_bias"] == "Bearish":
            narrative.append("Higher timeframe bias is bearish.")

        if analysis["bos"]:
            narrative.append("Recent Break of Structure confirms continuation.")

        if analysis["choch"]:
            narrative.append("Change of Character detected.")

        if analysis["liquidity"]:
            narrative.append("Liquidity sweep has occurred.")

        if analysis["execution"]["entry"]:
            narrative.append("Execution conditions satisfied.")

        return " ".join(narrative)