class ReasoningEngine:

    def explain(self, analysis):

        reasons = []

        if analysis["trend"] == "Bullish":
            reasons.append("Bullish EMA trend")

        if analysis["market_bias"] == "Bullish":
            reasons.append("Market bias is bullish")

        if analysis["market_structure"] == "Bullish":
            reasons.append("Bullish market structure")

        if analysis["bos"]["BOS"] != "No BOS":
            reasons.append(analysis["bos"]["BOS"])

        if analysis["liquidity"]["Liquidity"] == "Buy Side":
            reasons.append("Buy-side liquidity targeted")

        return reasons