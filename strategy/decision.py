class DecisionEngine:

    def __init__(self):
        pass

    def evaluate(self, analysis):

        trend = analysis["trend"]
        confidence = analysis["confidence"]
        market_bias = analysis["market_bias"]
        market_state = analysis["market_state"]
        structure_memory = analysis["structure_memory"]
        protected_levels = analysis["protected_levels"]
        structure_strength = analysis["structure_strength"]

        if (
            trend == "Bullish"
            and market_bias == "BUY"
            and confidence >= 80
        ):
            decision = "BUY"

        elif (
            trend == "Bearish"
            and market_bias == "SELL"
            and confidence >= 80
        ):
            decision = "SELL"

        else:
            decision = "WAIT"

        return {
            "decision": decision,
            "reason": {
                "trend": trend,
                "market_bias": market_bias,
                "market_state": market_state,
                "confidence": confidence,
                "structure_memory": structure_memory,
                "protected_levels": protected_levels,
                "structure_strength": structure_strength
            }
        }