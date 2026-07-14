class DecisionEngine:

    def __init__(self):
        pass

    def evaluate(self, analysis):

        trend = analysis["trend"]
        confidence = analysis["confidence"]
        market_bias = analysis["market_bias"]
        market_state = analysis["market_state"]
        market_structure = analysis["market_structure"]

        structure_memory = analysis["structure_memory"]
        protected_levels = analysis["protected_levels"]
        structure_strength = analysis["structure_strength"]

        if (
            trend == "Bullish"
            and market_bias == "BUY"
            and confidence >= 80
            and structure_strength == "Strong Bullish Structure"
        ):
            decision = "BUY"

        elif (
            trend == "Bearish"
            and market_bias == "SELL"
            and confidence >= 80
            and structure_strength == "Strong Bearish Structure"
        ):
            decision = "SELL"

        else:
            decision = "WAIT"

        return {
            "decision": decision,

            "analysis": {
                "trend": trend,
                "market_bias": market_bias,
                "market_state": market_state,
                "market_structure": market_structure,
                "confidence": confidence,
                "structure_memory": structure_memory,
                "protected_levels": protected_levels,
                "structure_strength": structure_strength
            }
        }